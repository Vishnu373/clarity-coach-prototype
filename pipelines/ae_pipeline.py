"""Analysis Enhancement pipeline for resume processing and suggestions"""

from services.model_processor import file_processing
from rag.retrieve import retrieve_all_chunks
from rag.suggest import suggestions
from utils.s3_client import S3Client
from services.restructuring import get_restructured_data
from config import S3_RAG_INPUT_KEY

def run_ae_pipeline():
    """Run the Analysis Enhancement pipeline"""
    # Get restructured data from S3 
    restructured_data = get_restructured_data()

    # 3. Preparing it for RAG
    rag_input, _ = file_processing(restructured_data)

    # 4. RAG - Retrieve
    retrieved_results = retrieve_all_chunks(rag_input)

    # 5. RAG - Augment + Generate
    suggested_results = suggestions(retrieved_results)

    # 6. Delete the input files from S3
    S3Client().delete_file(S3_RAG_INPUT_KEY)

    return suggested_results

