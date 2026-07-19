import streamlit as st
from ui.dashboard.dashboard_analyzer import DashboardAnalyzer

class AIInsights:

    @staticmethod
    def render(plan):

        with st.container(border=True):

            st.subheader("🧠 AI Insights")

            insights = DashboardAnalyzer.generate(plan)

            if not insights:

                st.info("No insights available.")
                return

            for insight in insights:

                content = (
                    f"{insight['icon']} **{insight['title']}**\n\n"
                    f"{insight['message']}"
                )

                if insight["type"] == "success":

                    st.success(content)

                elif insight["type"] == "warning":

                    st.warning(content)

                elif insight["type"] == "error":

                    st.error(content)

                else:

                    st.info(content)