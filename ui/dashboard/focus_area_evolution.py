import streamlit as st

from ui.dashboard.focus_area_evolution_analyzer import (
    FocusAreaEvolutionAnalyzer,
)


class FocusAreaEvolution:

    @staticmethod
    def render(plans):

        with st.container(border=True):

            st.subheader("📊 Focus Area Evolution")

            if not plans:

                st.info("No therapy plans available.")

                return

            data = FocusAreaEvolutionAnalyzer.generate(
                plans
            )

            if not data:

                st.info("No focus areas found.")

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
                        f"**{item['focus_area']}**"
                    )

                    progress = item["count"] / max_count

                    st.progress(progress)

                with right:

                    st.metric(

                        "Occurrences",

                        item["count"],

                        f"{item['percent']}%",

                    )

                    st.caption(

                        "Last: "

                        + item["last_seen"].strftime(
                            "%d %b %Y"
                        )

                    )