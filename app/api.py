"""
TalentAI API

This API provides intelligent resume analysis by combining OCR (Optical Character Recognition)
and LLM (Large Language Models). It supports uploading resumes in PDF, JPG, or PNG format,
extracts the text, and either summarizes the content or answers specific recruitment-related queries.

Main Endpoint:
--------------
POST /analyze/ : Accepts multiple resume files and returns either summaries or answers based on a user-provided query.

Modules:
--------
- app.ocr: Contains `extract_text` function to process OCR.
- app.llm: Contains `summarize_resume` and `answer_query` functions for LLM processing.
- app.storage: Handles logging via the `log_request` function.
"""

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from app.ocr import extract_text
from app.llm import summarize_resume, answer_query
from app.storage import log_request
import uuid
import datetime

app = FastAPI(
    title="TalentAI API",
    description="API for intelligent resume analysis (OCR + LLM)",
    version="1.0.0"
)

class LogSchema(BaseModel):
    """
    Schema used to log analysis requests.

    Attributes:
        request_id (str): Unique identifier of the request.
        user_id (str): Identifier of the user making the request.
        timestamp (str): Timestamp of the request in UTC.
        query (str): Optional recruitment-related question provided by the user.
        result (str): Result returned by the analysis (summaries or answer).
    """
    request_id: str
    user_id: str
    timestamp: str
    query: str
    result: str

@app.post("/analyze/", summary="Analisa e sumariza currículos")
async def analyze(
    files: list[UploadFile] = File(..., description="Lista de arquivos PDF/JPG/PNG"),
    query: str = Form(None, description="Query de recrutamento, se desejado"),
    request_id: str = Form(..., description="UUID da requisição"),
    user_id: str = Form(..., description="Identificador do solicitante")
):
  
    """
    Analyze resumes using OCR and LLM for summarization or question answering.

    This endpoint accepts one or more resume files and performs text extraction using OCR.
    If a query is provided, the system uses an LLM to generate an answer based on the resume content.
    If no query is provided, it returns a summary for each resume.

    Args:
        files (list[UploadFile]): List of uploaded files in PDF, JPG, or PNG format.
        query (str, optional): Optional query for candidate analysis.
        request_id (str): Unique identifier for the request.
        user_id (str): Identifier of the user making the request.

    Returns:
        dict: A dictionary containing either summaries of the resumes or an answer to the query.
    """
    resumes_text = []
    for file in files:
        file_bytes = await file.read()
        text = extract_text(file_bytes, file.filename)
        resumes_text.append(text)

    if not query:
        summaries = [summarize_resume(rt) for rt in resumes_text]
        result = {"summaries": summaries}
    else:
        answer = answer_query(resumes_text, query)
        result = {"answer": answer}

    log = LogSchema(
        request_id=request_id,
        user_id=user_id,
        timestamp=str(datetime.datetime.utcnow()),
        query=query,
        result=str(result)
    )
    log_request(log.model_dump())
    return result
