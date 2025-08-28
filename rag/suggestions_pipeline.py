from dotenv import load_dotenv
from rag.embedding import generate_embeddings
from rag.indexing import search_similar
from services.model_processor import get_rag_input
from rag.retrieve import retrieve_all_chunks
from rag.suggest import suggestions

def run_pipeline(data):
    retrieval_results = retrieve_all_chunks(data)
    suggestion_results = suggestions(retrieval_results)

    return suggestion_results


# Final output need to be plugged into main.py
data = get_rag_input()
print(run_pipeline(data))

# File to be deleted as everything is in ae pipeline.