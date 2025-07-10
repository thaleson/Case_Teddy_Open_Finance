"""
TalentAI Streamlit App

This frontend application allows users to upload resumes (PDF, JPG, PNG),
optionally submit a recruitment query, and receive intelligent summaries
or comparisons using OCR and LLM-based processing.

Features:
---------
- Upload multiple resumes
- Provide a user ID and request ID
- Submit a recruitment-related query
- Get AI-generated summaries or selection answers
- Uses REST API for processing (`/analyze/`)
"""

import streamlit as st
import requests
import uuid
import os

def local_css(file_name: str):
    """
    Injects local CSS into the Streamlit app.

    Args:
        file_name (str): Path to the CSS file to be loaded.

    Returns:
        None
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css(os.path.join("styles", "style.css"))


st.set_page_config(
    page_title="TalentAI - Análise de Currículos",
    layout="centered",
    initial_sidebar_state="auto"
)


st.title("🚀 TalentAI - Análise Inteligente de Currículos")
st.markdown(
    "**OCR + LLM** para extrair, resumir e comparar currículos em segundos!",
    unsafe_allow_html=True
)


uploaded_files = st.file_uploader(
    "🗂️ Envie currículos (PDF/JPG/PNG)",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)


user_id = st.text_input(
    "👤 Seu identificador (user_id)",
    help="Informe seu nome, e-mail ou matrícula"
)

request_id = st.text_input(
    "🆔 ID da requisição (request_id)",
    value=str(uuid.uuid4()),
    help="UUID único para o seu request"
)

query = st.text_area(
    "❓ Query de recrutamento (opcional)",
    placeholder="Ex: Qual desses currículos se encaixa melhor na vaga de Engenheiro Python Sênior?"
)

st.markdown("<hr>", unsafe_allow_html=True)


if st.button("Enviar para análise"):
    if not uploaded_files or not user_id or not request_id:
        st.error("Por favor, envie ao menos um arquivo e preencha todos os campos obrigatórios.")
    else:
        
        files_data = [("files", (f.name, f.read(), f.type)) for f in uploaded_files]
        data = {"user_id": user_id, "request_id": request_id}
        if query.strip():
            data["query"] = query

        
        api_url = os.getenv("API_URL", "http://api:8000/analyze/")
        with st.spinner("🔄 Processando... aguarde um instante"):
            try:
                response = requests.post(api_url, files=files_data, data=data, timeout=600)
                response.raise_for_status()
                result = response.json()

                st.success("✅ Processamento concluído!")
                st.markdown("## 📋 Resultado:")

                if "summaries" in result:
                    for i, summary in enumerate(result["summaries"], 1):
                        st.markdown(f"**Resumo do Currículo {i}:**")
                        st.write(summary)
                elif "answer" in result:
                    st.markdown("**Resposta à sua query:**")
                    st.write(result["answer"])
                else:
                    st.write(result)

            except Exception as e:
                st.error(f"⚠️ Erro: {e}")

st.markdown("<hr>", unsafe_allow_html=True)
st.info("ℹ️ Nenhum currículo é armazenado no servidor — só logs de uso para auditoria.")
