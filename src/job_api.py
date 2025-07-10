import requests
import os
from datetime import datetime, timedelta

def fetch_jobs(job_title: str, location: str, days_limit: int):
    baseUrl = "https://serpapi.com"
    api_key = os.getenv("SERP_API_KEY")

    if not api_key:
        print("Error: SERP_API_KEY not found in environment variables.")
        return

    print(f"Searching for '{job_title}' jobs in '{location}' posted within last {days_limit} day(s).\n")

    params = {
        "engine": "google_jobs",
        "q": job_title,
        "location": location,
        "api_key": api_key,
        "job_type": "full_time"
    }

    response = requests.get(f"{baseUrl}/search", params=params)
    data = response.json()

    jobs_results = data.get("jobs_results", [])
    filtered_jobs = []

    for job in jobs_results:
        posted_str = job.get('detected_extensions', {}).get('posted_at', '').lower()
        if posted_str:
            if "hour" in posted_str or "just posted" in posted_str:
                # Consider very recent posts as within limit
                filtered_jobs.append(job)
            elif "day" in posted_str:
                try:
                    days_ago = int(posted_str.split()[0])
                    if days_ago <= days_limit:
                        filtered_jobs.append(job)
                except ValueError:
                    # In case parsing fails, ignore this job
                    continue

    if filtered_jobs:
        print(f"Found {len(filtered_jobs)} job(s):\n")
        for job in filtered_jobs:
            print(f"Title: {job.get('title')}")
            print(f"Company: {job.get('company_name')}")
            print(f"Location: {job.get('location')}")
            print(f"Posted: {job.get('detected_extensions', {}).get('posted_at')}")
            print(f"Link: {job.get('apply_options')[0]['link'] if job.get('apply_options') else 'N/A'}")
            print("------")
    else:
        print(f"No jobs found within the last {days_limit} day(s).")

# fetch_jobs("Software Engineer", "Toronto", 3)

"""
cities = [
    "Toronto", "Vancouver", "Calgary", "Montreal", "Ottawa", "Waterloo",
    "San Francisco", "Austin", "Boise", "Seattle", "New York", "Boston", "Raleigh", "Salt Lake City",
    "Berlin", "Paris", "Madrid", "Amsterdam", "Tallinn", "Helsinki", "Zurich", "Lisbon", "Copenhagen", "Krakow", "Vilnius", "Ljubljana"
]
"""

# Current option - SERP API
# Second option for API - Adzuna Jobs API