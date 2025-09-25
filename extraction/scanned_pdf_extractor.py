from io import BytesIO
from utils.s3_client import S3Client
from utils.textract_client import TextractClient
from .preprocessing import preprocess_text

class ScannedPdfPipeline:
    def __init__(self, file_bytes: bytes, bucket_name: str, region="us-east-1"):
        self.file_bytes = file_bytes
        self.bucket_name = bucket_name
        self.s3_client = S3Client(region=region, bucket_name=bucket_name)
        self.textract_client = TextractClient(region=region)

    def run_pipeline(self):
        object_name = None
        try:
            object_name = self.s3_client.upload_file(BytesIO(self.file_bytes))
            textract_result = self.textract_client.detect_document_text(self.bucket_name, object_name)
            
            lines = [block["Text"] for block in textract_result.get("Blocks", []) if block["BlockType"] == "LINE"]
            raw_text = "\n".join(lines)
            
            cleaned_text = preprocess_text(raw_text)
            
            return {"text": cleaned_text}
            
        except Exception as e:
            print(f"Scanned PDF extraction failed: {e}")
            return {"text": ""}
        finally:
            if object_name:
                try:
                    self.s3_client.delete_file(object_name)
                except:
                    pass
