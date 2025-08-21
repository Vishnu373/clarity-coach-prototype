import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_suggestions(user_role, user_skills, retrieved_chunks):
    # Prepare context
    context = "\n".join([f"- {c['content']}" for c in retrieved_chunks])
    skills = ", ".join(user_skills) if user_skills else "N/A"

    prompt = f"""
You are an assistant that suggests resume responsibilities.

The user’s job role:
{user_role}

Their known skills:
{skills}

Here are common responsibilities and projects for this type of role:
{context}

TASK: Suggest up to 10 additional resume bullet points that the user *might plausibly* have done.
RULES:
- Only use information consistent with the role and skills.
- Do NOT invent companies, dates, or personal details.
- Phrase each bullet in past tense, action-oriented style (e.g., "Developed...").
- Keep them concise and resume-ready.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content
