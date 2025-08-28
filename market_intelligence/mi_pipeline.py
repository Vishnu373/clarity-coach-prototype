from market_intelligence.imf_classifier import parse_results
from market_intelligence.role_exposure import score_calculator
from services.restructuring import get_restructured_data
from market_intelligence.imf_classifier import classifier

def run_pipeline():
    # 1. Getting the data
    restructured_data = get_restructured_data()

    # 2. Classified data
    results = str(classifier(restructured_data))

    # 3. Parsing the classified data
    task_category, industry_category, skill_category = parse_results(results)

    # 4. Calculating the score
    final_score, risk_level, interpretation = score_calculator(task_category, industry_category, skill_category)

    # Output
    print(f"Based on the IMF’s Gen-AI report (2024): {final_score}, {risk_level}, {interpretation}")

run_pipeline()
