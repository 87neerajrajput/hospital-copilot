"""
report.py

Milestone 9.2

Report Skill

Responsibilities
----------------
Execute report-related business tasks.

Supported Tasks
---------------
- generate_report
- save_report
"""

from agents.report import report_agent

from graph.state import HealthcareState

from hospital_mcp.hospital_client import mcp


class ReportSkill:

    def __init__(self):

        self.mcp = mcp

    # ======================================================
    # EXECUTE
    # ======================================================

    async def execute(
        self,
        task: str,
        arguments: dict,
        context: dict,
    ):

        if task == "generate_report":

            return await self.generate_report(
                arguments,
                context,
            )

        elif task == "save_report":

            return await self.save_report(
                arguments,
                context,
            )

        raise ValueError(
            f"Unknown Report task: {task}"
        )

    # ======================================================
    # GENERATE REPORT
    # ======================================================

    async def generate_report(
        self,
        arguments: dict,
        context: dict,
    ):

        patient = context.get("patient")

        if patient is None:

            raise ValueError(
                "Patient not available in execution context."
            )

        therapy_plan = context.get("therapy_plan")

        if therapy_plan is None:

            raise ValueError(
                "Therapy plan not available in execution context."
            )

        qa_result = context.get(
            "qa_result"
        )

        requested = arguments.get("report_type", "both")

        if requested == "parent":
            report_types = ["parent"]

        elif requested == "clinical":
            report_types = ["clinical"]

        else:
            report_types = ["clinical", "parent"]

        state = HealthcareState(

            patient_form=None,

            user_query="",

            assessment_summary=None,

            patient_info=patient,

            patient_id=patient["id"],

            clinical_memory=None,

            therapy_plan=therapy_plan,

            plan_id=context.get("plan_id"),

            retrieved_docs=None,

            qa_result=qa_result,

            approval_status=None,

            report_types=report_types,

            clinical_report=None,

            parent_report=None,

            clinical_report_id=None,

            parent_report_id=None,

            next_agent="",

        )

        result = await report_agent(state)

        return result

    # ======================================================
    # SAVE REPORT
    # ======================================================

    async def save_report(
        self,
        arguments: dict,
        context: dict,
    ):

        patient = context.get("patient")

        report = context.get("report")

        if patient is None:

            raise ValueError(
                "Patient not available in execution context."
            )

        if report is None:

            raise ValueError(
                "Report not available in execution context."
            )

        report_type = arguments.get(
            "report_type",
            "Clinical Report"
        )

        result = await self.mcp.save_report(

            patient_id=patient["id"],

            report_type=report_type,

            report_content=report,

        )

        return result