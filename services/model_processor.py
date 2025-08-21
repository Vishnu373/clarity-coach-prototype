import json
import re
import uuid
from io import BytesIO
from typing import Optional, Tuple

from services.prompts import HYBRID_EXTRACTION_PROMPT
from services.model_client import gpt_model
from services.s3_client import S3Client

# Create S3 client instance
s3_client = S3Client()

# Store S3 keys for the uploaded files (fixed names)
_s3_keys = {
    'data': 'processed_data.json',
    'rag_input': 'rag_input.json',
    'market_intelligence': 'market_intel.json'
}

def process_with_model(extracted_data: dict) -> Tuple[dict, dict, dict]:
    global _s3_keys
    
    prompt = HYBRID_EXTRACTION_PROMPT.format(
        text=json.dumps(extracted_data, ensure_ascii=False)
    )

    raw_response = gpt_model(prompt)

    match = re.search(r"\{.*\}", raw_response, re.S)
    if not match:
        raise ValueError("No valid JSON found in model output.")

    json_str = match.group(0)

    try:
        # Output from LLM call
        data = json.loads(json_str)
        # Input for RAG
        rag_input = data.get("RESUME_STRUCTURED", {})
        # Input for feature 2
        market_intelligence_input = data.get("MARKET_INTEL", {})

        # Upload to S3 with fixed names
        data_json = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        data_file_obj = BytesIO(data_json)
        s3_client.upload_file(data_file_obj, _s3_keys['data'])
        
        rag_json = json.dumps(rag_input, ensure_ascii=False, indent=2).encode('utf-8')
        rag_file_obj = BytesIO(rag_json)
        s3_client.upload_file(rag_file_obj, _s3_keys['rag_input'])
        
        market_json = json.dumps(market_intelligence_input, ensure_ascii=False, indent=2).encode('utf-8')
        market_file_obj = BytesIO(market_json)
        s3_client.upload_file(market_file_obj, _s3_keys['market_intelligence'])

        return data, rag_input, market_intelligence_input
    
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e}")

# Getter functions to download from S3
def get_cached_data():
    json_data = s3_client.download_file(_s3_keys['data'])
    return json.loads(json_data)

def get_rag_input():
    json_data = s3_client.download_file(_s3_keys['rag_input'])
    return json.loads(json_data)

def get_market_intelligence_input():
    json_data = s3_client.download_file(_s3_keys['market_intelligence'])
    return json.loads(json_data)
