import logging
from extraction import validation_pipeline
from intelligence import resume_field_identification
from database import save_resume
from config import AWS_S3_BUCKET

logger = logging.getLogger(__name__)

class Processor:
    def __init__(self):
        self.bucket_name = AWS_S3_BUCKET
    
    def pipeline(self, filename: str, file_bytes: bytes) -> dict:
        try:
            # 0. Validation and extraction pipeline 
            extracted_resume_data = validation_pipeline(filename, file_bytes, bucket_name=self.bucket_name)
            
            # 1. Identification of fields
            raw_text = extracted_resume_data.get("text", "")
            identified_fields = resume_field_identification(raw_text)
            
            # 2. Save to database
            file_size = len(file_bytes)
            resume_id = save_resume(identified_fields, filename, file_size)
            
            # 2.1. Return identified fields with database ID
            identified_fields["resume_id"] = resume_id
            logger.info(f"Resume processed and saved with ID: {resume_id}")
            
            return identified_fields
            
        except Exception as e:
            logger.error(f"Processing pipeline failed: {e}")
            return {"error": f"Processing failed: {str(e)}"}
