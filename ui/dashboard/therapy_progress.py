import streamlit as st


class TherapyProgress:

    @staticmethod
    def render(plan):

        with st.container():

            st.subheader("🎯 Active Therapy Goals")

            if not plan:
                st.info("No therapy plan available.")
                return

            goals = (
                plan
                .get("therapy_plan", {})
                .get("therapy_goals", [])
            )

            if not goals:
                st.info("No therapy goals available.")
                return

            for goal in goals:

                col1, col2 = st.columns(
                    [0.08, 0.92],
                    vertical_alignment="top",
                )

                with col1:
                    st.markdown(
                        "<span style='font-size:18px;color:#22c55e;'>✓</span>",
                        unsafe_allow_html=True,
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div style="
                            font-size:15px;
                            line-height:1.4;
                            margin-bottom:8px;
                        ">
                            {goal}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )