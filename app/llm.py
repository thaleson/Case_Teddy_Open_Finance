"""
LLM-based Resume Analysis Module

This module provides functionality to summarize resumes or answer recruitment-related
queries using a large language model (LLM) via the GROQ API. It communicates with
a hosted model (e.g., LLaMA3) and generates intelligent responses based on resume content.

Environment Variables:
----------------------
- GROQ_API_KEY : API key for authentication with GROQ.
- MODEL        : (Optional) Model identifier to use. Defaults to "llama3-70b-8192".

Dependencies:
-------------
- requests
- os
"""

import os
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama3-70b-8192")


def summarize_resume(text: str) -> str:
    """
    Generates a concise summary of a single resume using an LLM.

    Args:
        text (str): Raw extracted text from a resume.

    Returns:
        str: Objective summary of the resume.
    """
    prompt = f"Resuma de forma objetiva o currículo abaixo:\n{text}"
    return call_groq(prompt)


def answer_query(resumes: list[str], query: str) -> str:
    """
    Analyzes multiple resumes and answers a recruitment-related query.

    The LLM evaluates the content of each resume and determines which one
    best fits the given question, providing a justification.

    Args:
        resumes (list[str]): List of resume texts.
        query (str): Recruitment or selection-related question.

    Returns:
        str: AI-generated answer with justification.
    """
    joined = "\n---\n".join([f"Currículo {i+1}:\n{r}" for i, r in enumerate(resumes)])
    prompt = f"""Considere os currículos a seguir:
{joined}
Pergunta: {query}
Analise e responda qual currículo atende melhor, justificando a resposta de forma técnica.
"""
    return call_groq(prompt)


def call_groq(prompt: str) -> str:
    """
    Sends a prompt to the GROQ API and returns the model's response.

    Args:
        prompt (str): The prompt to send to the language model.

    Returns:
        str: Content of the generated response from the model.

    Raises:
        requests.HTTPError: If the API call fails.
    """
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Você é um especialista em recrutamento técnico."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 700,
        "temperature": 0.2
    }
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    resp = requests.post(GROQ_API_URL, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']
