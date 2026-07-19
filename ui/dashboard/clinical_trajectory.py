import streamlit as st

from ui.dashboard.clinical_trajectory_analyzer import (
    ClinicalTrajectoryAnalyzer,
)


class ClinicalTrajectory:

    @staticmethod
    def render(
        plans,
        latest_plan,
        previous_plan,
    ):

        with st.container(border=True):

            st.subheader("🧠 Clinical Trajectory")

            if not latest_plan:

                st.info(
                    "No therapy plans available."
                )

                return

            result = ClinicalTrajectoryAnalyzer.generate(

                plans,

                latest_plan,

                previous_plan,

            )

            text = (
                f"**{result['status']}**\n\n"
                f"Confidence: {result['confidence']}"
            )

            if result["status"] == "Improving":

                st.success(text)

            elif result["status"] == "Stable":

                st.info(text)

            elif result["status"] == "Plateauing":

                st.warning(text)

            else:

                st.error(text)

            st.markdown("### Evidence")

            for reason in result["reasons"]:

                st.markdown(f"- {reason}")