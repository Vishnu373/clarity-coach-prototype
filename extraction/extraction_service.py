import os
from io import BytesIO
from pdfminer.high_level import extract_text as extract_pdf_text
from .digital_pdf_extractor import DigitalPDFPipeline
from .scanned_pdf_extractor import ScannedPdfPipeline
from .word_docx_extractor import WordDocxPipeline
from .text_txt_extractor import TxtPipeline
from config import SUPPORTED_FILE_EXTENSIONS

SUPPORTED_EXTENSIONS = SUPPORTED_FILE_EXTENSIONS

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[-1].lower()

def validate_file(filename: str, file_bytes: bytes) -> dict:
    ext = get_file_extension(filename)

    if ext not in SUPPORTED_EXTENSIONS:
        return {
            "supported": False,
            "reason": f"Unsupported file type: {ext}",
            "file_type": ext,
            "is_digital_pdf": None
        }

    is_digital_pdf = None
    if ext == ".pdf":
        try:
            extracted_text = extract_pdf_text(BytesIO(file_bytes))
            is_digital_pdf = len(extracted_text.strip()) > 0
        except Exception:
            is_digital_pdf = False

    return {
        "supported": True,
        "file_type": ext,
        "is_digital_pdf": is_digital_pdf
    }

def process_file(filename: str, file_bytes: bytes, bucket_name: str = None) -> dict:
    validation = validate_file(filename, file_bytes)

    if not validation["supported"]:
        return {"error": validation["reason"]}

    ext = validation["file_type"]

    if ext == ".pdf":
        if validation["is_digital_pdf"]:
            pipeline = DigitalPDFPipeline(file_bytes)
        else:
            if not bucket_name:
                return {"error": "Bucket name is required for scanned PDFs"}
            pipeline = ScannedPdfPipeline(file_bytes, bucket_name=bucket_name)
    elif ext == ".docx":
        pipeline = WordDocxPipeline(file_bytes)
    elif ext == ".txt":
        pipeline = TxtPipeline(file_bytes)
    else:
        return {"error": f"No pipeline available for file type: {ext}"}

    extracted_data = pipeline.run_pipeline()
    
    return extracted_data
