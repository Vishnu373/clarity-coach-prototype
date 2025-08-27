import streamlit as st
from services.extraction_service import process_file
from dotenv import load_dotenv
import os
from services.model_processor import process_with_model
from services.model_client import gpt_model
from services.prompts import RESTRUCTURE_RESUME_PROMPT

import json

load_dotenv()
BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

uploaded_file = st.file_uploader("Upload a file:", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_bytes = uploaded_file.read()

    extracted_data = process_file(uploaded_file.name, file_bytes, bucket_name=BUCKET_NAME)

    if "error" in extracted_data:
        st.error(extracted_data["error"])
    
    else:
        try:
            processed_data, _, _ = process_with_model(extracted_data)
            st.json(processed_data)

        except Exception as e:
            st.error(f"Error processing with model: {e}")