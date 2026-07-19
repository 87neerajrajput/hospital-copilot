import streamlit as st

from ui.dashboard.goal_evolution_analyzer import (
    GoalEvolutionAnalyzer,
)


class GoalEvolution:

    @staticmethod
    def render(previous_plan, latest_plan):

        with st.container(border=True):

            st.subheader("🧬 Goal Evolution")

            if not latest_plan:

                st.info("No therapy plans available.")
                return

            if not previous_plan:

                st.info(
                    "Only one therapy plan exists.\n\n"
                    "Goal comparison will appear after the next plan is created."
                )
                return

            evolution = GoalEvolutionAnalyzer.generate(
                previous_plan,
                latest_plan,
            )

            sections = [

                ("➕ Added Goals", evolution["added"], "success"),

                ("➖ Removed Goals", evolution["removed"], "warning"),

                ("➡ Continuing Goals", evolution["continued"], "info"),

            ]

            for title, goals, style in sections:

                st.markdown(f"#### {title}")

                if not goals:

                    st.caption("None")

                else:

                    for goal in goals:

                        if style == "success":
                            st.success(goal)

                        elif style == "warning":
                            st.warning(goal)

                        else:
                            st.info(goal)

                st.markdown("")