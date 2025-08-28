from services.prompts import IMF_CLASSIFICATION_PROMPT
import json
from services.restructuring import get_restructured_data
from services.model_client import gpt_model
import re

def classifier(data):
    prompt = IMF_CLASSIFICATION_PROMPT.format(
        text=json.dumps(data, ensure_ascii=False)
    )
    imf_values = gpt_model(prompt)

    return imf_values

restructured_data = get_restructured_data()
results = str(classifier(restructured_data))

# print(results)

def parse_results(results):
    task_match = re.search(r'Task Modifier:\s*([^,]+)', results)
    industry_match = re.search(r'Industry Risk Adjustment:\s*([^,]+)', results)
    skill_match = re.search(r'Skill Modifier:\s*(.+)', results)

    # Extract values or empty string if not found
    task_category = task_match.group(1).strip() if task_match else ""
    industry_category = industry_match.group(1).strip() if industry_match else ""
    skills_category = skill_match.group(1).strip() if skill_match else ""

    return task_category, industry_category, skills_category

task_category, industry_category, skills_category = parse_results(results)

# print(task_category)
# print(industry_category)
# print(skills_category)

