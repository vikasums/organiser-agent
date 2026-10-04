from openai import OpenAI
from core.config import OLLAMA_BASE_URL, OPENAI_API_KEY, PROVIDER


def get_llm_client():
  if PROVIDER == "ollama":
    return OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
  elif PROVIDER == "openai":
    return OpenAI(api_key=OPENAI_API_KEY)
  else:
    raise ValueError(f"Unsupported provider: {PROVIDER}")


def get_embedding_client():
  # Dedicated client for local embedding calls
  return OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
