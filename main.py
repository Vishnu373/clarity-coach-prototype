import streamlit as st
import os

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

upload_file = st.file_uploader("Upload a file: ", type = ["pdf", "docx", "txt"])

if upload_file:
    os.makedirs("data/raw", exist_ok=True)
    filepath = os.path.join("data/raw", upload_file.name)

    with open(filepath, "wb") as f:
        f.write(upload_file.read())
        
    st.success(f"Uploaded file: {upload_file.name}") 

    st.info("Extracting content...")
    extracted_text = "Here's your data extracted from the file"

    st.subheader("Final output: ")
    st.text_area("Output: ", extracted_text, height=300)
    
      