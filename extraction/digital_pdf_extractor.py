import pdfplumber
import logging
from io import BytesIO
from .preprocessing import preprocess_text

# Configure logging
logger = logging.getLogger(__name__)

class DigitalPDFPipeline:
    def __init__(self, file_bytes: bytes):
        self.file_bytes = file_bytes

    def extract_text(self):
        try:
            with pdfplumber.open(BytesIO(self.file_bytes)) as pdf:
                text_parts = []
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                    except Exception as e:
                        logger.warning(f"Failed to extract text from page {page_num}: {e}")
                        continue
                
                if not text_parts:
                    logger.warning("No text extracted from PDF")
                    return ""
                
                logger.info(f"Successfully extracted text from {len(text_parts)} pages")
                return '\n'.join(text_parts)
                
        except (FileNotFoundError, OSError) as e:
            logger.error(f"PDF file access error: {e}")
            raise RuntimeError(f"Cannot access PDF file: {e}")
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            raise RuntimeError(f"Failed to extract text from PDF: {e}")

    def extract_tables(self):
        try:
            with pdfplumber.open(BytesIO(self.file_bytes)) as pdf:
                all_tables = []
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        tables = page.extract_tables()
                        if tables:
                            all_tables.extend(tables)
                            logger.debug(f"Found {len(tables)} tables on page {page_num}")
                    except Exception as e:
                        logger.warning(f"Failed to extract tables from page {page_num}: {e}")
                        continue
                
                if all_tables:
                    logger.info(f"Successfully extracted {len(all_tables)} tables from PDF")
                else:
                    logger.debug("No tables found in PDF")
                    
                return all_tables
                
        except (FileNotFoundError, OSError) as e:
            logger.error(f"PDF file access error during table extraction: {e}")
            return []
        except Exception as e:
            logger.error(f"Table extraction failed: {e}")
            return []

    def run_pipeline(self):
        try:
            # Extract and clean text
            raw_text = self.extract_text()
            cleaned_text = preprocess_text(raw_text)
            
            # Extract tables (always include, even if empty)
            tables = self.extract_tables()
            
            result = {
                "text": cleaned_text,
                "tables": tables
            }

            logger.info("Digital PDF extraction pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Digital PDF pipeline failed: {e}")
            return {
                "error": f"Digital PDF extraction failed: {str(e)}",
                "text": ""
            }
