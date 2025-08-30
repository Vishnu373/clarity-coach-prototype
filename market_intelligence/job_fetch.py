import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_jobs(job_title, location):
    if not SERPAPI_KEY:
        raise RuntimeError("Missing SERPAPI_KEY environment variable.")
    
    params = {
        "engine": "google_jobs",
        "q": job_title,
        "location": location,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("jobs_results", [])

def print_output(jobs):
    for i, job in enumerate(jobs, 1):
        posted = job.get("detected_extensions", {}).get("posted_at")
        # pick the first available apply link
        link = None
        for opt in job.get("apply_options", []) or []:
            if opt.get("link"):
                link = opt["link"]; break
        link = link or job.get("apply_link") or job.get("link")

        print(f"{i}. {job.get('title')} at {job.get('company_name')} ({job.get('location')})")
        print(f"   Posted: {posted}")
        print(f"   Link: {link}")
        print()
