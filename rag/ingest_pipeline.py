from dotenv import load_dotenv
from rag.chunking import get_file, chunk_text
from rag.embedding import generate_embeddings
from rag.indexing import upsert_chunks

load_dotenv()

"""
Pipeline 1 (Offline - one time):
Load the knowledge base -> Chunking -> Embedding -> indexing
"""

# 0. Get the file
print("Starting")
kb_file = get_file()

# 1. Perform chunking
print("Chunking time")
kb_text = kb_file.read_text(encoding="utf-8", errors="ignore")
chunks = chunk_text(kb_text)

# 2. Generate embeddings
print("Embedding time")
embeddings = generate_embeddings(chunks)

# 3. Indexing
print("Indexing time")
upsert_chunks(embeddings)

print("Pipeline finished successfully")