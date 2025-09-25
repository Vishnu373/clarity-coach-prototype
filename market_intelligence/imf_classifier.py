from services.prompts import EVALUATION_PROMPT
from utils.model_client import gpt_model
import json

def classifier(data):
    """Classify resume data for AI risk assessment"""
    prompt = EVALUATION_PROMPT.format(
        text=json.dumps(data, ensure_ascii=False)
    )
    imf_values = gpt_model(prompt)

    return imf_values

def parse_data(data):
    """Parse classification results into components"""
    data = json.loads(data)

    score_evaluation = data["SCORE_EVALUATION"]
    upskill = data["UPSKILL"]
    suggested_job_titles = data["SUGGESTED_JOB_TITLES"]

    return score_evaluation, upskill, suggested_job_titles
