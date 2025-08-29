from market_intelligence.imf_classifier import parse_data
from market_intelligence.role_exposure import get_score_evaluators, score_calculator
from analysis_and_enhancement.restructuring import get_restructured_data
from market_intelligence.imf_classifier import classifier

def run_pipeline():
    # 1. Getting the data
    restructured_data = get_restructured_data()

    # 2. Classified data
    results = str(classifier(restructured_data))

    # 3. Parsing the classified data
    score_evaluation, upskill, suggested_job_titles = parse_data(results)
    # task_category, industry_category, skill_category = parse_results(results)

    # 4. Calculating the score
    tasks_category, industry_category, skills_category = get_score_evaluators(score_evaluation)
    final_score, risk_level, interpretation = score_calculator(tasks_category, industry_category, skills_category)

    # 5. Delete files from S3 - to be added later

    # 6. Score results
    print(f"Based on the IMF’s Gen-AI report (2024): The score is: {final_score}.\nThe risk is classifed as {risk_level}.\nInterpretation: {interpretation}")

    # 7. Upskill suggestions
    print("Suggested skills to upskill: ", upskill["skills"])

run_pipeline()
