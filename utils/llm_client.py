import openai
import logging
from config import OPENAI_API_KEY, GPT_4O_MINI_MODEL

logger = logging.getLogger(__name__)
openai.api_key = OPENAI_API_KEY

def smaller_model(prompt, temperature=0.1, system_message=None):
    try:
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        response = openai.chat.completions.create(
            model=GPT_4O_MINI_MODEL,
            messages=messages,
            temperature=temperature
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"GPT-4o-mini API call failed: {e}")
        raise Exception(f"Failed to call {GPT_4O_MINI_MODEL}: {str(e)}")