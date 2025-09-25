import streamlit as st
from pipelines import run_pipeline
from extraction import process_file
from services.restructuring import restructure_resume
from config import AWS_S3_BUCKET

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

uploaded_file = st.file_uploader("Upload a file:", type=["pdf", "docx", "txt"])

if uploaded_file:
    st.write("File uploaded. Processing...")

    file_bytes = uploaded_file.read()
    extracted_data = process_file(uploaded_file.name, file_bytes, bucket_name=AWS_S3_BUCKET)
    restructured_data = restructure_resume(extracted_data)

    st.write("Running Strategic Enhancement...")
    results_ae = run_pipeline("analysis")
    st.subheader("Strategic Enhancement Results")
    st.json(results_ae)

    st.write("Running Market Intelligence...")
    st.subheader("Assessment Results")
    run_pipeline("assessment")
    