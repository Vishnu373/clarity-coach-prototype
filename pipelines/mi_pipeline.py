from market_intelligence.imf_classifier import parse_data
from market_intelligence.role_exposure import get_score_evaluators, score_calculator
from services.restructuring import get_restructured_data
from market_intelligence.imf_classifier import classifier
from services.model_processor import get_market_intelligence_input
from market_intelligence.job_fetch import search_jobs, print_output
from utils.s3_client import S3Client

def run_pipeline():
    # 0. Getting the data
    restructured_data = get_restructured_data()

    # 1. Classified data
    results = str(classifier(restructured_data))

    # 2. Parsing the classified data
    score_evaluation, upskill, suggested_job_titles = parse_data(results)

    # 3. Calculating the score
    tasks_category, industry_category, skills_category = get_score_evaluators(score_evaluation)
    final_score, risk_level, interpretation = score_calculator(tasks_category, industry_category, skills_category)

    # 4. Score results
    print(f"Based on the IMF’s Gen-AI report (2024): The score is: {final_score}.\nThe risk is classifed as {risk_level}.\nInterpretation: {interpretation}")

    # 5. Upskill suggestions
    print("Suggested skills to upskill: ", upskill["skills"])

    # 6. Jobs fetched
    # 6.1. Preparing the required data
    job_title = suggested_job_titles['job_titles'][0]
    location_data = get_market_intelligence_input()
    location = location_data["current_location_inferred"]["country"]

    # 6.2 Inputing the data and getting the results
    jobs = search_jobs(job_title, location)
    print_output(jobs)

    # 7. Delete files from S3
    S3Client().delete_file("restructured_data.json")
    S3Client().delete_file("market_intel.json")

run_pipeline()
  