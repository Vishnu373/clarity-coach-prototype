from services.model_client import embedding_model

def generate_embeddings(chunks):
    results = []
    for chunk in chunks:
        embedding = embedding_model(chunk["content"])
        results.append({
            "chunk_id": chunk["chunk_id"],
            "content": chunk["content"],
            "embedding": embedding
        })
    
    return results
