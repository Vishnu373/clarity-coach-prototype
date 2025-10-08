import json
import logging
from services.llm_client import smaller_model
from .prompts import get_field_identification_prompt, get_system_message

logger = logging.getLogger(__name__)

def resume_field_identification(resume_text):
    try:
        logger.info("Starting resume field identification")
        
        prompt = get_field_identification_prompt(resume_text)
        system_message = get_system_message()
        
        response = smaller_model(
            prompt=prompt,
            system_message=system_message
        )
        
        identified_fields = json.loads(response)
        
        logger.info(f"Successfully identified {len(identified_fields)} field categories")
        return identified_fields
        
    except Exception as e:
        logger.error(f"Resume field identification failed: {e}")
        return {
            "error": f"Field identification failed: {str(e)}",
            "raw_text": resume_text
        }
