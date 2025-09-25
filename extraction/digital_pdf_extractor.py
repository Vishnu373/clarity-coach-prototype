import pdfplumber
from io import BytesIO
from .preprocessing import preprocess_text

class DigitalPDFPipeline:
    def __init__(self, file_bytes: bytes):
        self.file_bytes = file_bytes

    def extract_text(self):
        try:
            with pdfplumber.open(BytesIO(self.file_bytes)) as pdf:
                text_parts = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                return '\n'.join(text_parts)
        except Exception as e:
            print(f"PDF text extraction failed: {e}")
            return ""

    def extract_tables(self):
        try:
            with pdfplumber.open(BytesIO(self.file_bytes)) as pdf:
                all_tables = []
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
                return all_tables
        except Exception as e:
            print(f"Table extraction failed: {e}")
            return []

    def run_pipeline(self):
        raw_text = self.extract_text()
        cleaned_text = preprocess_text(raw_text)
        
        result = {"text": cleaned_text}
        
        tables = self.extract_tables()
        if tables:
            result["tables"] = tables
            
        return result
