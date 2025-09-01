from dotenv import load_dotenv
from rag.embedding import generate_embeddings
from rag.indexing import search_similar
from services.model_processor import get_rag_input
from rag.retrieve import retrieve_all_chunks
from rag.suggest import suggestions
from rag.chunking import get_file, chunk_text
from rag.embedding import generate_embeddings
from rag.indexing import upsert_chunks


def run_pipeline():
    # 0. Get the file from S3
    kb_text = get_file()

    # 1. Perform chunking
    chunks = chunk_text(kb_text)

    # 2. Generate embeddings
    embeddings = generate_embeddings(chunks)

    # 3. Indexing
    upsert_chunks(embeddings)
