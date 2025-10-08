import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
KB_KEY = os.getenv("KB_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
MONGODB_DATABASE_NAME = "ClarityCoachData"
MONGODB_COLLECTION_NAME = "user_resumes"

GPT_4O_MINI_MODEL = "gpt-4o-mini"
GPT_5_MODEL = "gpt-5"
EMBEDDING_MODEL = "text-embedding-3-large"

SUPPORTED_FILE_EXTENSIONS = {".pdf", ".docx", ".txt"}

CHUNK_SIZE = 256
CHUNK_OVERLAP = 30
TOP_K_RETRIEVAL = 3
