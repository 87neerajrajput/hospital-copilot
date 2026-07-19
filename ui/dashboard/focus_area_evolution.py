import streamlit as st


class FocusAreaEvolution:

    @staticmethod
    def render(focus_evolution):

        with st.container():

            st.subheader("📊 Focus Area Evolution")

            if not focus_evolution:

                st.info("No focus areas available.")
                return

            max_count = max(
                item["count"]
                for item in focus_evolution
            )

            for item in focus_evolution:

                left, right = st.columns(
                    [4, 2]
                )

                with left:

                    st.markdown(
                        f"**{item['focus_area']}**"
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