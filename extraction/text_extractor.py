from .preprocessing import preprocess_text

class TextPipeline:
    def __init__(self, file_bytes: bytes):
        self.file_bytes = file_bytes

    def extract_text(self):
        try:
            return self.file_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Text extraction failed: {e}")
            return ""

    def run_pipeline(self):
        raw_text = self.extract_text()
        cleaned_text = preprocess_text(raw_text)
        return {"text": cleaned_text}
