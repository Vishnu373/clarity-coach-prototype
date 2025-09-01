from io import BytesIO
from utils.s3_client import S3Client
from utils.textract_client import TextractClient

class ScannedPdfPipeline:
    def __init__(self, file_bytes: bytes, bucket_name: str, region="us-east-1"):
        self.file_bytes = file_bytes
        self.bucket_name = bucket_name
        self.s3_client = S3Client(region=region, bucket_name=bucket_name)
        self.textract_client = TextractClient(region=region)

    def run_pipeline(self):
        try:
            object_name = self.s3_client.upload_file(BytesIO(self.file_bytes))
            textract_result = self.textract_client.detect_document_text(self.bucket_name, object_name)
            pages = [block["Text"] for block in textract_result.get("Blocks", []) if block["BlockType"] == "LINE"]

            return {
                "text": "\n".join(pages),
                "key_value_pairs": [],
                "tables": []
            }
        finally:
            self.s3_client.delete_file(object_name)
