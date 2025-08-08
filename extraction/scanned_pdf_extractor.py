from io import BytesIO
from services.s3_client import S3Client
from services.textract_client import TextractClient

class ScannedPdfPipeline:
    def __init__(self, file_bytes: bytes, bucket_name: str, region="us-east-1"):
        self.file_bytes = file_bytes
        self.bucket_name = bucket_name
        self.s3_client = S3Client(region=region, bucket_name=bucket_name)
        self.textract_client = TextractClient(region=region)

    def run_pipeline(self):
        try:
            # Upload to S3
            object_name = self.s3_client.upload_file(BytesIO(self.file_bytes))

            # Extract text
            textract_result = self.textract_client.detect_document_text(self.bucket_name, object_name)

            # Parse lines
            pages = [block["Text"] for block in textract_result.get("Blocks", []) if block["BlockType"] == "LINE"]

            return {
                "text": "\n".join(pages),
                "key_value_pairs": [],
                "tables": []
            }
        finally:
            # Delete object after processing
            self.s3_client.delete_file(object_name)
