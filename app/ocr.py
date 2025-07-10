"""
OCR Module

This module provides a utility to extract text from resume files using EasyOCR.
It supports both PDFs (converted to images) and image formats directly (e.g., PNG, JPG).

Dependencies:
-------------
- easyocr
- pdf2image
- tempfile
"""

import easyocr
from pdf2image import convert_from_bytes
import tempfile

# Initialize EasyOCR reader with Portuguese and English languages
reader = easyocr.Reader(['pt', 'en'], gpu=False)

def extract_text(file: bytes, filename: str) -> str:
    """
    Extracts text content from a file using OCR.

    Supports both PDF files (which are first converted into images)
    and standard image files (e.g., PNG, JPG, JPEG).

    Args:
        file (bytes): File content in bytes.
        filename (str): Name of the uploaded file (used to determine the file type).

    Returns:
        str: Extracted text from the file, combined into a single string.
    """
    if filename.lower().endswith('.pdf'):
        pages = convert_from_bytes(file)
        texts = []
        for page in pages:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as f:
                page.save(f.name, 'PNG')
                texts.append('\n'.join(reader.readtext(f.name, detail=0, paragraph=True)))
        return '\n'.join(texts)
    else:
        with tempfile.NamedTemporaryFile(suffix=filename[-4:], delete=True) as f:
            f.write(file)
            f.flush()
            return '\n'.join(reader.readtext(f.name, detail=0, paragraph=True))
