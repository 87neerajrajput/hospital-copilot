"""
executor.py

Execution Engine

Responsibilities
----------------
1. Execute every plan step.
2. Dispatch to the correct Skill.
3. Resolve runtime arguments.
4. Maintain execution context.
"""

from copilot.execution_plan import (
    PlanStep,
    ExecutionPlan,
)

from copilot.argument_resolver import ArgumentResolver

from copilot.registry_index import RegistryIndex

from copilot.skills.patient import PatientSkill
from copilot.skills.therapy import TherapySkill
from copilot.skills.knowledge import KnowledgeSkill
from copilot.skills.qa import QASkill
from copilot.skills.report import ReportSkill


class Executor:

    def __init__(self):

        self.registry = RegistryIndex()

        self.skills = {

            "patient": PatientSkill(),

            "therapy": TherapySkill(),

            "knowledge": KnowledgeSkill(),

            "qa": QASkill(),

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

            print(f"Original Args : {step.arguments}")

            print("--------------------------------")

            if step.skill not in self.skills:

                raise ValueError(

                    f"Unknown skill: {step.skill}"

                )

            skill = self.skills[step.skill]

            resolved_arguments = ArgumentResolver.resolve(

                step=step,

                context=context,

            )

            print(f"Resolved Args : {resolved_arguments}")

            result = await skill.execute(

                task=step.task,

                arguments=resolved_arguments,

                context=context,

            )

            print("Result")

            print(result)

            print()

            self._update_context(

                step=step,

                context=context,

                result=result,

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

        step,

        context: dict,

        result: dict,

    ):

        if not result:

            return

        # ----------------------------------------------
        # Lookup task metadata
        # ----------------------------------------------

        task_info = self.registry.get_task(

            skill=step.skill,

            task=step.task,

        )

        if task_info:

            produces = task_info["definition"]["produces"]

            for artifact in produces:

                if artifact in result:

                    context[artifact] = result[artifact]

        # ----------------------------------------------
        # Search results
        # ----------------------------------------------

        if "patients" in result:

            context["patients"] = result["patients"]

            if result["patients"]:

                context["patient"] = result["patients"][0]

        # ----------------------------------------------
        # Runtime identifiers
        # ----------------------------------------------

        for key in (

            "patient_id",

            "plan_id",

            "report_id",

        ):

            if key in result:

                context[key] = result[key]