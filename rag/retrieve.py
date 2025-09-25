# retrieve.py
from utils.model_client import embedding_model
from rag.indexing import search_similar

"""
Get the matching job roles and responbilites/projects for each user's experience from the knowledge base.
"""
def retrieve_all_chunks(data, top_k=None):
    """Retrieve matching chunks for each experience using RAG"""
    from config import TOP_K_RETRIEVAL
    if top_k is None:
        top_k = TOP_K_RETRIEVAL
    retrieval_results = []
    
    for exp in data['experience']:
        role = exp['role']
        skills = exp['skills'].split(', ')
        query = f"{role} with {', '.join(skills)}"
        
        qvec = embedding_model(query)
        results = search_similar(qvec, top_k=top_k)
        
        retrieval_results.append({
            'role': role,
            'query': query,
            'results': results
        })
        
    return retrieval_results
    
