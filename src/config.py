import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Google AI Configuration ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

# --- Qdrant Configuration ---
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "diabetes_rag_gemini")

# --- Model Configuration ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash-latest")

# --- Data Directories ---
DATA_DIR_GENERAL = "./data/general_docs"
DATA_DIR_PATIENTS = "./data/patient_records"

# --- Text Splitting Configuration ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150