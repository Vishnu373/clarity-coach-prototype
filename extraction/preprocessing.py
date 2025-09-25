import re

def preprocess_text(text: str) -> str:
    if isinstance(text, list):
        text = "\n".join(text)
        
    text = re.sub(r'[•·●▪▶►*]', '-', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'[-=]{2,}', '-', text)
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()
