from services.prompts import RESTRUCTURE_RESUME_PROMPT
from services.model_client import gpt_model
from services.s3_client import S3Client
from io import BytesIO
import json

# Create S3 client instance
s3_client = S3Client()

# Store S3 keys for the uploaded files
_s3_key = {'restructured_data': 'restructured_data.txt'}

def restructure_resume(data):
    global _s3_key

    # Restructuring the extracted resume
    prompt = RESTRUCTURE_RESUME_PROMPT.format(
            text=json.dumps(data, ensure_ascii=False)
        )

    restructured_data = gpt_model(prompt)        

    # Upload the data to S3
    restructured_data_encoded = restructured_data.encode('utf-8')
    restructured_data_obj = BytesIO(restructured_data_encoded)
    s3_client.upload_file(restructured_data_obj, _s3_key['restructured_data'])

    return restructured_data

# Download the file from S3
def get_restructured_data():
    restructured_data = s3_client.download_file(_s3_key['restructured_data'])
    return restructured_data

# print(get_restructured_data())