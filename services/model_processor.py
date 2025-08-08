import json
import re
from services.prompts import STRUCTURE_FILTER_PROMPT
from services.model_client import gpt_model

def process_with_model(extracted_data: dict) -> dict:
    prompt = STRUCTURE_FILTER_PROMPT.format(
        text=json.dumps(extracted_data, ensure_ascii=False)
    )

    raw_response = gpt_model(prompt)

    match = re.search(r"\{.*\}", raw_response, re.S)
    if not match:
        raise ValueError("No valid JSON found in model output.")

    json_str = match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e}")
