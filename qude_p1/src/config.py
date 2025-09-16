import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Project Paths ---
# This assumes the script is run from the project root (DiabetesRAG/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
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