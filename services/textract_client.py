import boto3
import os

class TextractClient:
    def __init__(self, region=None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.client = boto3.client("textract", region_name=self.region)

    def detect_document_text(self, bucket_name, object_name):
        """Simple text detection."""
        return self.client.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": object_name
                }
            }
        )

    def analyze_document(self, bucket_name, object_name, features=None):
        """Full analysis for forms & tables."""
        return self.client.analyze_document(
            Document={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": object_name
                }
            },
            FeatureTypes=features or ["FORMS", "TABLES"]
        )
