from services.prompts import RESTRUCTURE_RESUME_PROMPT
from utils.model_client import gpt_model
from utils.s3_client import S3Client
from config import S3_RESTRUCTURED_DATA_KEY
from io import BytesIO
import json

# Create S3 client instance
s3_client = S3Client()

def restructure_resume(data):

    # Restructuring the extracted resume
    prompt = RESTRUCTURE_RESUME_PROMPT.format(
            text=json.dumps(data, ensure_ascii=False)
        )

    restructured_data = gpt_model(prompt)        

    # Upload the data to S3
    restructured_data_encoded = restructured_data.encode('utf-8')
    restructured_data_obj = BytesIO(restructured_data_encoded)
    s3_client.upload_file(restructured_data_obj, S3_RESTRUCTURED_DATA_KEY)

    return restructured_data

# Download the file from S3
def get_restructured_data():
    """Download restructured data from S3"""
    restructured_data = s3_client.download_file(S3_RESTRUCTURED_DATA_KEY)
    return restructured_data
