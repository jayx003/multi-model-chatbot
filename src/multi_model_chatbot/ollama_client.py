import os

import httpx
import streamlit as st


# ============================================================
# API URLs
# ============================================================

LOCAL_API_URL = "http://127.0.0.1:8000"
CLOUD_API_URL = "https://ollama.com/api"


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
# GENERATE RESPONSE
# ============================================================

def generate_response(model, messages, mode="local"):
    """
    Generate an AI response using either:

    - Local FastAPI + Ollama
    - Ollama Cloud
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

        try:

            response = httpx.post(
                f"{CLOUD_API_URL}/chat",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                },
                timeout=300.0,
            )

            # ------------------------------------------------
            # Paid model / insufficient free credits
            # ------------------------------------------------

            if response.status_code == 402:

                raise RuntimeError(
                    f"Model '{model}' requires paid Ollama "
                    "usage credits or is no longer included "
                    "in the Free tier."
                )

            # ------------------------------------------------
            # Authentication
            # ------------------------------------------------

            if response.status_code == 401:

                raise RuntimeError(
                    "Ollama Cloud API key is invalid or expired."
                )

            # ------------------------------------------------
            # Rate limit
            # ------------------------------------------------

            if response.status_code == 429:

                raise RuntimeError(
                    "Ollama Cloud Free-tier limit has been "
                    "reached. Please try again later."
                )

            response.raise_for_status()

            data = response.json()

            return data["message"]["content"]

        except httpx.TimeoutException:

            raise RuntimeError(
                "Ollama Cloud request timed out. "
                "Please try again."
            )

        except httpx.ConnectError:

            raise RuntimeError(
                "Could not connect to Ollama Cloud."
            )

    # ========================================================
    # LOCAL MODE
    # ========================================================

    try:

        response = httpx.post(
            f"{LOCAL_API_URL}/chat",
            json={
                "model": model,
                "messages": messages,
            },
            timeout=300.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except httpx.ConnectError:

        raise RuntimeError(
            "Could not connect to the local FastAPI backend. "
            "Make sure the backend is running."
        )

    except httpx.TimeoutException:

        raise RuntimeError(
            "Local model request timed out."
        )