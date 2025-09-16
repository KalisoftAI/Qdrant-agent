# doctor_tools/rag_logic/rag_config.py
import os
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv(os.path.join(settings.BASE_DIR, '.env'))

# --- API Keys ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Project Paths ---
DATA_DIR = os.path.join(settings.BASE_DIR, "data")
CONVERSATIONS_DIR = os.path.join(DATA_DIR, "conversations")
KNOWLEDGE_BASE_DIR = os.path.join(DATA_DIR, "knowledge_base")

# --- Qdrant Configuration ---
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "diabetes_management"

# --- LangChain Model Configuration ---
EMBEDDING_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-1.5-pro-latest"

# --- Text Splitting Configuration ---
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200