import streamlit as st

import asyncio

from assistants.chat_assistant import ask_ai

from ui.workflow_status import WorkflowStatus
from copilot.workflow_events import workflow_events

CHAT_HEIGHT = 600


def render_chat():

    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ==========================================
    # OUTER CARD
    # ==========================================

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True) 

    with st.container(border=True):

        # ---------- Header ----------

        col1, col2 = st.columns([5, 1])

        with col1:
            #st.subheader("💬 AI Therapist Assistant")
            # 1. Force the internal Streamlit block container to drop its padding
            st.markdown(
                """
                <style>
                /* Targets the inner block container and shrinks the top spacing */
                [data-testid="stVerticalBlock"] > div:first-child {
                    margin-top: -8px !important;
                }
                /* Shrinks default paragraph/header padding inside the markdown component */
                .stMarkdown div p, .stMarkdown div h3 {
                    margin-top: 0px !important;
                    padding-top: 0px !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # 2. Your header code
            st.markdown(
                "<h3 style='margin-top: -15px; margin-bottom: 0px; padding-top: 0px;'>💬 AI Therapist Assistant</h3>", 
                unsafe_allow_html=True
            )

        with col2:

            st.write("")

            if st.button(
                "➕",
                help="New Chat",
                use_container_width=True,
            ):
                st.session_state.chat_history = []
                workflow_events.clear_all()
                st.session_state.workflow_id = None
                st.rerun()

        # 2. Use custom HTML/CSS instead of st.divider() to force a tight margin
        st.markdown(
    """
    <hr style="
        margin-top: 5px; 
        margin-bottom: 15px; 
        border: none; 
        border-top: 0.5px solid rgba(255, 255, 255, 0.1);
    ">
    """, 
    unsafe_allow_html=True
)


        #st.divider()

        # ---------- Chat Window ----------

        chat_window = st.container(
            height=CHAT_HEIGHT,
            border=False
        )

        with chat_window:

            #if not st.session_state.chat_history:

                # st.info(
                #     "👋 I'm your AI Therapist Assistant. "
                #     " I can help you with therapy planning."
                # )

            for msg in st.session_state.chat_history:

                with st.chat_message(msg["role"]):

                    # ------------------------------------------------
                    # Assistant Workflow
                    # ------------------------------------------------

                    if msg["role"] == "assistant":

                        workflow_id = msg.get(
                            "workflow_id"
                        )

                        if workflow_id:

                            with st.expander(

                                "⚙️ Workflow",

                                expanded=False,

                            ):

                                WorkflowStatus.render(
                                    workflow_id
                                )

                    # ------------------------------------------------
                    # Assistant/User Message
                    # ------------------------------------------------

                    st.markdown(
                        msg["content"]
                    )

        #st.divider()

        # ---------- Chat Input ----------
        # 1. Create a placeholder container ABOVE the chat input component
        #spinner_placeholder = st.container()
        #workflow_placeholder = st.empty()

        prompt = st.chat_input(
            #"Ask the AI Therapist..."
            "👋 I'm your AI Therapist Assistant. I can help you with therapy planning."
        )

        if prompt:

            # -----------------------------------
            # Build Patient Context
            # -----------------------------------

            patient = None

            if st.session_state.selected_patient_id:

                patient = st.session_state.current_patient

            MAX_HISTORY = 6

            history = st.session_state.chat_history[:-1]

            # -----------------------------------
            # Show User Message Immediately
            # -----------------------------------

            st.session_state.chat_history.append(

                {
                    "role": "user",
                    "content": prompt,
                }

            )

            # -----------------------------------
            # Store Pending Prompt
            # -----------------------------------

            st.session_state.pending_prompt = {

                "question": prompt,

                "patient": patient,

                "history": history[-MAX_HISTORY:],

            }

            st.rerun()


        # ==========================================================
        # Execute Pending Prompt
        # ==========================================================

        if st.session_state.pending_prompt:

            pending = st.session_state.pending_prompt

            # -----------------------------------
            # Clear Previous Workflow
            # -----------------------------------

            workflow_events.clear_all()

            st.session_state.workflow_id = None

            # -----------------------------------
            # Execute Copilot
            # -----------------------------------

            from assistants.copilot_assistant import CopilotAssistant

            copilot = CopilotAssistant()

            answer = asyncio.run(

                copilot.ask(

                    question=pending["question"],

                    patient=pending["patient"],

                    chat_history=pending["history"],

                )

            )

            # -----------------------------------
            # Save Assistant Response
            # -----------------------------------

            st.session_state.chat_history.append(

                {

                    "role": "assistant",

                    "content": answer,

                    "workflow_id": st.session_state.get(
                        "workflow_id"
                    ),

                }

            )

            # -----------------------------------
            # Clear Pending Prompt
            # -----------------------------------

            st.session_state.pending_prompt = None

            # -----------------------------------
            # Debug
            # -----------------------------------

            from pprint import pprint

            print("\n========== CHAT HISTORY ==========\n")

            pprint(st.session_state.chat_history)

            print("\n==================================\n")

            st.rerun()