from utils.model_client import rag_model
from services.prompts import AUGMENT_PROMPT
import json

"""
Augment prompt - Instructions + Retrieval results
Generation - Augment prompt + LLM call
"""
# Arugement passed -> retrieved results
def suggestions(results):
    prompt = AUGMENT_PROMPT.format(
        retrieval_results=json.dumps(results, indent=2),
    )

    suggestions_results = rag_model(prompt)

    try:
        return json.loads(suggestions_results)
    except:
        return [suggestions_results.strip()]
    
