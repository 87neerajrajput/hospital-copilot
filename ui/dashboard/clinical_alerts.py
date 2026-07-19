import streamlit as st

from ui.dashboard.clinical_alerts_analyzer import (
    ClinicalAlertsAnalyzer,
)


class ClinicalAlerts:

    @staticmethod
    def render(plans, latest_plan, previous_plan):

        with st.container(border=True):

            st.subheader("🚨 Clinical Alerts")

            alerts = ClinicalAlertsAnalyzer.generate(

                plans,

                latest_plan,

                previous_plan,

            )

            if not alerts:

                st.success(
                    "No clinical alerts.\n\n"
                    "Patient is progressing without any system-detected concerns."
                )

                return

            for alert in alerts:

                content = (
                    f"**{alert['title']}**\n\n"
                    f"{alert['message']}"
                )

                if alert["type"] == "error":

                    st.error(content)

                elif alert["type"] == "warning":

                    st.warning(content)

                elif alert["type"] == "success":

                    st.success(content)

                else:

                    st.info(content)