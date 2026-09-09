import streamlit as st

from multi_model_chatbot.models import MODELS
from multi_model_chatbot.ollama_client import generate_response


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Multi-model-AI-Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS ONLY
# No custom HTML
# ============================================================

st.markdown(
    """
<style>

    /* App background */
    .stApp {
        background-color: #0b0f14;
    }

    /* Main content width */
    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11161d;
        border-right: 1px solid #252c36;
    }

    /* Sidebar title */
    section[data-testid="stSidebar"] h1 {
        color: #ffffff;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 42px;
        background-color: #171d25;
        border: 1px solid #303845;
        color: #e7ebf0;
    }

    .stButton > button:hover {
        border-color: #6d5dfc;
        color: white;
    }

    /* Selectbox */
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

    /* Horizontal rule */
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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Multi Model AI")

    st.caption("Private multi-model assistant")

    st.divider()

    # New chat
    if st.button("＋  New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Model section
    st.caption("MODEL")

    model_name = st.selectbox(
        "Choose an AI model",
        options=list(MODELS.keys()),
        label_visibility="collapsed",
    )

    selected_model = MODELS[model_name]

    st.divider()

    # Current model
    st.caption("ACTIVE MODEL")

    st.info(
        f"🧠 **{model_name}**\n\n"
        f"`{selected_model}`"
    )

    # Backend
    st.caption("BACKEND")

    st.success("🟢 Ollama")

    # Inference
    st.caption("INFERENCE")

    st.info("🔒 Running locally")

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by Ollama + Streamlit")


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🤖 Multi Model AI Chat")

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

    st.markdown("## ✨ What can I help you with?")

    st.write(
        "Ask questions, write code, learn new topics, "
        "debug problems, or explore ideas with your local AI."
    )

    st.write("")

    # Suggestion buttons
    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💡 Explain something",
            use_container_width=True,
        ):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Explain artificial intelligence in simple words.",
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
                    "content": "Teach me an interesting Python concept.",
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
                    "content": "Show me a useful Python project idea.",
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
                    "content": "What are some interesting things you can help me with?",
                }
            )
            st.rerun()

    st.write("")
    st.write("")


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Message your AI assistant..."
)


if prompt:

    # User message
    with st.chat_message(
        "user",
        avatar="👤",
    ):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Assistant
    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        try:

            response = st.write_stream(
                generate_response(
                    selected_model,
                    st.session_state.messages,
                )
            )

        except Exception as e:

            response = (
                "❌ **Error communicating with Ollama**\n\n"
                f"`{e}`\n\n"
                "Make sure Ollama is running and the selected "
                "model is installed."
            )

            st.error(response)

    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )