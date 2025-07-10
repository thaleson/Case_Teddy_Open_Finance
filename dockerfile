FROM python:3.11-slim

# 1) Instala libs de sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      poppler-utils \
      tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

# 2) Cria pasta de trabalho e instala requisitos em /usr/local
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copia o restante do código
COPY . .

# 4) Cria usuário não-root e ajusta perms
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# 5) =========== as from aqui é under appuser ============
USER appuser

# Garante que ~.local/bin esteja no PATH (para console-scripts)
ENV PATH="/home/appuser/.local/bin:${PATH}"

# 6) Expõe portas
EXPOSE 8000 8501

# 7) Comando default (pode ser sobrescrito pelo Compose)
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
