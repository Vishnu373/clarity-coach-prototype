import streamlit as st
import os
from src.validation import validate_file
from src.extraction import DigitalPDFPipeline

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

    # elif not validation_result["is_resume"]:
    #     st.warning("The uploaded file does not appear to be a resume.")

    elif validation_result["file_type"] == ".pdf" and validation_result["is_digital_pdf"]:
        st.info("Running Digital PDF Extraction Pipeline...")

        pipeline = DigitalPDFPipeline(filepath)
        result = pipeline.run_pipeline()

        st.subheader("Cleaned Text Output")
        st.text_area("Resume Text", result["text"], height=300)

        if result.get("tables"):
            st.subheader("Extracted Tables")
            for idx, table in enumerate(result["tables"]):
                st.write(f"Table {idx + 1}")
                st.write(table)

    # else:
    #     st.info("Extracted preview of your file content:")
    #     st.text_area("Extracted Text", validation_result["extracted_text"], height=300)
