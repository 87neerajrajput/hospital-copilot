import streamlit as st

from ui.dashboard.therapy_journey_analyzer import (
    TherapyJourneyAnalyzer,
)


class TherapyJourney:

    @staticmethod
    def render(plans):

        with st.container(border=True):

            st.subheader("📈 Therapy Journey")

            if not plans:

                st.info("No therapy plans available.")

                return

            journey = TherapyJourneyAnalyzer.generate(
                plans
            )

            for step in journey:

                with st.expander(

                    step["date"].strftime(
                        "%d %b %Y"
                    ),

                    expanded=False,

                ):

                    st.markdown("**Focus Areas**")

                    if step["focus"]:

                        for area in step["focus"]:

                            st.markdown(f"• {area}")

                    else:

                        st.caption("None")

                    st.metric(
                        "Goals",
                        step["goal_count"],
                    )

                    if step["added"]:

                        st.success("Added Goals")

                        for goal in step["added"]:

                            st.write("➕", goal)

                    if step["removed"]:

                        st.warning("Removed Goals")

                        for goal in step["removed"]:

                            st.write("➖", goal)