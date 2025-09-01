from io import BytesIO
from services.preprocessing import preprocess_text

class TxtPipeline:
    def __init__(self, file_bytes: bytes):
        self.file_bytes = file_bytes
        self.raw_text = ""

    def extract_text(self):
        self.raw_text = self.file_bytes.decode('utf-8', errors='ignore')
        return self.raw_text

    def run_pipeline(self):
        raw_text = self.extract_text()
        cleaned_text = preprocess_text(raw_text)
        return {"text": cleaned_text}
