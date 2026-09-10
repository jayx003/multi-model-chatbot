import streamlit as st

from multi_model_chatbot.models import (
    check_local_ollama,
    get_models,
)
from multi_model_chatbot.ollama_client import generate_response


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Multi-Model AI Chat",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0e1117;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .status-card {
        padding: 12px;
        border-radius: 10px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }

    .online-status {
        color: #3fb950;
        font-weight: 600;
    }

    .offline-status {
        color: #f85149;
        font-weight: 600;
    }

    .neutral-status {
        color: #9ca3af;
        font-weight: 600;
    }

    .model-info {
        padding: 10px 12px;
        border-radius: 8px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-top: 8px;
        color: #9ca3af;
        font-size: 0.85rem;
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


if "selected_model" not in st.session_state:
    st.session_state.selected_model = None


# ============================================================
# CHECK LOCAL OLLAMA STATUS
# ============================================================

local_ollama_online = check_local_ollama()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Settings")

    # --------------------------------------------------------
    # New Chat
    # --------------------------------------------------------

    if st.button(
        "🆕 New Chat",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # LOCAL OLLAMA STATUS
    # --------------------------------------------------------

    st.subheader("💻 Local Ollama")

    if local_ollama_online:

        st.markdown(
            """
            <div class="status-card">
                <span class="online-status">
                    🟢 ONLINE
                </span>
                <br>
                Your local Ollama is running.
                <br>
                <small>
                    Local models are available.
                </small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="status-card">
                <span class="offline-status">
                    🔴 OFFLINE
                </span>
                <br>
                Ollama is not reachable on this PC.
                <br>
                <small>
                    Start Ollama to use local models.
                </small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # --------------------------------------------------------
    # AI PROVIDER
    # --------------------------------------------------------

    st.subheader("AI Provider")

    provider_options = [
        "☁️ Ollama Cloud",
    ]

    # Only make Local Ollama selectable when it is online.
    if local_ollama_online:
        provider_options.append(
            "💻 Local Ollama"
        )

    provider_label = st.radio(
        "Choose provider",
        provider_options,
        label_visibility="collapsed",
    )

    if provider_label == "☁️ Ollama Cloud":
        mode = "cloud"
    else:
        mode = "local"

    st.divider()

    # --------------------------------------------------------
    # LOAD MODELS
    # --------------------------------------------------------

    try:

        models = get_models(
            mode=mode
        )

    except Exception as e:

        models = []

        if mode == "local":

            st.error(
                "Unable to load local models."
            )

        else:

            st.error(
                str(e)
            )

    # --------------------------------------------------------
    # MODEL SELECTOR
    # --------------------------------------------------------

    if models:

        model_names = [
            model["name"]
            for model in models
        ]

        # Make sure selected model exists
        # in the currently selected provider.

        if (
            st.session_state.selected_model
            not in model_names
        ):
            st.session_state.selected_model = (
                model_names[0]
            )

        selected_model = st.selectbox(
            "Model",
            model_names,
            index=model_names.index(
                st.session_state.selected_model
            ),
        )

        st.session_state.selected_model = (
            selected_model
        )

        # ----------------------------------------------------
        # MODEL INFORMATION
        # ----------------------------------------------------

        selected_info = next(
            (
                model
                for model in models
                if model["name"] == selected_model
            ),
            None,
        )

        if selected_info:

            description = selected_info.get(
                "description"
            )

            if description:

                st.markdown(
                    f"""
                    <div class="model-info">
                        <b>
                            {selected_info.get(
                                "display_name",
                                selected_model
                            )}
                        </b>
                        <br>
                        {description}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    else:

        selected_model = None

        if mode == "local":

            st.warning(
                "No local models available."
            )

        else:

            st.warning(
                "No cloud models available."
            )

    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    st.write("")

    if st.button(
        "🔄 Refresh Models",
        use_container_width=True,
    ):
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # CURRENT PROVIDER STATUS
    # --------------------------------------------------------

    st.subheader("Status")

    if mode == "cloud":

        st.markdown(
            """
            <div class="status-card">
                ☁️ <b>Provider</b><br>
                Ollama Cloud
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="status-card">
                ⚡ <b>Inference</b><br>
                Cloud
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="status-card">
                <span class="online-status">
                    🟢 CLOUD AVAILABLE
                </span>
                <br>
                Your PC can be OFF.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="status-card">
                💻 <b>Provider</b><br>
                FastAPI + Local Ollama
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="status-card">
                ⚡ <b>Inference</b><br>
                Local
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="status-card">
                <span class="online-status">
                    🟢 LOCAL ONLINE
                </span>
                <br>
                Running on this PC.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # MODEL COUNT
    # --------------------------------------------------------

    st.write(
        f"**Models available:** {len(models)}"
    )

    st.divider()

    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="app-title">'
    '🤖 Multi-Model AI Chat'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Local + Cloud • Multi-Model AI'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# LOCAL OFFLINE NOTICE
# ============================================================

if not local_ollama_online:

    st.info(
        "💻 Local Ollama is currently offline. "
        "Start Ollama on this PC to use local models. "
        "☁️ Ollama Cloud remains available."
    )


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.messages:

    st.info(
        "👋 Welcome! Select a model from the sidebar "
        "and start chatting."
    )

    st.markdown(
        """
        ### 💡 Try asking

        - Explain machine learning in simple language
        - Write a Python program for a calculator
        - Explain how APIs work
        - Give me project ideas for GenAI
        """
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(role):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Ask anything..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if prompt:

    if not selected_model:

        st.error(
            "Please select an available model first."
        )

        st.stop()

    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            f"Thinking with {selected_model}..."
        ):

            try:

                answer = generate_response(
                    model=selected_model,
                    messages=st.session_state.messages,
                    mode=mode,
                )

                st.markdown(answer)

                # Save assistant response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as e:

                st.error(
                    f"⚠️ {str(e)}"
                )