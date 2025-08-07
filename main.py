import streamlit as st

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

upload_file = st.file_uploader("Upload a file:", type=["pdf", "docx", "txt"])