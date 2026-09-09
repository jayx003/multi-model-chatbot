# 🤖 Multi-Model Local AI Chatbot

A **private, multi-model AI chatbot** built with **Python, Streamlit, FastAPI, and Ollama**. It provides a web interface for interacting with locally installed open-source LLMs.

## ✨ Features

- 🤖 Support for multiple Ollama models
- 🔄 Automatic detection of installed models
- 💬 Session-based chat history
- ⚡ Streaming AI responses
- 🖥️ Clean Streamlit UI
- 🚀 FastAPI backend
- 🔒 Local/private AI inference
- 📦 Dependency management with `uv`

## 🏗️ Architecture

```text
Streamlit UI
     │
     │ HTTP
     ▼
FastAPI Backend
     │
     ▼
Ollama
     │
     ├── Llama
     ├── Qwen
     ├── Gemma
     └── Other Models
```

## 📁 Project Structure

```text
multi-model-chatbot/
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── src/
│   └── multi_model_chatbot/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       └── ollama_client.py
│
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## 🚀 Run Locally

Make sure **Ollama** is installed and running.

Install dependencies:

```powershell
uv sync
```

Start the FastAPI backend:

```powershell
uv run uvicorn backend.main:app --reload
```

In another terminal, start Streamlit:

```powershell
uv run streamlit run src/multi_model_chatbot/main.py
```

Open the application:

```text
http://localhost:8501
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## 🧠 Adding Models

Install any compatible Ollama model:

```powershell
ollama pull llama3.2
ollama pull qwen3
```

The chatbot automatically detects installed Ollama models through the FastAPI backend.

Check installed models:

```powershell
ollama list
```

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **FastAPI**
- **Ollama**
- **HTTPX**
- **uv**

## 🔐 Privacy

AI inference runs locally through Ollama, so your prompts and responses do not need to be sent to a third-party AI API.

---

Built as a **local-first GenAI application** for experimenting with and comparing multiple open-source LLMs.
