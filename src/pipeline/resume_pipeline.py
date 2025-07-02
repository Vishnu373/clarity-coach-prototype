from src.extraction.digital_pdf_pipeline import DigitalPDFPipeline
from src.extraction.word_docx_pipeline import WordDocxPipeline
from src.extraction.text_txt_pipeline import TxtPipeline
from src.extraction.scanned_pdf_pipeline import ScannedPdfPipeline

def run_resume_pipeline(filepath, validation_result):
    file_type = validation_result["file_type"]

    if file_type == ".pdf":
        if validation_result.get("is_digital_pdf"):
            pipeline = DigitalPDFPipeline(filepath)
            
        else:
            pipeline = ScannedPdfPipeline(filepath)

    elif file_type == ".docx":
        pipeline = WordDocxPipeline(filepath)

    elif file_type == ".txt":
        pipeline = TxtPipeline(filepath)

    else:
        return None

    return pipeline.run_pipeline()
