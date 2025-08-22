# retrieve.py
from services.model_client import embedding_model
from rag.indexing import search_similar
from services.model_processor import get_rag_input

"""
Get the matching job roles and responbilites/projects for each user's experience from the knowledge base.
"""
def retrieve_all_chunks(data, top_k=3):
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
    
