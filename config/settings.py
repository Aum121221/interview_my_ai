# config/settings.py

# Imports
from pathlib import Path

import streamlit as st


# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

VAULT_ROOT = Path(r"C:\OBSIDIAN")

SOURCE_MAP_FILE = (
    PROJECT_ROOT
    / "config"
    / "source_map.json"
)

KNOWLEDGE_FILE = (
    PROJECT_ROOT
    / "data"
    / "knowledge.jsonl"
)


# Application Configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

DEFAULT_MODEL_TEMPERATURE = 0.2

DEFAULT_MODEL_MAX_TOKENS = 700

DEFAULT_MAX_AGENT_STEPS = 5


# API Keys
def get_openrouter_model() -> str:
    """Return the OpenRouter model ID."""
    return st.secrets["OPENROUTER_MODEL"]


def get_openrouter_api_key() -> str:
    """Return the OpenRouter API key."""
    return st.secrets["OPENROUTER_API_KEY"]


def get_gemini_api_key() -> str:
    """Return the Gemini API key."""
    return st.secrets["GEMINI_API_KEY"]


def get_supabase_url() -> str:
    """Return the Supabase project URL."""
    return st.secrets["SUPABASE_URL"]


def get_supabase_key() -> str:
    """Return the Supabase API key."""
    return st.secrets["SUPABASE_KEY"]


# Embeddings
EMBEDDING_MODEL = "gemini-embedding-2"

EMBEDDING_DIMENSION = 768


# Retrieval
DEFAULT_TOP_K = 5

DEFAULT_SIMILARITY_THRESHOLD = 0.25
