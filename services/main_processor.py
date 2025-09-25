from extraction import validation_pipeline
from config import AWS_S3_BUCKET

class MainProcessor:
    
    def __init__(self):
        self.bucket_name = AWS_S3_BUCKET
    
    # 0. Run validation and extraction pipeline
    def process_resume(self, filename: str, file_bytes: bytes) -> dict:        
        result = validation_pipeline(filename, file_bytes, bucket_name=self.bucket_name)
        
        # Add processing metadata
        result["filename"] = filename
        result["file_size"] = len(file_bytes)
        
        return result
    
    def get_processing_status(self, result: dict) -> dict:        
        if "error" in result:
            return {
                "success": False,
                "message": result["error"],
                "type": "error"
            }
        
        validation_info = result.get("validation", {})
        
        return {
            "success": True,
            "message": f"Valid resume processed successfully",
            "validation_reason": validation_info.get("reason", ""),
            "type": "success"
        }


def process_file(filename: str, file_bytes: bytes) -> dict:
    """Quick processing function"""
    processor = MainProcessor()
    return processor.process_resume_file(filename, file_bytes)

def get_status(result: dict) -> dict:
    processor = MainProcessor()
    return processor.get_processing_status(result)