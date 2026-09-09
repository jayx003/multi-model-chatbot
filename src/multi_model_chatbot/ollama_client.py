import httpx


API_URL = "http://127.0.0.1:8000"


def generate_response(model, messages):
    response = httpx.post(
        f"{API_URL}/chat",
        json={
            "model": model,
            "messages": messages,
        },
        timeout=300.0,
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]