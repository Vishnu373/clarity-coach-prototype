import streamlit as st
import os
from src.validation import validate_file

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

upload_file = st.file_uploader("Upload a file: ", type = ["pdf", "docx", "txt"])

if upload_file:
    os.makedirs("data/raw", exist_ok=True)
    filepath = os.path.join("data/raw", upload_file.name)

    with open(filepath, "wb") as f:
        f.write(upload_file.read())
        
    st.success(f"Uploaded file: {upload_file.name}") 

    validation_result = validate_file(filepath)

    if not validation_result["supported"]:
        st.error(f"Unsupported file type: {validation_result.get('reason', '')}")

    elif not validation_result["is_resume"]:
        st.warning("The uploaded file does not appear to be a resume.")

    else:
        st.info("Extracted preview of your file content:")
        st.text_area("Extracted Text", validation_result["extracted_text"], height=300)

