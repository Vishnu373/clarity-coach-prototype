import streamlit as st
from services.extraction_service import process_file
from dotenv import load_dotenv
import os
from pipelines.ae_pipeline import run_pipeline

load_dotenv()
BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

uploaded_file = st.file_uploader("Upload a file:", type=["pdf", "docx", "txt"])

if uploaded_file:
    results = run_pipeline(uploaded_file)
    st.json(results)