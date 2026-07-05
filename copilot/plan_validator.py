"""
plan_validator.py

Validates an ExecutionPlan before execution.

Responsibilities
----------------
1. Verify every task exists.
2. Verify every required artifact has already been produced.
3. Prevent invalid execution plans from reaching the Executor.

The validator is metadata-driven.

It never contains hardcoded business rules.
"""

from copilot.execution_plan import ExecutionPlan
from copilot.registry_index import RegistryIndex


class PlanValidationError(Exception):
    """Raised when an execution plan is invalid."""
    pass


class PlanValidator:

    def __init__(self):

        self.registry = RegistryIndex()

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        plan: ExecutionPlan,
    ) -> ExecutionPlan:

        available_artifacts = set()

        for step in plan.steps:

            task = self.registry.get_task(

                skill=step.skill,

                task=step.task,

            )

            if task is None:

                raise PlanValidationError(

                    f"Unknown task: {step.skill}.{step.task}"

                )

            definition = task["definition"]

            # -----------------------------------------
            # Verify required artifacts
            # -----------------------------------------

            for required in definition["requires"]:

                if required not in available_artifacts:

                    raise PlanValidationError(

                        f"{step.skill}.{step.task} requires "
                        f"'{required}' before execution."

                    )

            # -----------------------------------------
            # Mark produced artifacts available
            # -----------------------------------------

            available_artifacts.update(

                definition["produces"]

            )

        return plan