import streamlit as st


class TherapyTimeline:

    @staticmethod
    def render(plans):

        with st.container():

            st.subheader("🗓 Therapy Timeline")

            if not plans:
                st.info("No therapy plans available.")
                return

            for i, plan in enumerate(plans):

                icon_col, content_col = st.columns(
                    [0.6, 9],
                    vertical_alignment="top",
                )

                # -----------------------------------
                # Timeline Icon
                # -----------------------------------

                with icon_col:

                    st.markdown(
                        """
                        <div style="
                            font-size:22px;
                            margin-top:2px;
                        ">
                            📄
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # -----------------------------------
                # Timeline Content
                # -----------------------------------

                with content_col:

                    st.markdown(
                        """
                        <div style="
                            font-size:17px;
                            font-weight:600;
                            margin-bottom:2px;
                        ">
                            Therapy Plan Generated
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"""
                        <div style="
                            color:#9ca3af;
                            font-size:13px;
                            margin-top:0px;
                            margin-bottom:4px;
                        ">
                            🕒 {plan["created_at"].strftime("%d %b %Y • %I:%M %p")}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # -----------------------------------
                # Divider
                # -----------------------------------

                if i < len(plans) - 1:

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