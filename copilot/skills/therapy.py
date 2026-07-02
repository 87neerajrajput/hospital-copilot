"""
therapy.py

Milestone 9.2

Therapy Skill

Responsibilities
----------------
Execute therapy-related business tasks.

Supported Tasks
---------------
- generate_therapy_plan
- load_latest_plan
- save_plan
"""

from hospital_mcp.hospital_client import HospitalMCPClient


class TherapySkill:

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

        if task == "generate_therapy_plan":

            return await self.generate_therapy_plan(
                arguments,
                context,
            )

        elif task == "load_latest_plan":

            return await self.load_latest_plan(
                arguments,
                context,
            )

        elif task == "save_plan":

            return await self.save_plan(
                arguments,
                context,
            )

        raise ValueError(
            f"Unknown Therapy task: {task}"
        )

    # ======================================================
    # GENERATE THERAPY PLAN
    # ======================================================

    async def generate_therapy_plan(
        self,
        arguments: dict,
        context: dict,
    ):
        """
        Placeholder.

        The actual therapy planner agent will be integrated
        in Milestone 9.3.
        """

        patient = context.get("patient")

        if patient is None:

            raise ValueError(
                "Patient not available in execution context."
            )

        return {

            "therapy_plan": None

        }

    # ======================================================
    # LOAD LATEST PLAN
    # ======================================================

    async def load_latest_plan(
        self,
        arguments: dict,
        context: dict,
    ):

        patient = context.get("patient")

        if patient is None:

            raise ValueError(
                "Patient not available in execution context."
            )

        plans = await self.mcp.get_patient_plans(
            patient["id"]
        )

        if not plans:

            return {

                "therapy_plan": None

            }

        latest_plan_id = plans[0]["id"]

        therapy_plan = await self.mcp.get_therapy_plan(
            latest_plan_id
        )

        return {

            "therapy_plan": therapy_plan

        }

    # ======================================================
    # SAVE PLAN
    # ======================================================

    async def save_plan(
        self,
        arguments: dict,
        context: dict,
    ):

        patient = context.get("patient")

        therapy_plan = context.get("therapy_plan")

        if patient is None:

            raise ValueError(
                "Patient not available in execution context."
            )

        if therapy_plan is None:

            raise ValueError(
                "Therapy plan not available in execution context."
            )

        plan_id = await self.mcp.save_therapy_plan(

            patient_id=patient["id"],

            patient_info=patient,

            therapy_plan=therapy_plan,

        )

        return {

            "plan_id": plan_id

        }