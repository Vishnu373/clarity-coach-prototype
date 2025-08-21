from supabase import create_client
import os

# get URL + anon/service key from Supabase dashboard
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    print(f"Inserted {len(rows)} chunks into Supabase.")

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
