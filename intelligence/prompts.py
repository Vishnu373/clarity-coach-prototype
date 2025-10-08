def get_field_identification_prompt(resume_text):
    field_identificaiton_prompt = f"""
You are a resume parsing expert. Extract and structure ALL the information from the following resume text into a standardized JSON format.

IMPORTANT INSTRUCTIONS:
1. Use these EXACT field names: contact_info, experience, education, skills, projects, certifications, awards, publications, languages, volunteer, interests
2. If a section doesn't exist, omit it from the output
3. Standardize field names (e.g., "Work Experience" → experience, "Side Projects" → projects)
4. Parse dates into YYYY-MM format when possible, use "present" for current positions
5. Group skills into logical categories
6. Include inferred information: current_location_inferred, industry_inferred, career_level_inferred

OUTPUT REQUIREMENTS:
- Return ONLY valid JSON
- Use the exact structure shown in the example
- Be thorough - extract ALL available information
- Maintain original text for achievements/descriptions

RESUME TEXT:
{resume_text}

Return the structured data as JSON:
"""
    
    return field_identificaiton_prompt


def get_system_message():
    system_message = """You are a professional resume parser. Your task is to extract and structure resume information into standardized JSON format. 

Key requirements:
- Extract ALL available information
- Use standardized field names
- Parse dates consistently  
- Group related information logically
- Infer location, industry, and career level
- Return only valid JSON without any explanation"""
    
    return system_message