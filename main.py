import streamlit as st
from config import AWS_BUCKET_NAME, AWS_REGION
from services.s3_client import S3Client

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

s3_client = S3Client(region=AWS_REGION, bucket_name=AWS_BUCKET_NAME)

uploaded_file = st.file_uploader("Upload a file:", type=["pdf", "docx", "txt"])

if uploaded_file:
    object_key = uploaded_file.name
    s3_client.upload_file(uploaded_file, object_key)
    st.success(f"File '{object_key}' uploaded to S3 bucket '{AWS_BUCKET_NAME}'.")
