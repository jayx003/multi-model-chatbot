import httpx


API_URL = "http://127.0.0.1:8000"


def get_models():
    response = httpx.get(
        f"{API_URL}/models",
        timeout=10.0,
    )

    response.raise_for_status()

    return response.json()["models"]