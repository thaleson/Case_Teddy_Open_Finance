# 🚀 TalentAI - Análise Inteligente de Currículos (OCR + LLM)

> Uma aplicação full-stack que automatiza a extração de texto (OCR) e análise semântica (LLM) de currículos para selecionar o melhor candidato.

---

## 📋 Visão Geral

O **TalentAI** recebe múltiplos arquivos (PDF/JPG/PNG), extrai texto via OCR, gera resumos e responde a queries de recrutamento através de uma API FastAPI + LLM (Groq). O front-end é em Streamlit. Todos os eventos são registrados em MongoDB (logs apenas, sem armazenar documentos completos). 👩‍💻👨‍💻

### Principais Componentes

- 🐍 **Python 3.11** (FastAPI, Streamlit, EasyOCR, requests)
- 🌐 **FastAPI** ➡️ API REST (`/analyze/`)
- 🔍 **EasyOCR** (`tesseract-ocr`, `poppler-utils`) para extração de texto
- 🤖 **LLM (Groq)** para sumarização e análise comparativa
- 📊 **Streamlit** para interface web
- 📦 **MongoDB** (logs de uso) via Docker
- 🐳 **Docker Compose** para orquestração dos containers

---

## 📦 Estrutura do Projeto

```plaintext
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
├── requirements.txt
├── app/
│   ├── api.py
│   ├── ocr.py
│   ├── llm.py
│   ├── storage.py
│   └── models.py
└── main.py          # Streamlit UI
```

---

## ⚙️ Pré-requisitos

| SO      | Instalação do Docker + Compose                                                                                    |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| Linux   | `sudo apt install docker-ce docker-compose-plugin`                                                                |
| Windows | Docker Desktop ([https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)) |
| macOS   | Docker Desktop                                                                                                    |

> 🔑 **Crie um arquivo** `.env` na raiz:
>
> ```dotenv
> GROQ_API_KEY=seu_token_aqui
> MODEL=llama3-70b-8192
> MONGO_URI=mongodb://mongo:27017
> ```

---

## 🚀 Como Executar (Linux / macOS / Windows)

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seu-usuario/talentai.git
   cd talentai
   ```

2. **Configure as variáveis de ambiente**:

   - Crie/edite `.env` (veja seção acima) 🔒

3. **Suba os containers**:

   ```bash
   # Build + start em segundo plano
   docker compose up -d --build
   ```

4. **Verifique**:

   ```bash
   docker compose ps
   ```

   Você deve ver 3 serviços `Up`: `api`, `streamlit`, `mongo`.

5. **Acesse a aplicação**:

   - Swagger/API:  👉 [http://localhost:8000/docs](http://localhost:8000/docs)
   - Streamlit UI: 👉 [http://localhost:8501](http://localhost:8501)

6. **Logs em tempo real** (opcional):

   ```bash
   docker compose logs -f api
   docker compose logs -f streamlit
   docker compose logs -f mongo
   ```

7. **Parar / Remover**:

   ```bash
   docker compose down -v
   ```

---

## 🔄 Persistência após Reinicialização

❓ **Preciso rodar o Docker toda vez?**

- Sempre que reiniciar a máquina, **os containers param**. Para reativar, basta rodar:
  ```bash
  docker compose up -d   # inicia containers já construídos
  ```
- Se não houve mudança no código, **não é necessário rebuildar** (`--build`).
- Para reiniciar containers parados:
  ```bash
  docker compose start
  ```

---

## ❓ Dúvidas Frequentes

- **Como atualizar dependências?**

  1. Atualize `requirements.txt`.
  2. Rode `docker compose build --no-cache`.

- **Como mudar o modelo LLM?**

  - Ajuste a variável `MODEL` no `.env`.

- **Como alterar o endpoint?**

  - O nome do serviço API no Compose é `api`. Internamente, a UI chama `http://api:8000/analyze/`.

---


