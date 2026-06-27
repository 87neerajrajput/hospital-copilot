import streamlit as st

from assistants.chat_assistant import ask_ai

CHAT_HEIGHT = 650


def render_chat():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ==========================================
    # OUTER CARD
    # ==========================================

    with st.container(border=True):

        # ---------- Header ----------

        col1, col2 = st.columns([5, 1])

        with col1:
            st.subheader("💬 AI Therapist Assistant")

        with col2:

            st.write("")

            if st.button(
                "🗑️",
                help="New Chat",
                use_container_width=True,
            ):
                st.session_state.chat_history = []
                st.rerun()

        st.divider()

        # ---------- Chat Window ----------

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

        # ---------- Chat Input ----------

        prompt = st.chat_input(
            "Ask the AI Therapist..."
        )

        if prompt:

            # -----------------------------------
            # Show User Message
            # -----------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            # -----------------------------------
            # Build Patient Context
            # -----------------------------------

            patient = None

            if st.session_state.selected_patient_id:

                patient = {

                    "name": st.session_state.patient_name,

                    "age": st.session_state.age,

                    "diagnosis": st.session_state.diagnosis,

                    "concerns": (
                        st.session_state
                        .primary_concerns
                        .split("\n")
                    ),

                    "therapy_plan": (
                        st.session_state
                        .therapy_plan_summary
                    )
                }

            # -----------------------------------
            # AI Response
            # -----------------------------------

            with st.spinner("Thinking..."):

                answer = ask_ai(
                    question=prompt,
                    patient=patient,
                )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.rerun()