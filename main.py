import streamlit as st
from services.extraction_service import process_file
from config import AWS_BUCKET_NAME

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

uploaded_file = st.file_uploader("Upload a file:", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    result = process_file(uploaded_file.name, file_bytes, bucket_name=AWS_BUCKET_NAME)
    st.write(result)