import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
from utils.s3_client import S3Client
from pathlib import Path
import os

def get_file() -> str:
    bucket_name = os.getenv("AWS_S3_BUCKET")
    key = "knowledge_base.txt"
    s3 = S3Client(bucket_name)

    return s3.download_file(key)

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
