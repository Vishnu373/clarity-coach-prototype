from io import BytesIO
from docx import Document
from .preprocessing import preprocess_text

class WordPipeline:
    def __init__(self, file_bytes: bytes):
        self.file_bytes = file_bytes

    def extract_text(self):
        try:
            doc = Document(BytesIO(self.file_bytes))
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            return '\n'.join(paragraphs)
        except Exception as e:
            print(f"Word text extraction failed: {e}")
            return ""

    def extract_tables(self):
        try:
            doc = Document(BytesIO(self.file_bytes))
            tables = []
            for table in doc.tables:
                table_data = []
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells]
                    table_data.append(row_data)
                if table_data:  # Only add non-empty tables
                    tables.append(table_data)
            return tables
        except Exception as e:
            print(f"Word table extraction failed: {e}")
            return []

    def run_pipeline(self):
        raw_text = self.extract_text()
        cleaned_text = preprocess_text(raw_text)
        
        result = {"text": cleaned_text}
        
        tables = self.extract_tables()
        if tables:
            result["tables"] = tables
            
        return result
