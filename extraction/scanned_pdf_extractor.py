import logging
from io import BytesIO
from utils.s3_client import upload_file, delete_file, get_bucket
from utils.textract_client import TextractClient
from .preprocessing import preprocess_text

# Configure logging
logger = logging.getLogger(__name__)

class ScannedPdfPipeline:
    def __init__(self, file_bytes: bytes, bucket_name: str = None, region: str = "us-east-1"):
        self.file_bytes = file_bytes
        self.bucket_name = bucket_name or get_bucket()
        self.textract_client = TextractClient(region=region)

    def run_pipeline(self):
        object_name = None
        try:
            # Upload file to S3
            logger.info("Uploading scanned PDF to S3 for Textract processing")
            object_name = upload_file(BytesIO(self.file_bytes))
            
            # Process with Textract
            logger.info(f"Processing document with Textract: {object_name}")
            textract_result = self.textract_client.detect_document_text(self.bucket_name, object_name)
            
            # Extract text lines from Textract response
            lines = self.textract_client.extract_text_lines(textract_result)
            raw_text = "\n".join(lines)
            
            if not raw_text.strip():
                logger.warning("No text extracted from scanned PDF")
                return {
                    "text": ""
                }
            
            # Clean the extracted text
            cleaned_text = preprocess_text(raw_text)
            
            result = {
                "text": cleaned_text
            }
            
            logger.info("Scanned PDF extraction pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Scanned PDF extraction failed: {e}")
            return {
                "error": f"Scanned PDF extraction failed: {str(e)}",
                "text": ""
            }
        
        finally:
            if object_name:
                try:
                    logger.debug(f"Cleaning up S3 object: {object_name}")
                    delete_file(object_name)
                    
                except Exception as cleanup_error:
                    logger.warning(f"Failed to cleanup S3 object {object_name}: {cleanup_error}")
