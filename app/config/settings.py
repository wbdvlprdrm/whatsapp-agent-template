import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

def get_env(name: str, required: bool = True, default=None):
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

# =========================
# WhatsApp
# =========================
WHATSAPP_TOKEN = get_env("WHATSAPP_TOKEN", required=False)
WHATSAPP_PHONE_ID = get_env("WHATSAPP_PHONE_ID", required=False)
VERIFY_TOKEN = get_env("VERIFY_TOKEN", required=False)

# =========================
# LLM
# =========================
LLM_PROVIDER = get_env("LLM_PROVIDER", required=False, default="groq")
GROQ_API_KEY = get_env("GROQ_API_KEY", required=False)

# =========================
# App
# =========================
APP_ENV = get_env("APP_ENV", required=False, default="development")
