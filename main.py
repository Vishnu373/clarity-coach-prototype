import streamlit as st
import json
from services.processor import Processor

# Page configuration
st.set_page_config("Clarity Coach", layout='centered')
st.title("Clarity Coach")
st.write("Upload your resume")

# File upload
uploaded_file = st.file_uploader(
    "Choose a resume file:", 
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, Word Document, Text file"
)

# Process uploaded file
if uploaded_file:
    st.write("Processing file...")
    
    # Read file bytes
    file_bytes = uploaded_file.read()
    
    processor = Processor()
    result = processor.pipeline(uploaded_file.name, file_bytes)
    
    # Display results
    if "error" in result:
        st.error(f"Error: {result['error']}")
    else:
        st.success("Resume processed successfully!")
        
        # Display identified fields
        st.subheader("Identified Resume Fields")
        st.json(result)
    