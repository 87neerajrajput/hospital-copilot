import streamlit as st


class ClinicalTrajectory:

    @staticmethod
    def render(trajectory):

        with st.container(border=True):

            st.subheader("🧠 Clinical Trajectory")

            if not trajectory:

                st.info("Trajectory unavailable.")

                return

            text = (

                f"**{trajectory['status']}**\n\n"

                f"Confidence: {trajectory['confidence']}"

            )

            if trajectory["status"] == "Improving":

                st.success(text)

            elif trajectory["status"] == "Stable":

                st.info(text)

            elif trajectory["status"] == "Plateauing":

                st.warning(text)

            else:

                st.error(text)

            st.markdown("### Evidence")

            for reason in trajectory["reasons"]:

                st.markdown(f"- {reason}")