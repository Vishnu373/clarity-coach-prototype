# STRUCTURE_FILTER_PROMPT = """
# Extract structured information from the following resume text into ONE valid JSON object exactly as defined.

# GLOBAL RULES:
# - Return ONLY one valid JSON object.
# - No markdown, no extra text, no explanations.
# - Do not fabricate data.
# - If no data for a field, use empty arrays [] or null.
# - Avoid duplicates between STRUCTURED_RESUME.projects and FILTERED_EXPERIENCE.projects.
# - Format with indentation for readability.

# The JSON must have exactly these two keys:

# {{
#   "STRUCTURED_RESUME": {{
#     "experience": [
#       {{
#         "title": string,
#         "location": string|null,
#         "duration": string,
#         "responsibilities": string,
#         "projects": [
#           {{ "title": string, "description": string }}
#         ]
#       }}
#     ],
#     "awards": [string],
#     "publications": [string]
#   }},
#   "FILTERED_EXPERIENCE": [
#     {{
#       "role": string,
#       "skills": [string],
#       "projects": [string]
#     }}
#   ]
# }}

# Rules for FILTERED_EXPERIENCE:
# - Include only professional experience/internships.
# - Limit skills to 3–5 per role.
# - Limit projects to 3–5 per role.
# - If no specific projects, include key responsibilities as project-like entries.

# TEXT:
# {text}
# """

HYBRID_EXTRACTION_PROMPT = """
Extract structured information from the following resume text into ONE valid JSON object exactly as defined.

GLOBAL RULES:
- Include professional experience, internships and personal or side projects.
- Return ONLY one valid JSON object.
- No markdown, no extra text, no explanations.
- Do not fabricate data.
- If no data for a field, use empty arrays [] or null.
- Format with indentation for readability.

RULES REGARDING RESUME_STRUCTURED:
- Fetch all the job experiences the user has done throughout his career.
- If the user has done any personal or side projects - include it in the experience part at last.
- In case of personal or side projects - carefully analyze the responsbilities and assign a "role" accordingly.
- Analyze the user's skills and the skill set used in the project and then mention top 3 skills in the "skills" section.
- Don't make the skills like general make it specific like what technology was used if available.
- Just the skills must be in the list no index number required.
- Avoid hallucination as much as possible.

The JSON must have exactly TWO top-level keys:
1. RESUME_STRUCTURED
2. MARKET_INTEL

{{ 
    "RESUME_STRUCTURED": {{
    "experience": [
      {{
        "role": string,
        "skills": string,
        "responsibilities": string,
      }}
    ]
  }},
  "MARKET_INTEL": {{
    "current_location_inferred": {{
      "city": string|null,
      "state": string|null,
      "country": string|null
    }},
    "industry_inferred": string|null,
    "career_level_inferred": string|null
  }}
}}

TEXT:
{text}
"""

AUGMENT_PROMPT = """
You are an AI resume coach. You are getting some data which is retrieved data.
The retrieved data is in dictionary format.
The main components of the retrieval_results are:
role - What was the job title for which the retrieval was done?
query - The job title with the skills combined
results - Matching data found from the existing knowledge base.

Here are the retrieved matches from the knowledge base:
{retrieval_results}

TASK:
For each role the user have done:
1. Suggest upto 10 new bullet points/responsibilities the user might plausibly have done.

RULES:
- Base suggestions on the reference knowledge and the user’s role/skills.
- Keep each bullet concise, past tense, action-oriented.
- Avoid duplicates of existing bullets.
- Do NOT invent employers, dates, or personal details.
- Return ONLY a JSON array of strings.

Give me the final output in following format for each role:
1. role - the title of the job
2. repsonsbilities - all the 10 bullet points/responsbilities line by line no other extra context required
"role": {{
"repsonsbilities": {{
}} 
}}
"""