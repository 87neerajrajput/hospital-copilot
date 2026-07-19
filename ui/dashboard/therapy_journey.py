import streamlit as st


class TherapyJourney:

    @staticmethod
    def render(journey):

        with st.container():

            st.subheader("📈 Therapy Journey")

            if not journey:

                st.info("No therapy plans available.")
                return

            for step in journey:

                with st.expander(

                    step["date"].strftime("%d %b %Y"),

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

                            st.write(f"➕ {goal}")

                    if step["removed"]:

                        st.warning("Removed Goals")

                        for goal in step["removed"]:

                            st.write(f"➖ {goal}")