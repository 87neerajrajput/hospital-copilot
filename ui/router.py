from enum import Enum

import streamlit as st


class AppPage(str, Enum):

    WORKSPACE = "👨‍⚕️ Workspace"

    DASHBOARD = "📊 Dashboard"

    ADMIN = "⚙ Administration"


class AppRouter:

    @staticmethod
    def render() -> AppPage:

        return st.segmented_control(
            "Navigation",
            options=[
                AppPage.WORKSPACE.value,
                AppPage.DASHBOARD.value,
                AppPage.ADMIN.value,
            ],
            default=AppPage.WORKSPACE.value,
            label_visibility="collapsed",
        )