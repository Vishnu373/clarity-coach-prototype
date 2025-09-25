from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def upsert_chunks(chunks_with_embeddings):
    rows = []
    for c in chunks_with_embeddings:
        rows.append({
            "content": c["content"],
            "embedding": c["embedding"],
            "role": c.get("role"),
            "skills": c.get("skills", []),
            "source": c.get("source"),
        })

    supabase.table("job_chunks").insert(rows).execute()

# Vector search
def search_similar(query_embedding, top_k=3):
    """
    query_embedding: list[float] (same dim as stored embeddings)
    """
    response = supabase.rpc(
        "match_job_chunks",
        {"query_embedding": query_embedding, "match_count": top_k}
    ).execute()

    return response.data
