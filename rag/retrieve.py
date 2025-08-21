from dotenv import load_dotenv
from rag.embedding import generate_embeddings
from rag.indexing import search_similar

load_dotenv()

# Example query
query = "Web developer"

# 1. Embed the query
query_embedding = generate_embeddings([{"chunk_id": 0, "content": query}])[0]["embedding"]

# 2. Search in Supabase
results = search_similar(query_embedding, top_k=3)

print("Results:")
for r in results:
    print(f"- {r['content']} (similarity={r['similarity']:.3f})")
