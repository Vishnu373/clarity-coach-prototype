from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
from utils.s3_client import S3Client
from config import S3_KNOWLEDGE_BASE_KEY, CHUNK_SIZE, CHUNK_OVERLAP

def get_file() -> str:
    """Download knowledge base file from S3"""
    s3 = S3Client()
    return s3.download_file(S3_KNOWLEDGE_BASE_KEY)

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Dict]:
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
