import os
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

RESUME_KEYWORDS = {"experience", "education", "skills", "summary", "projects"}

def get_file_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[-1].lower()

def is_supported(file_path: str) -> bool:
    ext = get_file_extension(file_path)
    return ext in SUPPORTED_EXTENSIONS

def is_resume(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in RESUME_KEYWORDS)

def extract_text(file_path: str) -> str:
    ext = get_file_extension(file_path)
    try:
        if ext == ".pdf":
            return extract_pdf_text(file_path) or ""
        elif ext == ".docx":
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs]) or ""
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read() or ""
    except Exception:
        return ""
    return ""

"""
    Validate the uploaded file:
    - Check if file type is supported
    - Perform minimal text extraction
    - For PDFs, determine if scanned or digital based on extracted text presence
    - Check if extracted text appears to be a resume
 """
def validate_file(file_path: str) -> dict:
    ext = get_file_extension(file_path)

    if ext not in SUPPORTED_EXTENSIONS:
        return {
            "supported": False,
            "reason": f"Unsupported file type: {ext}",
            "extracted_text": ""
        }

    extracted_text = extract_text(file_path)
    is_resume_file = is_resume(extracted_text)

    is_digital_pdf = None
    if ext == ".pdf":
        is_digital_pdf = len(extracted_text.strip()) > 0

    return {
        "supported": True,
        "file_type": ext,
        "is_digital_pdf": is_digital_pdf,
        "is_resume": is_resume_file,
        "extracted_text": extracted_text
    }