from analysis_and_enhancement.restructuring import restructure_resume
from services.model_processor import process_with_model
from dotenv import load_dotenv
from rag.embedding import generate_embeddings
from rag.indexing import search_similar
from services.model_processor import get_rag_input
from rag.retrieve import retrieve_all_chunks
from rag.suggest import suggestions

def run_pipeline(extracted_data):
    # 1. Restructuring the resume
    restructured_data = restructure_resume(extracted_data)

    # 2. Process the resume
    _, rag_input, _ = process_with_model(restructured_data)

    # 3. RAG - Retrieve
    retrieved_results = retrieve_all_chunks(rag_input)

    # 4. RAG - Augment + Generate
    suggested_results = suggestions(retrieved_results)

    # 5. Deleting the files from S3
    # Code to be added later

    return suggested_results

