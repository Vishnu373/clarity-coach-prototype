from services.restructuring import restructure_resume
from services.model_processor import file_processing
from dotenv import load_dotenv
from rag.embedding import generate_embeddings
from rag.indexing import search_similar
from rag.retrieve import retrieve_all_chunks
from rag.suggest import suggestions
from utils.s3_client import S3Client
import os
from services.extraction_service import process_file

load_dotenv()
BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

def run_pipeline(uploaded_file):
    # 0. Get the uploaded file
    file_bytes = uploaded_file.read()

    # 1. Extracted the resume
    extracted_data = process_file(uploaded_file.name, file_bytes, bucket_name=BUCKET_NAME)

    # 2. Restructuring the resume
    restructured_data = restructure_resume(extracted_data)

    # 3. Preparing it for RAG
    rag_input, _ = file_processing(restructured_data)

    # 4. RAG - Retrieve
    retrieved_results = retrieve_all_chunks(rag_input)

    # 5. RAG - Augment + Generate
    suggested_results = suggestions(retrieved_results)

    # 6. Delete the input files from S3
    S3Client().delete_file("rag_input.json")

    return suggested_results

