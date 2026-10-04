import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PROVIDER = os.getenv("PROVIDER", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3.5:latest")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DB_PATH = os.getenv("DB_PATH", "agent_state.db")
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "./test_workspace")
HISTORY_DIR = os.getenv("HISTORY_DIR", "./history")