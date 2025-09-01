from market_intelligence.imf_classifier import parse_data
from market_intelligence.role_exposure import get_score_evaluators, score_calculator
from services.restructuring import get_restructured_data
from market_intelligence.imf_classifier import classifier
from services.model_processor import get_market_intelligence_input
from market_intelligence.job_fetch import search_jobs, print_output
from utils.s3_client import S3Client
import streamlit as st

def display_jobs(jobs):   
    for job in jobs:
        st.subheader(job['title'])
        st.write(f"**Company:** {job['company_name']}")
        st.write(f"**Location:** {job['location']}")
        st.write(f"**Posted:** {job['extensions'][0] if job.get('extensions') else 'N/A'}")
        
        with st.expander("View Description"):
            st.write(job.get('description', 'No description'))
        
        if job.get('apply_options'):
            st.write("**Apply:**")
            for option in job['apply_options']:
                st.link_button(option['title'], option['link'])
        
        st.divider()


def run_mi_pipeline():
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
    st.subheader("IMF Gen-AI Report (2024)")
    st.write(f"**Score:** {final_score}")
    st.write(f"**Risk Level:** {risk_level}")
    st.write(f"**Interpretation:** {interpretation}")

    # 5. Upskill suggestions
    st.subheader("Suggested Skills to Upskill")
    st.write(upskill["skills"])

    # 6. Jobs fetched
    # 6.1. Preparing the required data
    job_title = suggested_job_titles['job_titles'][0]
    location_data = get_market_intelligence_input()
    location = location_data["current_location_inferred"]["country"]

    # 6.2 Jobs fetched
    jobs = search_jobs(job_title, location)

    # 6.3. Prints the result
    display_jobs(jobs)

    # 7. Delete files from S3
    S3Client().delete_file("restructured_data.json")
    S3Client().delete_file("market_intel.json")
  