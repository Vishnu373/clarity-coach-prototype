import streamlit as st
import os
from src.validation import validate_file
from src.pipeline.resume_pipeline import run_resume_pipeline

st.set_page_config("Clarity Coach Prototype", layout='centered')
st.title("Clarity Coach Prototype")

upload_file = st.file_uploader("Upload a file:", type=["pdf", "docx", "txt"])

if upload_file:
    os.makedirs("data/raw", exist_ok=True)
    filepath = os.path.join("data/raw", upload_file.name)

    with open(filepath, "wb") as f:
        f.write(upload_file.read())

    st.success(f"Uploaded file: {upload_file.name}")

    validation_result = validate_file(filepath)

    if not validation_result["supported"]:
        st.error(f"Unsupported file type: {validation_result.get('reason', '')}")
    else:
        st.info("Running appropriate extraction pipeline...")
        result = run_resume_pipeline(filepath, validation_result)

        if result:
            st.subheader("Cleaned Text Output")
            st.text_area("Resume Text", result.get("text", ""), height=300)

            if result.get("tables"):
                st.subheader("Extracted Tables")
                for idx, table in enumerate(result["tables"]):
                    st.write(f"Table {idx + 1}")
                    st.write(table)
