import os
import json
import faiss
import numpy as np
from src.services.model_client import get_embedding, model

class RAGPipeline:
    def __init__(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))

        # Load FAISS index
        index_path = os.path.join(base_path, "faiss_index.index")
        self.index = faiss.read_index(index_path)

        # Load chunk metadata
        chunk_path = os.path.join(base_path, "chunk_metadata.json")
        with open(chunk_path, "r", encoding="utf-8") as f:
            self.knowledge_chunks = json.load(f)
        
    # 1. Retrieval    
    def retrieve(self, query_text, top_k=5):
        query_embedding = get_embedding(query_text)
        query_vector = np.array(query_embedding).astype("float32").reshape(1, -1)
        distances, indices = self.index.search(query_vector, top_k)
        retrieved_data = [self.knowledge_chunks[i] for i in indices[0]]

        return retrieved_data

    # 2, 3. Augmented and Generation
    def augment_and_generate(self, extracted_data, retrieved_chunks):
        context = "\n\n".join(retrieved_chunks)
        prompt = f"""
        Given the resume data:\n{extracted_data}\n\n
        And these relevant job details:\n{context}\n\n
        Suggest 10 additional projects this candidate might have done at each job role.
        """
        generated_result = model(prompt_template=prompt, text = "").strip()

        return generated_result

    def run_rag_pipeline(self, extracted_resume_text):
        result = self.retrieve(extracted_resume_text)
        result = self.augment_and_generate(extracted_resume_text, result)

        return result
