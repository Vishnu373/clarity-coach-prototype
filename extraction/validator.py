import os
import re
from io import BytesIO
from pdfminer.high_level import extract_text as extract_pdf_text
from .digital_pdf_extractor import DigitalPDFPipeline
from .scanned_pdf_extractor import ScannedPdfPipeline
from .word_extractor import WordPipeline
from .text_extractor import TextPipeline
from config import SUPPORTED_FILE_EXTENSIONS

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[-1].lower()

def validate_file_extension(filename: str) -> bool:
    ext = get_file_extension(filename)
    return ext in SUPPORTED_FILE_EXTENSIONS

def is_digital_pdf(file_bytes: bytes) -> bool:
    try:
        extracted_text = extract_pdf_text(BytesIO(file_bytes))
        return len(extracted_text.strip()) > 0
    except Exception:
        return False

def validation_pipeline(filename: str, file_bytes: bytes, bucket_name: str = None) -> dict:
    # Step 1: File extension validation
    if not validate_file_extension(filename):
        return {"error": f"Unsupported file type: {get_file_extension(filename)}"}
    
    # Step 2: Route to appropriate pipeline based on extension
    ext = get_file_extension(filename)
    
    if ext == ".pdf":
        if is_digital_pdf(file_bytes):
            pipeline = DigitalPDFPipeline(file_bytes)
        else:
            if not bucket_name:
                return {"error": "Bucket name required for scanned PDFs"}
            pipeline = ScannedPdfPipeline(file_bytes, bucket_name=bucket_name)
    elif ext == ".docx":
        pipeline = WordPipeline(file_bytes)
    elif ext == ".txt":
        pipeline = TextPipeline(file_bytes)
    else:
        return {"error": "Invalid file"}
    
    # Step 3: Extract content
    extracted_data = pipeline.run_pipeline()
    
    return extracted_data
