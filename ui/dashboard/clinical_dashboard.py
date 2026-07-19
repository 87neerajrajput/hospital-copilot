import asyncio
import streamlit as st

from ui.dashboard.ai_summary.ai_summary_builder import AISummaryBuilder
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
from services.llm_service import llm
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

        # ==========================================
        # Generate AI Summary
        # ==========================================

        prompt = AISummaryBuilder.build(
            patient,
            evidence,
        )

        response = llm.invoke(
            [
                (
                    "system",
                    prompt["system"],
                ),

                (
                    "human",
                    prompt["user"],
                ),
            ]
        )

        evidence.ai_summary = response.content

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
            with st.container(height=500, border=True):
                PatientSummary.render(patient)

        # ------------------------------------------
        # RIGHT COLUMN
        # ------------------------------------------

        with right:
            with st.container(height=500):
                # -----------------------------
                # AI Summary
                # -----------------------------

                AIInsights.render(
                    evidence.ai_summary
                )

                # st.markdown(
                #     "<div style='height:19px'></div>",
                #     unsafe_allow_html=True,
                # )

                # -----------------------------
                # Active Therapy Goals
                # -----------------------------

                TherapyProgress.render(
                    latest_plan
                )

        # ==========================================
        # Row 2
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        left, right = st.columns(
            [1, 1],
            gap="large",
        )

        with left:
            with st.container(height=600, border=True):
                ClinicalSummary.render(
                    patient,
                    full_plans,
                    latest_plan,
                )

        with right:
            with st.container(height=600, border=True):
                GoalEvolution.render(
                    evidence.goal_evolution
                )

        # ==========================================
        # Row 3
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        ClinicalTrajectory.render(
            evidence.trajectory
        )

        
        # ==========================================
        # Row 4
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        ClinicalAlerts.render(
            evidence.alerts
        ) 

        # ==========================================
        # Row 5
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        left, right = st.columns(
            [1, 1],
            gap="large",
        )

        with left:
            with st.container(height=700, border=True):
                FocusAreaEvolution.render(
                    evidence.focus_evolution
                )

        with right:
            with st.container(height=700, border=True):
                GoalPersistence.render(
                    evidence.goal_persistence
                )


        # ==========================================
        # Row 6
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        left, center, right = st.columns(
            [1, 1, 1],
            gap="large",
        )

        with left:
            with st.container(height=550, border=True):
                TherapyJourney.render(
                    evidence.therapy_journey
                )

        with center:
            with st.container(height=550, border=True):
                TherapyTimeline.render(full_plans)

        with right:
            with st.container(height=550, border=True):
                RecentActivity.render(activities)

        # ==========================================
        # Row 7
        # ==========================================

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True
        )

        with st.expander("AI Prompt", expanded=False):

            prompt = AISummaryBuilder.build(
                patient,
                evidence,
            )

            st.code(prompt["user"], language="json",)