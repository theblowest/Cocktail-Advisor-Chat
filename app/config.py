import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# Vector DB Configuration
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./chroma_db")

# Data paths
DATA_DIR = os.getenv("DATA_DIR", "./data")
COCKTAILS_DATA = os.path.join(DATA_DIR, "cocktails.csv")

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# LLM Configuration
TEMPERATURE = 0.7
MAX_TOKENS = 1000

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
