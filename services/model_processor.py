import json
import re
from services.prompts import HYBRID_EXTRACTION_PROMPT
from services.model_client import gpt_model

def process_with_model(extracted_data: dict) -> dict:
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

        return data, rag_input, market_intelligence_input
    
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e}")
    
    