# retrieve.py
from services.model_client import embedding_model
from rag.indexing import search_similar
from services.model_processor import get_rag_input, get_market_intelligence_input, get_processed_data

"""
Get the matching job roles and responbilites/projects for each user's experience from the knowledge base.
"""
def retrieve_chunks(exp, top_k=50):
    role = exp["role"].strip()
    skills = [s.strip() for s in exp.get("skills", [])][:5]
    query = f"{role} with {', '.join(skills)}" if skills else role

    qvec = embedding_model(query)
    results = search_similar(qvec, top_k=top_k)

    return results

rag_input = get_rag_input()

print(get_processed_data())
