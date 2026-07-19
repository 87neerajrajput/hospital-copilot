import streamlit as st


class GoalPersistence:

    @staticmethod
    def render(goal_persistence):

        with st.container():

            st.subheader("🎯 Goal Persistence")

            if not goal_persistence:

                st.info("No therapy goals available.")
                return

            max_count = max(
                item["count"]
                for item in goal_persistence
            )

            for item in goal_persistence:

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