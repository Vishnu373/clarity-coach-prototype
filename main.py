import streamlit as st
from services.main_processor import MainProcessor

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
    
    processor = MainProcessor()
    result = processor.process_resume(uploaded_file.name, file_bytes)
    status = processor.get_processing_status(result)
    
    # Display status
    if status["success"]:
        st.success(status["message"])
        st.info(f"{status['validation_reason']}")
        
        # Show extracted content
        st.subheader("Extracted Text:")
        st.text_area(
            "Content", 
            result.get("text", ""), 
            height=300,
            help="This is the text extracted from your resume"
        )
        
        # Show file info
        st.subheader("File Information:")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("File Size", f"{result['file_size']} bytes")
        with col2:
            st.metric("Word Count", len(result.get("text", "").split()))
        
        # Show tables if extracted
        if "tables" in result and result["tables"]:
            st.subheader("Tables Found:")
            for i, table in enumerate(result["tables"]):
                with st.expander(f"Table {i+1}"):
                    st.write(table)
    else:
        st.error(status["message"])
    