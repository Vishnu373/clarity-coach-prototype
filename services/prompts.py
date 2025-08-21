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

The JSON must have exactly TWO top-level keys:
1. RESUME_STRUCTURED
2. MARKET_INTEL

{{
  "RESUME_STRUCTURED": {{
    "experience": [
      {{
        "title": string,
        "location": string|null,
        "duration": string,
        "responsibilities": string,
        "projects": [
          {{ "title": string, "description": string }}
        ]
      }}
    ],
    "awards": [string],
    "publications": [string],
    "skills": [string]
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
