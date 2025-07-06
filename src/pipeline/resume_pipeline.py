from src.extraction.digital_pdf_pipeline import DigitalPDFPipeline
from src.extraction.word_docx_pipeline import WordDocxPipeline
from src.extraction.text_txt_pipeline import TxtPipeline
from src.extraction.scanned_pdf_pipeline import ScannedPdfPipeline
from src.services.model_client import model
from src.prompts import structure_filter_prompt

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
    
    # Gets extracted data
    extracted_data = pipeline.run_pipeline()

    # Extracted data in a structured format by gpt
    structured_data = model(structure_filter_prompt, extracted_data)

    return structured_data