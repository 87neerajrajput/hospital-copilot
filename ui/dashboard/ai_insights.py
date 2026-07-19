import streamlit as st

class AIInsights:

    @staticmethod
    def render(summary):

        with st.container():

            st.subheader("🧠 AI Clinical Summary")

            if not summary:

                st.info(
                    "AI summary unavailable."
                )

                return

            st.success(summary)

    # @staticmethod
    # def render(plan):

    #     with st.container(border=True):

    #         st.subheader("🧠 AI Insights")

    #         insights = DashboardAnalyzer.generate(plan)

    #         if not insights:

    #             st.info("No insights available.")
    #             return

    #         for insight in insights:

    #             content = (
    #                 f"{insight['icon']} **{insight['title']}**\n\n"
    #                 f"{insight['message']}"
    #             )

    #             if insight["type"] == "success":

    #                 st.success(content)

    #             elif insight["type"] == "warning":

    #                 st.warning(content)

    #             elif insight["type"] == "error":

    #                 st.error(content)

    #             else:

    #                 st.info(content)