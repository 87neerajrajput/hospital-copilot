"""
executor.py

Milestone 9.2

Execution Engine

Responsibilities
----------------
1. Execute every plan step.
2. Dispatch to the correct Skill.
3. Maintain execution context.
"""

from copilot.planner import ExecutionPlan

from copilot.skills.knowledge import KnowledgeSkill
from copilot.skills.patient import PatientSkill
from copilot.skills.therapy import TherapySkill
from copilot.skills.report import ReportSkill


class Executor:

    def __init__(self):

        self.skills = {

            "knowledge": KnowledgeSkill(),

            "patient": PatientSkill(),

            "therapy": TherapySkill(),

            "report": ReportSkill(),

        }

    # ======================================================
    # EXECUTE PLAN
    # ======================================================

    async def execute(
        self,
        plan: ExecutionPlan,
    ):

        context = {}

        print("\n========== EXECUTOR ==========\n")

        for index, step in enumerate(plan.steps, start=1):

            print(f"Executing Step {index}")

            print(f"Skill : {step.skill}")

            print(f"Task  : {step.task}")

            print(f"Args  : {step.arguments}")

            print("-----------------------------")

            skill = self.skills.get(step.skill)

            if skill is None:

                raise ValueError(
                    f"Unknown Skill: {step.skill}"
                )

            result = await skill.execute(

                task=step.task,

                arguments=step.arguments,

                context=context,

            )

            print("Result")

            print(result)

            print()

            # ==========================================
            # Update Execution Context
            # ==========================================

            self._update_context(
                context,
                result,
            )

        print("\n========== FINAL CONTEXT ==========\n")

        print(context)

        print("\n===================================\n")

        return context

    # ======================================================
    # UPDATE CONTEXT
    # ======================================================

    def _update_context(
        self,
        context: dict,
        result: dict,
    ):

        if not result:

            return

        # -----------------------------
        # Patient Search
        # -----------------------------

        if "patients" in result:

            patients = result["patients"]

            if patients:

                context["patients"] = patients

                context["patient"] = patients[0]

        # -----------------------------
        # Patient Load
        # -----------------------------

        if "patient" in result:

            if result["patient"]:

                context["patient"] = result["patient"]

        # -----------------------------
        # Therapy Plan
        # -----------------------------

        if "therapy_plan" in result:

            if result["therapy_plan"]:

                context["therapy_plan"] = result["therapy_plan"]

        # -----------------------------
        # Generated Report
        # -----------------------------

        if "report" in result:

            if result["report"]:

                context["report"] = result["report"]

        # -----------------------------
        # Save IDs
        # -----------------------------

        if "plan_id" in result:

            context["plan_id"] = result["plan_id"]

        if "report_id" in result:

            context["report_id"] = result["report_id"]

        if "patient_id" in result:

            context["patient_id"] = result["patient_id"]