import os

import httpx
import streamlit as st


# ============================================================
# API URLs
# ============================================================

LOCAL_API_URL = "http://127.0.0.1:8000"
OLLAMA_LOCAL_URL = "http://127.0.0.1:11434"

CLOUD_API_URL = "https://ollama.com/api"


# ============================================================
# FREE OLLAMA CLOUD MODELS
# ============================================================

FREE_CLOUD_MODELS = [
    {
        "name": "gpt-oss:20b-cloud",
        "display_name": "GPT-OSS 20B",
        "description": "Reasoning, coding and general tasks",
    },
    {
        "name": "gpt-oss:120b-cloud",
        "display_name": "GPT-OSS 120B",
        "description": "Stronger reasoning and coding",
    },
    {
        "name": "nemotron-3-nano:30b-cloud",
        "display_name": "Nemotron 3 Nano 30B",
        "description": "Fast reasoning and agent tasks",
    },
    {
        "name": "gemma4:31b-cloud",
        "display_name": "Gemma 4 31B",
        "description": "General tasks and multimodal capability",
    },
    {
        "name": "nemotron-3-super:cloud",
        "display_name": "Nemotron 3 Super",
        "description": "Advanced reasoning and agent tasks",
    },
    {
        "name": "nemotron-3-ultra:cloud",
        "display_name": "Nemotron 3 Ultra",
        "description": "Large-scale reasoning",
    },
]


# ============================================================
# DETECT STREAMLIT CLOUD
# ============================================================

def is_streamlit_cloud():
    """
    Detect whether the app is running on Streamlit Cloud.

    Returns:
        True  -> Running on Streamlit Cloud
        False -> Running locally
    """

    return os.getenv("STREAMLIT_SHARING_MODE") == "streamlit"


# ============================================================
# CLOUD API KEY
# ============================================================

def get_cloud_api_key():
    """
    Get Ollama Cloud API key from Streamlit secrets
    or environment variables.
    """

    try:
        return st.secrets["OLLAMA_API_KEY"]
    except Exception:
        return os.getenv("OLLAMA_API_KEY")


# ============================================================
# CHECK LOCAL OLLAMA
# ============================================================

def check_local_ollama():
    """
    Check whether Ollama is running on the same machine
    as the Streamlit application.

    Returns:
        True  -> Ollama is online
        False -> Ollama is offline
        None  -> Streamlit Cloud
    """

    # A Streamlit Cloud server cannot access Ollama
    # installed on the user's personal laptop.
    if is_streamlit_cloud():
        return None

    try:
        response = httpx.get(
            OLLAMA_LOCAL_URL,
            timeout=2.0,
        )

        return response.status_code == 200

    except httpx.RequestError:
        return False


# ============================================================
# GET LOCAL MODELS
# ============================================================

def get_local_models():
    """
    Get locally installed Ollama models through FastAPI.
    """

    response = httpx.get(
        f"{LOCAL_API_URL}/models",
        timeout=5.0,
    )

    response.raise_for_status()

    return response.json()["models"]


# ============================================================
# GET MODELS
# ============================================================

def get_models(mode="local"):
    """
    Get models for Local Ollama or Ollama Cloud.
    """

    # ========================================================
    # CLOUD MODE
    # ========================================================

    if mode == "cloud":

        api_key = get_cloud_api_key()

        if not api_key:
            raise RuntimeError(
                "OLLAMA_API_KEY is not configured."
            )

        return [
            {
                "name": model["name"],
                "display_name": model["display_name"],
                "description": model["description"],
                "size": 0,
            }
            for model in FREE_CLOUD_MODELS
        ]

    # ========================================================
    # LOCAL MODE
    # ========================================================

    return get_local_models()