from dotenv import load_dotenv
from rag.embedding import generate_embeddings
from rag.indexing import search_similar
from rag.generation import generate_suggestions

load_dotenv()

"""
Pipeline 2: (RAG)
1. Retrieve (the similar jobs roles/responsibilities found from knowledge base)
2. Augment (the required resume data passed)
3. Generate (suggest 10 projects/reponsibilities for each role by combining retrieved data + LLM call)
"""

user_role = "AI Engineer at Ilore AI"
user_skills = ["Python", "LangChain", "RAG"]

# Step 1: Build query embedding
query_text = "AI Engineer with Python, LangChain, RAG"
query_embedding = generate_embeddings([{"chunk_id": 0, "content": query_text}])[0]["embedding"]

# Step 2: Retrieve chunks from KB
chunks = search_similar(query_embedding, top_k=5)

# Step 3: Generate suggestions
suggestions = generate_suggestions(user_role, user_skills, chunks)

print("💡 Suggested Resume Bullets:")
print(suggestions)