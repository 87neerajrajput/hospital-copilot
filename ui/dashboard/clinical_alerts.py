import streamlit as st


class ClinicalAlerts:

    @staticmethod
    def render(alerts):

        with st.container(border=True):

            st.subheader("🚨 Clinical Alerts")

            if not alerts:

                st.success("No clinical alerts. Patient is progressing without any system-detected concerns.")

                return

            for alert in alerts:

                if alert["type"] == "error":

                    st.error(
                        f"**{alert['title']}**\n\n"
                        f"{alert['message']}"
                    )

                elif alert["type"] == "warning":

                    st.warning(
                        f"**{alert['title']}**\n\n"
                        f"{alert['message']}"
                    )

                elif alert["type"] == "success":

                    st.success(
                        f"**{alert['title']}**\n\n"
                        f"{alert['message']}"
                    )

                else:

                    st.info(
                        f"**{alert['title']}**\n\n"
                        f"{alert['message']}"
                    )