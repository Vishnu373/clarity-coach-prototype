import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict

from pathlib import Path
import os

def get_file() -> Path:
    path = Path(os.getenv("KB_PATH")).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Knowledge base file not found at: {path}")
    return path

def chunk_text(text: str, chunk_size: int = 256, chunk_overlap: int = 30) -> List[Dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)

    return [
        {"chunk_id": idx, "content": chunk}
        for idx, chunk in enumerate(chunks)
    ]



# kb_file = get_file()
# print(f"Using KB: {kb_file}")
# kb_text = kb_file.read_text(encoding="utf-8", errors="ignore")
# chunks = chunk_text(kb_text)
# print(f"Total chunks: {len(chunks)}")
# for c in chunks[:10]:
#     print(c)           


        