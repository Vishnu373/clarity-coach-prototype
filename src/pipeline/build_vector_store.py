import os
import json
import numpy as np
import faiss
from src.services.model_client import get_embedding

# 1. Load file
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
filepath = os.path.join(base_dir, "data", "knowledge_base.json")

with open(filepath, "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# 2. Chunking
knowledge_chunks = []
for entry in knowledge_base:
    chunk = f"""Role: {entry['role']}\nSkills: {', '.join(entry['skills'])}\nExample projects: {', '.join(entry['projects'])}"""
    knowledge_chunks.append(chunk.strip())

# 3. Embedding
embedding_vectors = []
for chunk in knowledge_chunks:
    embedding = get_embedding(chunk)
    embedding_vectors.append(embedding)

embedding_vectors = np.array(embedding_vectors).astype('float32')

# 4. Indexing
dimension = len(embedding_vectors[0])
index = faiss.IndexFlatL2(dimension)
index.add(embedding_vectors)

# 5. Saving the files
index_path = os.path.join(base_dir, "data", "faiss_index.index")
meta_path = os.path.join(base_dir, "data", "chunk_metadata.json")

faiss.write_index(index, index_path)

with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(knowledge_chunks, f, ensure_ascii=False, indent=2)

print("FAISS index and chunk metadata saved.")
