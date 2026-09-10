# 🤖 Multi-Model Local AI Chatbot

### Chat with multiple open-source LLMs locally using Ollama, FastAPI & Streamlit.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-black)](https://ollama.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://docs.astral.sh/uv/)

> A local-first Generative AI application that provides a web-based chat interface for interacting with multiple Ollama-hosted open-source Large Language Models (LLMs).

## 🚀 Live Demo

**Try the deployed application:**

👉 **https://multi-model-chatbot-003.streamlit.app/**

> **Note:** The live Streamlit deployment is primarily intended for demonstrating the application interface. Local execution is recommended when using Ollama-hosted models directly on your own machine.

---

## 📸 Application Preview

<!-- Add your application screenshot here -->

<img width="1920" height="929" alt="image" src="https://github.com/user-attachments/assets/21484727-7e2a-4246-b84a-54fe0263c42a" />

## 🎯 Why This Project?

Modern LLM applications often depend on cloud-based APIs.

This project explores a different approach:

**Run open-source LLMs locally through Ollama and expose them through a clean application architecture.**

The application separates the user interface, API layer, and model-inference layer:

```text
User
  │
  ▼
┌──────────────────────┐
│    Streamlit UI      │
│   Chat Interface     │
└──────────┬───────────┘
           │ HTTP
           ▼
┌──────────────────────┐
│    FastAPI Backend   │
│                      │
│ • Model Discovery    │
│ • Chat Requests      │
│ • API Communication  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Ollama         │
│   Local LLM Runtime  │
└──────────┬───────────┘
           │
      ┌────┼────┬─────┐
      ▼    ▼    ▼     ▼
    Llama Qwen Gemma  Other
```

This architecture keeps the frontend and model-inference logic separated while allowing different locally available models to be accessed through the same application.

---

# ✨ Features

### 🤖 Multi-Model Support

Interact with multiple models available through Ollama.

Examples include:

* Llama
* Qwen
* Gemma
* Other Ollama-compatible models

The application does not require models to be hard-coded into the UI.

---

### 🔍 Automatic Model Discovery

The backend communicates with Ollama to discover models installed on the local machine.

For example:

```bash
ollama list
```

The available models can then be exposed to the chatbot through the FastAPI backend.

---

### 💬 Session-Based Chat

Maintain conversation history within a chat session, allowing the application to behave like a conventional conversational AI assistant.

---

### ⚡ Streaming Responses

AI responses can be streamed progressively rather than waiting for the entire response to be generated.

Conceptually:

```text
User Prompt
     │
     ▼
Streamlit
     │
     ▼
FastAPI
     │
     ▼
Ollama
     │
     ▼
Generated Response
     │
     ├── Chunk 1
     ├── Chunk 2
     ├── Chunk 3
     ├── ...
     ▼
Streamlit UI
```

This provides a more responsive chat experience.

---

### 🔒 Local-First AI

When using locally hosted Ollama models, inference can run on the user's own machine without requiring prompts to be sent to a third-party cloud LLM API.

This makes the project useful for experimenting with local and privacy-conscious GenAI workflows.

---

### 🖥️ Streamlit Interface

A lightweight web interface provides:

* Model selection
* Chat interaction
* Conversation history
* Streaming responses
* Easy experimentation with different local models

---

### 🚀 FastAPI Backend

FastAPI acts as the application/service layer between the Streamlit frontend and Ollama.

Responsibilities include:

* API request handling
* Model discovery
* Communication with Ollama
* Chat request processing
* Streaming responses

---

# 🏗️ Architecture

The application follows a simple three-layer architecture:

```text
┌─────────────────────────────────────────┐
│              Presentation               │
│                                         │
│              Streamlit UI               │
└────────────────────┬────────────────────┘
                     │
                     │ HTTP
                     ▼
┌─────────────────────────────────────────┐
│              API Layer                  │
│                                         │
│              FastAPI                    │
│                                         │
│   Model Discovery │ Chat │ Streaming    │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│           LLM / Inference Layer         │
│                                         │
│                Ollama                   │
│                                         │
│  Llama │ Qwen │ Gemma │ Other Models    │
└─────────────────────────────────────────┘
```

### Why FastAPI?

FastAPI provides a dedicated backend layer instead of coupling the Streamlit interface directly to the Ollama client.

This separation makes it easier to:

* Keep UI and backend logic independent
* Expose reusable API endpoints
* Handle model discovery
* Implement streaming
* Extend the application in the future
* Replace or expand the frontend without rewriting the inference layer

---

# 📁 Project Structure

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

| Component                                  | Responsibility                         |
| ------------------------------------------ | -------------------------------------- |
| `src/multi_model_chatbot/main.py`          | Streamlit application                  |
| `src/multi_model_chatbot/models.py`        | Application/model-related definitions  |
| `src/multi_model_chatbot/ollama_client.py` | Ollama communication                   |
| `backend/main.py`                          | FastAPI application and API layer      |
| `pyproject.toml`                           | Project configuration and dependencies |
| `uv.lock`                                  | Reproducible dependency locking        |

---

# 🛠️ Tech Stack

| Technology    | Purpose                                      |
| ------------- | -------------------------------------------- |
| **Python**    | Core programming language                    |
| **Streamlit** | Web-based chatbot interface                  |
| **FastAPI**   | Backend/API layer                            |
| **Ollama**    | Local LLM runtime                            |
| **HTTPX**     | HTTP communication                           |
| **uv**        | Python dependency and environment management |

---

# ⚙️ Prerequisites

Before running the project locally, install:

1. **Python**
2. **Ollama**
3. **uv**

You can verify the installations:

```bash
python --version
```

```bash
ollama --version
```

```bash
uv --version
```

---

# 📥 Installation

## 1. Clone the repository

```bash
git clone https://github.com/jayx003/multi-model-chatbot.git
```

```bash
cd multi-model-chatbot
```

---

## 2. Install dependencies

Using `uv`:

```bash
uv sync
```

This creates/uses the project environment and installs the dependencies defined by the project.

---

# 🧠 Set Up Ollama

Make sure Ollama is installed and running.

Then pull at least one model.

For example:

```bash
ollama pull llama3.2
```

You can also install additional models:

```bash
ollama pull qwen3
```

```bash
ollama pull gemma3
```

Check the installed models:

```bash
ollama list
```

Example:

```text
NAME              SIZE
llama3.2:latest   ...
qwen3:latest      ...
gemma3:latest     ...
```

The application can detect the models available through Ollama.

---

# ▶️ Running the Application

The application consists of two services:

```text
FastAPI Backend
      +
Streamlit Frontend
```

Both should be running locally.

## Terminal 1 — Start FastAPI

```bash
uv run uvicorn backend.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Terminal 2 — Start Streamlit

```bash
uv run streamlit run src/multi_model_chatbot/main.py
```

The application will normally be available at:

```text
http://localhost:8501
```

Open the URL in your browser and start chatting with your locally available models.

---

# 🔄 Application Workflow

A typical request follows this flow:

```text
1. User selects an Ollama model
              │
              ▼
2. User enters a prompt
              │
              ▼
3. Streamlit sends request
              │
              ▼
4. FastAPI receives request
              │
              ▼
5. FastAPI communicates with Ollama
              │
              ▼
6. Ollama generates response
              │
              ▼
7. Response is streamed back
              │
              ▼
8. Streamlit displays response
```

---

# 🔐 Privacy & Local Inference

This project is designed around a **local-first LLM architecture**.

When Ollama is running locally:

```text
Your Prompt
    │
    ▼
Local FastAPI
    │
    ▼
Local Ollama
    │
    ▼
Local LLM
```

No external LLM API is inherently required for the inference process.

However, privacy depends on the complete environment in which the application is deployed and operated.

---

# 🧪 Example Models

The application can work with any compatible model available through Ollama.

Some examples:

```bash
ollama pull llama3.2
ollama pull qwen3
ollama pull gemma3
```

Then:

```bash
ollama list
```

The application can use the models exposed by the local Ollama runtime.

> Model availability and hardware requirements vary depending on the model.

---

# 💡 Use Cases

This project can be used for:

* 🧪 Experimenting with different open-source LLMs
* 🤖 Building local AI assistants
* 🔍 Comparing model behavior
* 📚 Learning LLM application development
* 🏠 Running AI workloads locally
* 🔐 Exploring privacy-conscious GenAI architectures
* ⚙️ Learning frontend/backend separation in AI applications

---

# 🚧 Future Improvements

Planned or potential improvements include:

* [ ] Side-by-side model comparison
* [ ] Model performance benchmarking
* [ ] Token/response latency metrics
* [ ] Persistent conversation storage
* [ ] Conversation export
* [ ] Custom system prompts
* [ ] Temperature and generation controls
* [ ] Authentication
* [ ] Docker deployment
* [ ] Automated testing
* [ ] GitHub Actions CI/CD
* [ ] Improved error handling
* [ ] Model metadata and capability display
* [ ] RAG support
* [ ] Document upload and question answering
* [ ] Multi-user support

---

# 🧪 Development

Install the project in development mode using:

```bash
uv sync
```

Run the backend:

```bash
uv run uvicorn backend.main:app --reload
```

Run the frontend:

```bash
uv run streamlit run src/multi_model_chatbot/main.py
```

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

### Basic workflow

```bash
git clone https://github.com/jayx003/multi-model-chatbot.git
```

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Make your changes and commit:

```bash
git add .
git commit -m "feat: add your feature"
```

Push the branch:

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📄 License

This project is intended for educational, experimental, and portfolio purposes.

Add an explicit open-source license such as **MIT** if you want others to legally reuse and modify the code.

---

# 👨‍💻 Author

**Jayesh Patil**

AI/ML • Generative AI • Python • LLM Applications

GitHub:
https://github.com/jayx003

Project:
https://github.com/jayx003/multi-model-chatbot

Live Demo:
https://multi-model-chatbot-003.streamlit.app/

---

# ⭐ Support

If you find this project useful or interesting:

⭐ **Star the repository**

🍴 **Fork it**

🐛 **Open an issue**

💡 **Suggest an improvement**

---

## 📌 Project Summary

**Multi-Model Local AI Chatbot** demonstrates how a modern Generative AI application can be built around locally hosted open-source LLMs.

The project combines:

```text
Streamlit
    +
FastAPI
    +
Ollama
    +
Open-Source LLMs
    +
Python
```

to create a modular, local-first conversational AI application.

---

### Built with Python 🐍 • FastAPI ⚡ • Streamlit 🎈 • Ollama 🦙
