from agents.qa import qa_agent
from graph.state import HealthcareState


class QASkill:

    async def execute(
        self,
        task: str,
        arguments: dict,
        context: dict,
    ):

        if task == "validate_therapy_plan":

            return await self.validate_therapy_plan(
                arguments,
                context,
            )

        raise ValueError(f"Unknown QA task: {task}")

    # ======================================================
    # VALIDATE THERAPY PLAN
    # ======================================================

    async def validate_therapy_plan(
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

        assessment_summary = context.get(
            "assessment_summary"
        )

        retrieved_docs = context.get(
            "retrieved_docs",
            []
        )

        state = HealthcareState(

            patient_form=None,

            user_query="",

            assessment_summary=assessment_summary,

            patient_info=patient,

            patient_id=patient["id"],

            therapy_plan=therapy_plan,

            plan_id=context.get("plan_id"),

            retrieved_docs=retrieved_docs,

            qa_result=None,

            approval_status=None,

            clinical_report=None,

            parent_report=None,

            clinical_report_id=None,

            parent_report_id=None,

            next_agent="",

        )

        result = await qa_agent(state)

        return result