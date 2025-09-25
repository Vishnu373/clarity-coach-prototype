"""
Extraction package for processing various document formats.

This package handles:
- PDF extraction (digital and scanned)
- Word document extraction  
- Text file extraction
- Text preprocessing
- Main extraction service orchestration
"""

from .extraction_service import process_file, validate_file
from .preprocessing import preprocess_text
from .digital_pdf_extractor import DigitalPDFPipeline
from .scanned_pdf_extractor import ScannedPdfPipeline
from .word_docx_extractor import WordDocxPipeline
from .text_txt_extractor import TxtPipeline

__all__ = [
    'process_file',
    'validate_file', 
    'preprocess_text',
    'DigitalPDFPipeline',
    'ScannedPdfPipeline',
    'WordDocxPipeline',
    'TxtPipeline'
]