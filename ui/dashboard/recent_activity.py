import streamlit as st


class RecentActivity:

    @staticmethod
    def render(activities):

        with st.container():

            st.subheader("📝 Recent Activity")

            if not activities:

                st.info("No recent activity available.")
                return

            activities = sorted(
                activities,
                key=lambda x: x["timestamp"],
                reverse=True,
            )

            for i, activity in enumerate(activities):

                icon_col, content_col = st.columns(
                    [0.6, 9],
                    vertical_alignment="top",
                )

                with icon_col:

                    st.markdown(
                        f"""
                        <div style="
                            font-size:20px;
                            margin-top:2px;
                        ">
                            {activity["icon"]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with content_col:

                    st.markdown(
                        f"""
                        <div style="
                            font-size:16px;
                            font-weight:600;
                            margin-bottom:2px;
                        ">
                            {activity["title"]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"""
                        <div style="
                            color:#9ca3af;
                            font-size:13px;
                            margin-bottom:4px;
                        ">
                            🕒 {activity["timestamp"].strftime("%d %b %Y • %I:%M %p")}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                if i < len(activities) - 1:

                    st.markdown(
                        """
                        <hr style="
                            margin-top:8px;
                            margin-bottom:8px;
                            border:none;
                            border-top:1px solid rgba(255,255,255,0.12);
                        ">
                        """,
                        unsafe_allow_html=True,
                    )