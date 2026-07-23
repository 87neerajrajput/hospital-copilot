import os

from pathlib import Path
from dotenv import load_dotenv


# ==========================================================
# Load Environment
# ==========================================================

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# Environment
# ==========================================================

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development",
)

if ENVIRONMENT not in {"development", "production"}:
    raise ValueError(
        f"Invalid ENVIRONMENT: {ENVIRONMENT}"
    )

DEBUG = os.getenv(
    "DEBUG",
    "True",
).lower() == "true"


# ==========================================================
# LLM
# ==========================================================

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama-3.3-70b-versatile",
)

LLM_TEMPERATURE = float(
    os.getenv(
        "LLM_TEMPERATURE",
        "0",
    )
)


# ==========================================================
# Embedding Model
# ==========================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "models/gemini-embedding-001",
)


# ==========================================================
# Chroma
# ==========================================================

CHROMA_DIR = BASE_DIR / "chroma_db"

DATA_DIR = BASE_DIR / "data"


# ==========================================================
# Uploads
# ==========================================================

UPLOAD_DIR = BASE_DIR / "uploads"


# ==========================================================
# UI
# ==========================================================

APP_TITLE = "Paravartan Healthcare Copilot"


# ==========================================================
# Database
# ==========================================================

if ENVIRONMENT == "development":

    DB_HOST = os.getenv("DB_HOST", "localhost")

    DB_PORT = os.getenv("DB_PORT", "5432")

    DB_NAME = os.getenv("DB_NAME", "hospital_copilot")

    DB_USER = os.getenv("DB_USER", "postgres")

    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

else:

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "",
    )