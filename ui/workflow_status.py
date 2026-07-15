import streamlit as st

from copilot.workflow_events import workflow_events


class WorkflowStatus:

    @staticmethod
    def render(
        workflow_id: str,
    ):
        
        print("UI EventBus:", id(workflow_events))
        print(workflow_events.active_workflows())

        events = workflow_events.get_history(
            workflow_id
        )

        if not events:
            return

        latest = events[-1]

        WorkflowStatus._render_progress(
            latest
        )

        WorkflowStatus._render_timeline(
            events
        )

    # --------------------------------------------------
    # Progress
    # --------------------------------------------------

    @staticmethod
    def _render_progress(
        latest,
    ):

        progress = (
            latest.step / latest.total_steps
            if latest.total_steps
            else 0
        )

        st.progress(progress)

        st.caption(

            f"Step {latest.step} of {latest.total_steps}"

        )

    # --------------------------------------------------
    # Timeline
    # --------------------------------------------------

    @staticmethod
    def _render_timeline(
        events,
    ):

        with st.container(
            border=True,
        ):

            st.markdown(
                "###### 🏥 Workflow Execution"
            )

            for event in events:

                icon = WorkflowStatus._icon(
                    event.status
                )

                st.markdown(

                    f"{icon} {event.message}"

                )

    # --------------------------------------------------
    # Icons
    # --------------------------------------------------

    @staticmethod
    def _icon(
        status: str,
    ):

        mapping = {

            "running": "🔄",

            "completed": "✅",

            "waiting": "⏳",

            "failed": "❌",

        }

        return mapping.get(
            status,
            "•",
        )