import asyncio
import streamlit as st

from ui.dashboard.goal_evolution import GoalEvolution
from ui.dashboard.patient_summary import PatientSummary
from ui.dashboard.therapy_progress import TherapyProgress
from ui.dashboard.therapy_timeline import TherapyTimeline
from ui.dashboard.ai_insights import AIInsights
from ui.dashboard.recent_activity import RecentActivity
from ui.dashboard.clinical_summary import ClinicalSummary
from ui.dashboard.clinical_alerts import ClinicalAlerts
from ui.dashboard.therapy_journey import TherapyJourney
from ui.dashboard.focus_area_evolution import FocusAreaEvolution
from ui.dashboard.goal_persistence import GoalPersistence
from ui.dashboard.clinical_trajectory import ClinicalTrajectory
from ui.dashboard.evidence.clinical_evidence_builder import (
    ClinicalEvidenceBuilder,
)
from hospital_mcp.hospital_client import mcp

# ==========================================================
# MCP CLIENT
# ==========================================================

class ClinicalDashboard:

    @staticmethod
    def render(patient_id: int):

        # ------------------------------------------
        # Load dashboard from MCP
        # ------------------------------------------

        dashboard = asyncio.run(
            mcp.get_patient_dashboard(
                patient_id
            )
        )

        if not dashboard:

            st.error("Dashboard not found.")

            return

        patient = dashboard["patient"]

        full_plans = dashboard["plans"]

        # ------------------------------------------
        # Reuse loaded plans
        # ------------------------------------------

        latest_plan = full_plans[0] if full_plans else None

        previous_plan = (
            full_plans[1]
            if len(full_plans) > 1
            else None
        )

        # ==========================================
        # Build Clinical Evidence
        # ==========================================

        evidence = ClinicalEvidenceBuilder.build(
            full_plans,
            latest_plan,
            previous_plan,
        )

        activities = []

        for plan in full_plans:

            activities.append({

                "type": "therapy_plan",

                "title": "Therapy Plan Generated",

                "timestamp": plan["created_at"],

                "icon": "📄",

            })

        # ==========================================
        # Row 1
        # ==========================================

        left, right = st.columns(
            [1, 1],
            gap="large",
        )

        with left:
            PatientSummary.render(patient)

        with right:
            TherapyProgress.render(latest_plan)

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True
        )

        # ==========================================
        # Row 2
        # ==========================================

        left, right = st.columns(
            [1, 1],
            gap="large",
        )

        with left:
            TherapyTimeline.render(full_plans)

        with right:
            AIInsights.render(latest_plan)

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True
        )

        # ==========================================
        # Row 3
        # ==========================================

        left, center, right = st.columns(
            [1, 1, 1],
            gap="large",
        )

        with left:
            RecentActivity.render(activities)

        with center:
            ClinicalSummary.render(
                patient,
                full_plans,
                latest_plan,
            )

        with right:
            GoalEvolution.render(
                previous_plan,
                latest_plan,
            )

        
        # ==========================================
        # Row 4
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        ClinicalAlerts.render(
            full_plans,
            latest_plan,
            previous_plan,
        )

        # ==========================================
        # Row 5
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        TherapyJourney.render(
            full_plans
        )

        # ==========================================
        # Row 6
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        FocusAreaEvolution.render(
            full_plans
        )

        # ==========================================
        # Row 7
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        GoalPersistence.render(
            full_plans
        )

        # ==========================================
        # Row 8
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        ClinicalTrajectory.render(

            full_plans,

            latest_plan,

            previous_plan,

        )