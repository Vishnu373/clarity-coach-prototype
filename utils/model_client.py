from openai import OpenAI
from config import OPENAI_API_KEY, GPT_4O_MINI_MODEL, GPT_5_MODEL, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def gpt_model(prompt_template: str, text: str = "") -> str:
    """Standard GPT model for general tasks"""
    if "{text}" in prompt_template:
        prompt = prompt_template.format(text=text)
    else:
        prompt = prompt_template
    
    response = client.chat.completions.create(
        model=GPT_4O_MINI_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def rag_model(prompt_template: str, text: str = "") -> str:
    """Advanced GPT model for RAG and complex tasks"""
    if "{text}" in prompt_template:
        prompt = prompt_template.format(text=text)
    else:
        prompt = prompt_template
    
    response = client.chat.completions.create(
        model="GPT_5_MODEL",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content.strip()

def embedding_model(text):
    """Generate embeddings for text using OpenAI embedding model"""
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding
