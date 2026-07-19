import streamlit as st

from ui.dashboard.goal_persistence_analyzer import (
    GoalPersistenceAnalyzer,
)


class GoalPersistence:

    @staticmethod
    def render(plans):

        with st.container(border=True):

            st.subheader("🎯 Goal Persistence")

            if not plans:

                st.info("No therapy plans available.")

                return

            data = GoalPersistenceAnalyzer.generate(
                plans
            )

            if not data:

                st.info("No therapy goals found.")

                return

            max_count = max(
                item["count"]
                for item in data
            )

            for item in data:

                left, right = st.columns(
                    [4, 2]
                )

                with left:

                    st.markdown(
                        f"**{item['goal']}**"
                    )

                    st.progress(
                        item["count"] / max_count
                    )

                with right:

                    st.metric(

                        "Plans",

                        item["count"],

                        f"{item['percent']}%",

                    )

                    st.caption(

                        "Last: "

                        + item["last_seen"].strftime(
                            "%d %b %Y"
                        )

                    )