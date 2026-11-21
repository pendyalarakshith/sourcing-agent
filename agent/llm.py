import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key="ollama",  # required by the library, ignored by Ollama
)
MODEL = os.getenv("LLM_MODEL", "qwen3.5:4b")