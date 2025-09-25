"""Ingestion pipeline for processing knowledge base into vector embeddings.
This is a one-time process to prepare the knowledge base for RAG."""

from rag.chunking import get_file, chunk_text
from rag.embedding import generate_embeddings
from rag.indexing import upsert_chunks


def run_ing_pipeline():
    # 0. Get the file from S3
    kb_text = get_file()

    # 1. Perform chunking
    chunks = chunk_text(kb_text)

    # 2. Generate embeddings
    embeddings = generate_embeddings(chunks)

    # 3. Indexing
    upsert_chunks(embeddings)
