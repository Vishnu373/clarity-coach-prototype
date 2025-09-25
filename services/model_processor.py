import json
import re
from io import BytesIO
from typing import Tuple

from services.prompts import HYBRID_EXTRACTION_PROMPT
from utils.model_client import gpt_model
from utils.s3_client import S3Client
from config import S3_MARKET_INTEL_KEY

# Create S3 client instance
s3_client = S3Client()

def file_processing(extracted_data: dict) -> Tuple[dict, dict]:
    
    prompt = HYBRID_EXTRACTION_PROMPT.format(
        text=json.dumps(extracted_data, ensure_ascii=False)
    )

    raw_response = gpt_model(prompt)

    match = re.search(r"\{.*\}", raw_response, re.S)
    if not match:
        raise ValueError("No valid JSON found in model output.")

    json_str = match.group(0)

    try:
        data = json.loads(json_str)

        # Input for RAG
        rag_input = data.get("RESUME_STRUCTURED", {})

        # Input for feature 2
        market_intelligence_input = data.get("MARKET_INTEL", {})

        # Upload to S3       
        market_json = json.dumps(market_intelligence_input, ensure_ascii=False, indent=2).encode('utf-8')
        market_file_obj = BytesIO(market_json)
        s3_client.upload_file(market_file_obj, S3_MARKET_INTEL_KEY)

        return rag_input, market_intelligence_input
    
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e}")

# Getter functions to download from S3
def get_market_intelligence_input():
    """Download market intelligence data from S3"""
    json_data = s3_client.download_file(S3_MARKET_INTEL_KEY)
    return json.loads(json_data)
