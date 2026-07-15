"""
workflow_events.py

Production Workflow Event Bus.

Responsibilities
----------------
- Store workflow events by workflow id.
- Publish workflow progress.
- Retrieve workflow history.
- Optionally mirror into Streamlit session state.
- Remain usable from tests, CLI and APIs.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

# ----------------------------------------------------------
# Optional Streamlit Support
# ----------------------------------------------------------

try:

    import streamlit as st

    STREAMLIT_AVAILABLE = True

except Exception:

    STREAMLIT_AVAILABLE = False


# ==========================================================
# Workflow Event
# ==========================================================

@dataclass(slots=True)
class WorkflowEvent:

    workflow_id: str

    step: int

    total_steps: int

    skill: str

    task: str

    status: str

    message: str

    timestamp: datetime


# ==========================================================
# Workflow Event Bus
# ==========================================================

class WorkflowEventBus:

    def __init__(self):

        self._events: dict[
            str,
            list[WorkflowEvent],
        ] = defaultdict(list)

    # ------------------------------------------------------

    def publish(
        self,
        *,
        workflow_id: str,
        step: int,
        total_steps: int,
        skill: str,
        task: str,
        status: str,
        message: str,
    ):

        event = WorkflowEvent(

            workflow_id=workflow_id,

            step=step,

            total_steps=total_steps,

            skill=skill,

            task=task,

            status=status,

            message=message,

            timestamp=datetime.now(),

        )

        # -----------------------------------------
        # Internal history
        # -----------------------------------------

        self._events[workflow_id].append(event)

        # -----------------------------------------
        # Optional Streamlit mirror
        # -----------------------------------------

        print("STREAMLIT:", STREAMLIT_AVAILABLE)

        if STREAMLIT_AVAILABLE:

            if "workflow_events" not in st.session_state:

                st.session_state.workflow_events = {}

            st.session_state.workflow_events[
                workflow_id
            ] = self._events[workflow_id]

            st.session_state.current_workflow_id = workflow_id

            st.session_state.current_workflow_event = event

    # ------------------------------------------------------

    def get_history(
        self,
        workflow_id: str,
    ) -> list[WorkflowEvent]:

        return list(

            self._events.get(

                workflow_id,

                [],

            )

        )

    # ------------------------------------------------------

    def latest(
        self,
        workflow_id: str,
    ) -> WorkflowEvent | None:

        events = self._events.get(
            workflow_id
        )

        if not events:

            return None

        return events[-1]

    # ------------------------------------------------------

    def clear(
        self,
        workflow_id: str,
    ):

        self._events.pop(
            workflow_id,
            None,
        )

        if STREAMLIT_AVAILABLE:

            if "workflow_events" in st.session_state:

                st.session_state.workflow_events.pop(
                    workflow_id,
                    None,
                )

    # ------------------------------------------------------

    def clear_all(self):

        self._events.clear()

        if STREAMLIT_AVAILABLE:

            st.session_state.workflow_events = {}

            st.session_state.current_workflow_event = None

            st.session_state.current_workflow_id = None

    # ------------------------------------------------------

    def active_workflows(self) -> list[str]:

        return list(self._events.keys())


# ==========================================================
# Singleton
# ==========================================================

workflow_events = WorkflowEventBus()