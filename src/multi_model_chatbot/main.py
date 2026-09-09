import streamlit as st

from multi_model_chatbot.models import get_models
from multi_model_chatbot.ollama_client import generate_response


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Local AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #0b0f14;
    }

    /* Main content width */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11161d;
        border-right: 1px solid #252c36;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 42px;
        background-color: #171d25;
        border: 1px solid #303845;
        color: #e7ebf0;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        border-color: #6d5dfc;
        color: white;
    }

    /* Select box */
    div[data-baseweb="select"] > div {
        background-color: #171d25;
        border-color: #303845;
        border-radius: 10px;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        border-radius: 14px;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        padding-top: 12px;
        padding-bottom: 12px;
    }

    /* Dividers */
    hr {
        border-color: #252c36;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# LOAD MODELS FROM FASTAPI
# ============================================================

try:
    available_models = get_models()

except Exception as e:

    st.error(
        "❌ Could not connect to the FastAPI backend."
    )

    st.code(str(e))

    st.info(
        "Make sure FastAPI is running on "
        "http://127.0.0.1:8000"
    )

    st.stop()


# ============================================================
# CHECK MODELS
# ============================================================

if not available_models:

    st.warning(
        "⚠️ No Ollama models are installed."
    )

    st.info(
        "Install a model using the Ollama terminal, "
        "then click Refresh Models."
    )

    st.stop()


# ============================================================
# CREATE MODEL OPTIONS
# ============================================================

model_options = {
    model["display_name"]: model["name"]
    for model in available_models
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Local AI")

    st.caption("Private multi-model assistant")

    st.divider()

    # --------------------------------------------------------
    # New Chat
    # --------------------------------------------------------

    if st.button(
        "＋  New Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # Model Selection
    # --------------------------------------------------------

    st.caption("MODEL")

    model_name = st.selectbox(
        "Choose model",
        options=list(model_options.keys()),
        label_visibility="collapsed",
    )

    selected_model = model_options[model_name]

    # --------------------------------------------------------
    # Refresh Models
    # --------------------------------------------------------

    if st.button(
        "🔄 Refresh Models",
        use_container_width=True,
    ):

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # Active Model
    # --------------------------------------------------------

    st.caption("ACTIVE MODEL")

    st.info(
        f"🧠 **{model_name}**\n\n"
        f"`{selected_model}`"
    )

    # --------------------------------------------------------
    # Number of Models
    # --------------------------------------------------------

    st.caption("AVAILABLE MODELS")

    st.metric(
        label="Installed",
        value=len(available_models),
    )

    # --------------------------------------------------------
    # Backend
    # --------------------------------------------------------

    st.caption("BACKEND")

    st.success("🟢 FastAPI + Ollama")

    # --------------------------------------------------------
    # Inference
    # --------------------------------------------------------

    st.caption("INFERENCE")

    st.info("🔒 Running locally")

    st.divider()

    # --------------------------------------------------------
    # Clear Conversation
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "Powered by Ollama + FastAPI + Streamlit"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🤖 Local AI Chat")

st.caption(
    "Private • Local • Multi-Model"
)

st.write(
    f"🟢 **{model_name}**  ·  Ollama"
)

st.divider()


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        "## ✨ What can I help you with?"
    )

    st.write(
        "Ask questions, write code, learn new topics, "
        "debug problems, or explore ideas with your "
        "local AI models."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💡 Explain something",
            use_container_width=True,
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": (
                        "Explain artificial intelligence "
                        "in simple words."
                    ),
                }
            )

            st.rerun()

        if st.button(
            "🐍 Help me with Python",
            use_container_width=True,
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": (
                        "Teach me an interesting "
                        "Python concept."
                    ),
                }
            )

            st.rerun()

    with col2:

        if st.button(
            "💻 Write some code",
            use_container_width=True,
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": (
                        "Show me a useful Python "
                        "project idea."
                    ),
                }
            )

            st.rerun()

        if st.button(
            "🧠 Ask a question",
            use_container_width=True,
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": (
                        "What are some interesting "
                        "things you can help me with?"
                    ),
                }
            )

            st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":
        avatar = "👤"
    else:
        avatar = "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Message your AI assistant..."
)


# ============================================================
# HANDLE USER MESSAGE
# ============================================================

if prompt:

    # --------------------------------------------------------
    # Display User Message
    # --------------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # --------------------------------------------------------
    # Generate AI Response
    # --------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        try:

            with st.spinner(
                f"{model_name} is thinking..."
            ):

                response = generate_response(
                    selected_model,
                    st.session_state.messages,
                )

            st.markdown(response)

        except Exception as e:

            response = (
                "❌ **Could not generate a response.**"
            )

            st.error(response)

            st.code(
                str(e),
                language="text",
            )

    # --------------------------------------------------------
    # Save Assistant Response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )