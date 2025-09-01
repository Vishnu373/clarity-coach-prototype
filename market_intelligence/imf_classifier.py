from services.prompts import EVALUATION_PROMPT
import json
from services.restructuring import get_restructured_data
from utils.model_client import gpt_model
import re

def classifier(data):
    prompt = EVALUATION_PROMPT.format(
        text=json.dumps(data, ensure_ascii=False)
    )
    imf_values = gpt_model(prompt)

    return imf_values

def parse_data(data):
    data = json.loads(data)

    score_evaluation = data["SCORE_EVALUATION"]
    upskill = data["UPSKILL"]
    suggested_job_titles = data["SUGGESTED_JOB_TITLES"]

    return score_evaluation, upskill, suggested_job_titles

restructured_data = get_restructured_data()