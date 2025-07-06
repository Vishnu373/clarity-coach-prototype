from src.preprocessing.cleaning import preprocess_text

class TxtPipeline:
    def __init__(self, filepath):
        self.filepath = filepath
        self.raw_text = ""

    def extract_text(self):
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as file:
            self.raw_text = file.read()
        return self.raw_text

    def run_pipeline(self):
        raw_text = self.extract_text()
        cleaned_text = preprocess_text(raw_text)  
        
        return {"text": cleaned_text}    
