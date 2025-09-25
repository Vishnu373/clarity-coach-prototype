import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

KB_PATH = os.getenv("KB_PATH", "data/knowledge__base.txt")

GPT_4O_MINI_MODEL = "gpt-4o-mini"
GPT_5_MODEL = "gpt-5"
EMBEDDING_MODEL = "text-embedding-3-small"

SUPPORTED_FILE_EXTENSIONS = {".pdf", ".docx", ".txt"}

CHUNK_SIZE = 256
CHUNK_OVERLAP = 30
TOP_K_RETRIEVAL = 3

S3_RESTRUCTURED_DATA_KEY = "restructured_data.txt"
S3_MARKET_INTEL_KEY = "market_intel.json"
S3_RAG_INPUT_KEY = "rag_input.json"
S3_KNOWLEDGE_BASE_KEY = "knowledge_base.txt"