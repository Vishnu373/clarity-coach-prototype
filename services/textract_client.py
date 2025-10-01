import boto3
import logging
from botocore.exceptions import ClientError, NoCredentialsError
from config import AWS_REGION

# Configure logging
logger = logging.getLogger(__name__)

class TextractClient:
    def __init__(self, region: str = None):
        self.region = region or AWS_REGION
        try:
            self.client = boto3.client("textract", region_name=self.region)
            logger.info(f"Textract client initialized for region: {self.region}")

        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise

        except Exception as e:
            logger.error(f"Failed to create Textract client: {e}")
            raise
    
    def detect_document_text(self, bucket_name: str, object_name: str) -> dict:
        try:
            response = self.client.detect_document_text(
                Document={
                    "S3Object": {
                        "Bucket": bucket_name,
                        "Name": object_name
                    }
                }
            )
            
            blocks = response.get("Blocks", [])
            text_blocks = [b for b in blocks if b["BlockType"] == "LINE"]
            logger.info(f"Textract detected {len(text_blocks)} text lines in document")
            
            return response
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            logger.error(f"Textract text detection failed with error {error_code}: {e}")
            raise RuntimeError(f"Failed to detect document text: {error_code}")

        except Exception as e:
            logger.error(f"Unexpected error during text detection: {e}")
            raise RuntimeError(f"Unexpected error during text detection: {e}")
    
    def analyze_document(self, bucket_name: str, object_name: str, features: list = None) -> dict:
        if features is None:
            features = ["FORMS", "TABLES"]
            
        try:
            response = self.client.analyze_document(
                Document={
                    "S3Object": {
                        "Bucket": bucket_name,
                        "Name": object_name
                    }
                },
                FeatureTypes=features
            )
            
            # Log basic stats
            blocks = response.get("Blocks", [])
            logger.info(f"Textract analyzed document with {len(blocks)} total blocks")
            
            return response
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            logger.error(f"Textract document analysis failed with error {error_code}: {e}")
            raise RuntimeError(f"Failed to analyze document: {error_code}")

        except Exception as e:
            logger.error(f"Unexpected error during document analysis: {e}")
            raise RuntimeError(f"Unexpected error during document analysis: {e}")
    
    def extract_text_lines(self, textract_response: dict) -> list:
        blocks = textract_response.get("Blocks", [])
        lines = [
            block["Text"] 
            for block in blocks 
            if block["BlockType"] == "LINE" and "Text" in block
        ]
        
        logger.debug(f"Extracted {len(lines)} text lines from Textract response")
        return lines