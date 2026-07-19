# import streamlit as st


# class GoalEvolution:

#     @staticmethod
#     def render(goal_evolution):

#         with st.container():

#             st.subheader("🧬 Goal Evolution")

#             if not goal_evolution:

#                 st.info("Goal comparison not available.")
#                 return

#             sections = [

#                 (
#                     "➕ Added Goals",
#                     goal_evolution["added"],
#                     "success",
#                 ),

#                 (
#                     "➖ Removed Goals",
#                     goal_evolution["removed"],
#                     "warning",
#                 ),

#                 (
#                     "➡ Continuing Goals",
#                     goal_evolution["continued"],
#                     "info",
#                 ),

#             ]

#             for title, goals, style in sections:

#                 st.markdown(f"##### {title}")

#                 if not goals:

#                     st.caption("None")

#                 else:

#                     for goal in goals:

#                         if style == "success":

#                             st.success(goal)

#                         elif style == "warning":

#                             st.warning(goal)

#                         else:

#                             st.info(goal)

#                 st.markdown("")

import streamlit as st
import plotly.graph_objects as go


class GoalEvolution:

    @staticmethod
    def render(goal_evolution):

        st.subheader("🧬 Goal Evolution")

        added = goal_evolution["added"]
        removed = goal_evolution["removed"]
        continued = goal_evolution["continued"]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "Added",
                        "Removed",
                        "Continuing",
                    ],
                    values=[
                        len(added),
                        len(removed),
                        len(continued),
                    ],
                    textinfo="label+percent",
                    textposition="inside",
                    marker=dict(
                        colors=[
                            "#22c55e",
                            "#ef4444",
                            "#3b82f6",
                        ]
                    ),
                )
            ]
        )

        fig.update_layout(
            height=320,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10,
            ),
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(
            fig,
            width='stretch',
            config={
                "displayModeBar": False,
            },
        )

        st.divider()

        st.markdown("#### 🟢 Added Goals")

        if added:

            for goal in added:

                st.success(goal)

        else:

            st.caption("No new goals added.")

        st.divider()

        st.markdown("#### 🔴 Removed Goals")

        if removed:

            for goal in removed:

                st.warning(goal)

        else:

            st.caption("No goals removed.")