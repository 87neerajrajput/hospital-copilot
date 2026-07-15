import streamlit as st

from datetime import timedelta

from copilot.workflow_events import workflow_events


class WorkflowStatus:

    @staticmethod
    def render(
        workflow_id: str,
    ):

        events = workflow_events.get_history(
            workflow_id
        )

        if not events:
            return

        latest = events[-1]

        WorkflowStatus._render_header(
            latest,
            events,
        )

        WorkflowStatus._render_timeline(
            events
        )

        WorkflowStatus._render_footer(
            events
        )

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    @staticmethod
    def _render_header(
        latest,
        events,
    ):

        progress = (
            latest.step / latest.total_steps
            if latest.total_steps
            else 0
        )

        status = latest.status.lower()

        if status == "running":

            st.progress(progress)

            st.caption(
                f"Executing step {latest.step} of {latest.total_steps}"
            )

        elif status == "waiting":

            st.warning("Waiting for therapist approval")

        elif status == "failed":

            st.error("Workflow failed")

        else:

            st.success("Workflow completed")

    # --------------------------------------------------
    # Timeline
    # --------------------------------------------------

    @staticmethod
    def _render_timeline(
        events,
    ):

        st.markdown("#### 🧠 AI Execution")

        for event in events:

            badge = WorkflowStatus._badge(
                event.status
            )

            ts = event.timestamp.strftime("%H:%M:%S")

            st.markdown(
                f"""
    <div style="
    padding:12px 14px;
    margin-bottom:10px;
    border-radius:10px;
    border:1px solid rgba(255,255,255,.08);
    background:rgba(255,255,255,.02);
    ">

    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    ">

    <div style="display:flex;align-items:center;gap:10px;">

    {badge}

    <span style="
    font-weight:600;
    font-size:15px;
    ">
    {event.message}
    </span>

    </div>

    <div style="
    font-size:12px;
    opacity:.55;
    ">
    {ts}
    </div>

    </div>

    </div>
    """,
                unsafe_allow_html=True,
            )


    @staticmethod
    def _badge(
        status: str,
    ):

        styles = {

            "running": (
                "#2563eb",
                "Running",
            ),

            "completed": (
                "#16a34a",
                "Done",
            ),

            "waiting": (
                "#d97706",
                "Waiting",
            ),

            "failed": (
                "#dc2626",
                "Failed",
            ),

        }

        color, text = styles.get(

            status.lower(),

            ("#6b7280", "Info"),

        )

        return f"""
    <span style="
    background:{color};
    color:white;
    padding:2px 8px;
    border-radius:999px;
    font-size:11px;
    font-weight:600;
    min-width:70px;
    display:inline-block;
    text-align:center;
    ">
    {text}
    </span>
    """

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------

    @staticmethod
    def _render_footer(
        events,
    ):

        if len(events) < 2:
            return

        duration = (
            events[-1].timestamp
            - events[0].timestamp
        )

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:

            st.caption(
                f"⏱ Duration: {WorkflowStatus._format_duration(duration)}"
            )

        with c2:

            st.caption(
                f"📋 {len(events)} events"
            )

    # --------------------------------------------------
    # Icons
    # --------------------------------------------------

    @staticmethod
    def _icon(
        status: str,
    ):

        return {

            "running": "🔄",

            "completed": "✅",

            "waiting": "⏳",

            "failed": "❌",

        }.get(status, "•")

    # --------------------------------------------------
    # Duration
    # --------------------------------------------------

    @staticmethod
    def _format_duration(
        duration: timedelta,
    ):

        ms = duration.total_seconds()

        if ms < 1:

            return f"{int(ms*1000)} ms"

        return f"{ms:.2f} sec"