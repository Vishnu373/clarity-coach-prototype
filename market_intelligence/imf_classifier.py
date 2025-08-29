from services.prompts import EVALUATION_PROMPT
import json
from analysis_and_enhancement.restructuring import get_restructured_data
from services.model_client import gpt_model
import re

def classifier(data):
    prompt = EVALUATION_PROMPT.format(
        text=json.dumps(data, ensure_ascii=False)
    )
    imf_values = gpt_model(prompt)

    return imf_values

restructured_data = get_restructured_data()
results = str(classifier(restructured_data))

# print("Here's the result: ", results)

def parse_data(data):
    data = json.loads(data)

    score_evaluation = data["SCORE_EVALUATION"]
    upskill = data["UPSKILL"]
    suggested_job_titles = data["SUGGESTED_JOB_TITLES"]

    return score_evaluation, upskill, suggested_job_titles
