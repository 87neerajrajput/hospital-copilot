import streamlit as st

from ui.dashboard.clinical_summary_analyzer import (
    ClinicalSummaryAnalyzer,
)


class ClinicalSummary:

    @staticmethod
    def render(patient, plans, latest_plan):

        summary = ClinicalSummaryAnalyzer.generate(
            patient,
            plans,
            latest_plan,
        )

        with st.container(border=True):

            st.subheader("📊 Clinical Summary")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Therapy Duration",
                    summary["therapy_duration"],
                )

                st.metric(
                    "Therapy Plans",
                    summary["therapy_plans"],
                )

            with col2:

                st.metric(
                    "Latest Plan",
                    summary["latest_plan"],
                )

                st.metric(
                    "Focus Areas",
                    len(summary["focus_areas"]),
                )

            st.markdown("---")

            st.markdown("##### Current Focus Areas")

            if summary["focus_areas"]:

                for area in summary["focus_areas"]:

                    st.markdown(f"• {area}")

            else:

                st.caption("No focus areas available.")