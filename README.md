# 🤖 Multi-Model Local AI Chatbot

**A private local AI chatbot for running and interacting with multiple open-source LLMs through Ollama.**

Build, test, and experiment with local AI models through a clean Streamlit interface.  
The application separates the UI from inference using a FastAPI backend.  
It avoids sending prompts to third-party AI services during local inference.

## 🚀 Live Demo

🌐 **Try the deployed application:**

👉 [**Multi-Model AI Chatbot**](https://multi-model-chatbot-003.streamlit.app/)

> **Note:** The deployed Streamlit application requires a reachable AI backend.
> Local Ollama instances are not directly accessible from Streamlit Cloud.

**Repository:** [GitHub Repository](https://github.com/jayx003/multi-model-chatbot)

---

## 🖼️ Project Preview

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/946802c3-d82f-4923-a436-87a3a4d396d7" />

## 🚀 Features

* 🤖 **Multi-model support**

  * Use multiple Ollama models.
  * Switch models from the UI.

* 🔄 **Automatic model detection**

  * Detect installed Ollama models.
  * Refresh the model list from the application.

* 💬 **Interactive chat**

  * Maintain conversation history.
  * Start new conversations instantly.
  * Clear conversations when needed.

* ⚡ **AI response generation**

  * Generate responses through Ollama.
  * Support streaming-style chat interaction.

* 🖥️ **Clean Streamlit interface**

  * Responsive chat interface.
  * Dedicated model selection.
  * Backend status indicators.

* 🚀 **FastAPI backend**

  * Separates UI and inference logic.
  * Provides REST API endpoints.
  * Includes interactive API documentation.

* 🔒 **Local-first architecture**

  * Run inference on your own machine.
  * Keep prompts within your local environment.

* 📦 **Modern dependency management**

  * Uses `uv` for Python dependencies.
  * Uses `uv.lock` for reproducible environments.

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │    User / Browser    │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         │                     │
                         │  Chat + Model UI    │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI Backend  │
                         │                     │
                         │ /models             │
                         │ /chat               │
                         │ /health             │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │       Ollama        │
                         │                     │
                         │ Llama               │
                         │ Qwen                │
                         │ Gemma               │
                         │ Other LLMs           │
                         └─────────────────────┘
```

### Request Flow

```text
User Prompt
     ↓
Streamlit
     ↓
FastAPI /chat
     ↓
Ollama
     ↓
Selected Local LLM
     ↓
FastAPI
     ↓
Streamlit
     ↓
AI Response
```

---

## 🛠️ Tech Stack

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| **Python**    | Core programming language    |
| **Streamlit** | Web-based chat interface     |
| **FastAPI**   | Backend REST API             |
| **Ollama**    | Local LLM inference          |
| **HTTPX**     | HTTP communication           |
| **Pydantic**  | API request validation       |
| **uv**        | Python dependency management |

---

## 📁 Project Structure

```text
multi-model-chatbot/
│
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
├── .devcontainer/
│
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

### Key Components

| File                       | Responsibility          |
| -------------------------- | ----------------------- |
| `backend/main.py`          | FastAPI application     |
| `src/.../main.py`          | Streamlit application   |
| `src/.../models.py`        | Backend model discovery |
| `src/.../ollama_client.py` | Backend communication   |
| `pyproject.toml`           | Project configuration   |
| `uv.lock`                  | Locked dependencies     |

---

## 📦 Prerequisites & Installation

### Prerequisites

| Requirement | Recommended              |
| ----------- | ------------------------ |
| **Python**  | 3.11+                    |
| **Git**     | Latest stable version    |
| **uv**      | Latest stable version    |
| **Ollama**  | Latest stable version    |
| **RAM**     | Depends on selected LLM  |
| **OS**      | Windows, macOS, or Linux |

---

### 1. Clone the Repository

```bash
git clone https://github.com/jayx003/multi-model-chatbot.git
```

Enter the project directory:

```bash
cd multi-model-chatbot
```

---

### 2. Install Dependencies

Using `uv`:

```bash
uv sync
```

This creates or updates the project's Python environment.

---

### 3. Verify Ollama

Check your Ollama installation:

```bash
ollama --version
```

Check installed models:

```bash
ollama list
```

---

### 4. Install an Ollama Model

For example:

```bash
ollama pull llama3.2
```

You can install additional models:

```bash
ollama pull qwen3
```

```bash
ollama pull gemma3
```

Verify them:

```bash
ollama list
```

---

## 💻 Usage

The application uses two processes.

Run the FastAPI backend first.

### Terminal 1 — FastAPI

```bash
uv run uvicorn backend.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Terminal 2 — Streamlit

Open another terminal.

Run:

```bash
uv run streamlit run src/multi_model_chatbot/main.py
```

Open the application:

```text
http://localhost:8501
```

---

## 🔌 API Endpoints

| Method | Endpoint  | Purpose                       |
| ------ | --------- | ----------------------------- |
| `GET`  | `/`       | Backend status                |
| `GET`  | `/health` | Health check                  |
| `GET`  | `/models` | List Ollama models            |
| `POST` | `/chat`   | Generate an AI response       |
| `GET`  | `/docs`   | Interactive API documentation |

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

### Get Installed Models

```bash
curl http://127.0.0.1:8000/models
```

The endpoint returns models available through Ollama.

---

### Chat API Example

Send a request to the backend:

```bash
curl -X POST "http://127.0.0.1:8000/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"llama3.2:latest\",\"messages\":[{\"role\":\"user\",\"content\":\"Explain Python in one sentence.\"}]}"
```

Example request body:

```json
{
  "model": "llama3.2:latest",
  "messages": [
    {
      "role": "user",
      "content": "Explain Python in one sentence."
    }
  ]
}
```

---

## 🔐 Privacy & Security

This project follows a local-first architecture.

Your prompts are processed by Ollama on the local machine.

No external AI provider is required for local inference.

### Never Commit Secrets

Do not commit API keys or credentials.

Use environment variables or local secret files when required.

Example:

```text
OLLAMA_API_KEY=your_secret_key
```

Add secret files to `.gitignore`:

```text
.env
.env.*
.streamlit/secrets.toml
```

> **Security note:** Never publish real API keys in GitHub repositories.

---

## 🔄 Updating the Project

If the repository is already cloned:

```bash
git pull
```

Then synchronize dependencies:

```bash
uv sync
```

Start the application again:

```bash
uv run uvicorn backend.main:app --reload
```

In another terminal:

```bash
uv run streamlit run src/multi_model_chatbot/main.py
```

---

## 🧠 Adding More Models

Ollama supports many open-source models.

Install a model:

```bash
ollama pull <model-name>
```

Example:

```bash
ollama pull llama3.2
```

Check installed models:

```bash
ollama list
```

The application retrieves available models from the FastAPI backend.

---

## 🧪 Development Workflow

Recommended development flow:

```text
1. Start Ollama
       ↓
2. Start FastAPI
       ↓
3. Start Streamlit
       ↓
4. Test the application
       ↓
5. Modify code
       ↓
6. Test again
       ↓
7. Commit changes
       ↓
8. Push to GitHub
```

Git workflow:

```bash
git status
```

```bash
git add .
```

```bash
git commit -m "Update chatbot"
```

```bash
git push
```

---

## 🚀 Future Improvements

Potential enhancements include:

* [ ] True token-by-token streaming
* [ ] Model performance comparison
* [ ] Conversation persistence
* [ ] Chat export
* [ ] Authentication
* [ ] Model-specific settings
* [ ] Temperature controls
* [ ] System prompt configuration
* [ ] File upload support
* [ ] RAG integration
* [ ] Docker deployment
* [ ] Cloud-hosted inference
* [ ] Multi-user support
* [ ] Automated testing
* [ ] CI/CD pipeline

---

## 🤝 Contributing

Contributions are welcome.

### 1. Fork the Repository

Create your own GitHub fork.

### 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/multi-model-chatbot.git
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature
```

### 4. Make Your Changes

Keep changes focused and well documented.

### 5. Test Locally

Run:

```bash
uv sync
```

Then start both services:

```bash
uv run uvicorn backend.main:app --reload
```

```bash
uv run streamlit run src/multi_model_chatbot/main.py
```

### 6. Commit Your Changes

```bash
git add .
git commit -m "Add your feature"
```

### 7. Push Your Branch

```bash
git push origin feature/your-feature
```

### 8. Open a Pull Request

Describe your changes clearly.

Include testing details when relevant.

### Reporting Issues

Before opening an issue:

* Check existing issues.
* Reproduce the problem.
* Include relevant error messages.
* Mention your operating system.
* Mention your Python version.
* Mention your Ollama version.
* Avoid posting API keys or secrets.

---
## ⭐ Project

If this project helps you learn local GenAI development, consider starring the repository.

**Built with Python, Streamlit, FastAPI, Ollama, and `uv`.**
