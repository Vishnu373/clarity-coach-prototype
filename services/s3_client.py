import boto3
import uuid
import logging
from typing import BinaryIO, Optional
from botocore.exceptions import ClientError, NoCredentialsError
from config import AWS_REGION, AWS_S3_BUCKET

# Configure logging
logger = logging.getLogger(__name__)

# Initialize S3 client once
_s3_client = None

def _get_s3_client():
    global _s3_client
    if _s3_client is None:
        try:
            _s3_client = boto3.client('s3', region_name=AWS_REGION)
        
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise

        except Exception as e:
            logger.error(f"Failed to create S3 client: {e}")
            raise
    return _s3_client

def get_bucket() -> str:
    if not AWS_S3_BUCKET:
        raise ValueError("S3 bucket name not configured")
    
    return AWS_S3_BUCKET

def upload_file(file_obj: BinaryIO, filename: Optional[str] = None) -> str:
    bucket_name = get_bucket()
    key = filename or str(uuid.uuid4())
    
    try:
        s3_client = _get_s3_client()
        s3_client.upload_fileobj(file_obj, bucket_name, key)
        logger.info(f"Uploaded file to S3: {key}")
        return key
    
    except ClientError as e:
        logger.error(f"S3 upload failed: {e}")
        raise RuntimeError(f"Failed to upload file to S3: {e}")

def delete_file(key: str) -> bool:
    if not key:
        return False
        
    bucket_name = get_bucket()
    
    try:
        s3_client = _get_s3_client()
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        logger.info(f"Deleted file from S3: {key}")
        return True
    
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code == 'NoSuchKey':
            logger.warning(f"File not found in S3: {key}")
            return True  # Consider success if file doesn't exist
        logger.error(f"S3 delete failed: {e}")
        return False
    
    except Exception as e:
        logger.error(f"Error deleting S3 file: {e}")
        return False