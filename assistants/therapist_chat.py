import streamlit as st
from assistants.chat_assistant import ask_ai

CHAT_HEIGHT = 650


def render_chat():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Outer Card
    with st.container(border=True):

        # ---------------- Header ----------------

        col1, col2 = st.columns([5, 1])

        with col1:
            st.subheader("💬 AI Therapist Assistant")

        with col2:

            st.write("")

            if st.button(
                "🗑️",
                help="Clear Chat",
                use_container_width=True,
            ):
                st.session_state.chat_history = []
                st.rerun()

        st.divider()

        # --------------- Chat Window ----------------

        chat_window = st.container(
            height=CHAT_HEIGHT,
            border=False
        )

        with chat_window:

            if not st.session_state.chat_history:

                st.info(
                    "👋 Welcome!\n\n"
                    "I'm your AI Therapist Assistant.\n\n"
                    "Ask me anything about therapy planning."
                )

            for msg in st.session_state.chat_history:

                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        st.divider()

        # --------------- Chat Input ----------------

        prompt = st.chat_input(
            "Ask the AI Therapist..."
        )

        if prompt:

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.spinner("Thinking..."):
                answer = ask_ai(prompt, st.session_state.chat_history)

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.rerun()