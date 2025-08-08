from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def gpt_model(prompt_template: str, text: str = "") -> str:
    if "{text}" in prompt_template:
        prompt = prompt_template.format(text=text)
    else:
        prompt = prompt_template  # already fully formatted
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
