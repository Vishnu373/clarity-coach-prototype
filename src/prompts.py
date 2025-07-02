resume_check = """
You are a helpful assistant that identifies resume documents.

Below is the extracted text from a document.
Your job is to decide if this is a resume. 
Reply only with "Yes" if it's a resume or "No" if it is not. 
Do not provide any explanation.

Text:
{text}
"""

structuring_prompt = """
You are a helpful assistant. Your job is to extract structured information from a resume.
The information was extracted from a resume file and is provided as plain text.
So, the text can contain:
1. plain text
2. tables 
3. multi column layout format as well

Return the following information in JSON format:
name: Full name of the person
email: Email address
phone: Phone number
location: Current city and country (if available)
skills: List of technical and soft skills
education: List of degrees with institution, graduation year (if available)
experience: List of jobs including title, company, duration, and responsibilities
projects: List of notable projects (with title + descriptions)
publications: if avaialable
awards: if available

Note: If the projects are mentioned under the experience section, no need to print it again in projects part.

Guidelines:
Return only valid JSON. No explanations, no extra text, and no markdown formatting.
Do not hallucinate data.
If any fields are missing, leave them as empty lists or null.

Text:
{text}
"""