from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx


app = FastAPI(
    title="Multi-Model AI API",
    description="FastAPI backend for Ollama chatbot",
    version="1.0.0",
)


OLLAMA_URL = "http://127.0.0.1:11434"


# ============================================================
# Request model
# ============================================================

class ChatRequest(BaseModel):
    model: str
    messages: list[dict]


# ============================================================
# Root
# ============================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Multi-Model AI API",
    }


# ============================================================
# Health
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# ============================================================
# Get Ollama models
# ============================================================

@app.get("/models")
def get_models():

    try:

        response = httpx.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=10.0,
        )

        response.raise_for_status()

        data = response.json()

        models = []

        for model in data.get("models", []):

            models.append(
                {
                    "name": model.get("name"),
                    "display_name": model.get("name"),
                    "size": model.get("size", 0),
                }
            )

        return {
            "models": models
        }

    except httpx.ConnectError:

        raise HTTPException(
            status_code=503,
            detail="Could not connect to Ollama. Make sure Ollama is running.",
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# Chat
# ============================================================

@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    try:

        response = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": request.model,
                "messages": request.messages,
                "stream": False,
            },
            timeout=300.0,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "model": request.model,
            "response": data["message"]["content"],
        }

    except httpx.ConnectError:

        raise HTTPException(
            status_code=503,
            detail="Could not connect to Ollama. Make sure Ollama is running.",
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )