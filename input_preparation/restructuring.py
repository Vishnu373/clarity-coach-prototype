from services.prompts import RESTRUCTURE_RESUME_PROMPT
from services.model_client import gpt_model
import json

def restructure_resume(data):
    prompt = RESTRUCTURE_RESUME_PROMPT.format(
            text=json.dumps(data, ensure_ascii=False)
        )

    restructured_data = gpt_model(prompt)

    return restructured_data
    