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

from hospital_mcp.hospital_client import HospitalMCPClient


class ReportSkill:

    def __init__(self):

        self.mcp = HospitalMCPClient()

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
        """
        Placeholder.

        The actual Report Generation Agent
        will be integrated in Milestone 9.3.
        """

        report = context.get("report")

        return {

            "report": report

        }

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