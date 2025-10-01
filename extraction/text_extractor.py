import logging
from .preprocessing import preprocess_text

# Configure logging
logger = logging.getLogger(__name__)

class TextPipeline:
    def __init__(self, file_bytes: bytes):
        self.file_bytes = file_bytes

    def extract_text(self):
        try:
            text = self.file_bytes.decode('utf-8')
            logger.info("Successfully decoded text file as UTF-8")
            return text
        
        except UnicodeDecodeError:
            try:
                text = self.file_bytes.decode('utf-8', errors='replace')
                logger.warning("Text file decoded with some character replacements")
                return text
            
            except Exception as e:
                logger.error(f"Failed to decode text file: {e}")
                raise RuntimeError(f"Cannot decode text file: {e}")
            
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            raise RuntimeError(f"Failed to extract text: {e}")

    def run_pipeline(self):
        try:
            raw_text = self.extract_text()
            cleaned_text = preprocess_text(raw_text)
            
            result = {
                "text": cleaned_text
                }
            
            logger.info("Text file extraction pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Text file pipeline failed: {e}")
            return {
                "error": f"Text file extraction failed: {str(e)}",
                "text": ""
            }
