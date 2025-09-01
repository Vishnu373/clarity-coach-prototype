import boto3
from botocore.exceptions import ClientError
import uuid
import os
from typing import BinaryIO, Optional

class S3Client:
    def __init__(self, region: Optional[str] = None, bucket_name: Optional[str] = None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.bucket_name = bucket_name or os.getenv("AWS_S3_BUCKET")
        if not self.bucket_name:
            raise ValueError("Bucket name must be provided via constructor or env var.")
        self.s3 = boto3.client('s3', region_name=self.region)

    def upload_file(self, file_obj: BinaryIO, filename: Optional[str] = None) -> str:
        key = filename or str(uuid.uuid4())
        try:
            self.s3.upload_fileobj(file_obj, self.bucket_name, key)
            return key
        except ClientError as e:
            raise RuntimeError(f"Error uploading file: {e}")

    def download_file(self, key: str) -> str:
        """Download file content as string"""
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            raise RuntimeError(f"Error downloading file: {e}")

    def delete_file(self, key: str) -> None:
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            raise RuntimeError(f"Error deleting file: {e}")