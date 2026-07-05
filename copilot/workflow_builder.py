"""
workflow_builder.py

Builds an executable ExecutionPlan from a WorkflowRequest.

Responsibilities
----------------
1. Read intent metadata.
2. Determine the requested artifact and operation.
3. Resolve task dependencies.
4. Inject runtime arguments.
5. Return an ExecutionPlan.

The WorkflowBuilder never performs dependency resolution itself.
It delegates that responsibility to DependencyResolver.
"""

from copilot.intent_registry import INTENTS
from copilot.dependency_resolver import DependencyResolver
from copilot.execution_plan import (
    PlanStep,
    ExecutionPlan,
)


class WorkflowBuilder:

    def __init__(self):

        self.resolver = DependencyResolver()

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        intent: str,
        goal: str,
        entities: dict,
    ) -> ExecutionPlan:

        if intent not in INTENTS:

            raise ValueError(

                f"Unknown intent: {intent}"

            )

        intent_info = INTENTS[intent]

        artifact = intent_info["artifact"]

        operation = intent_info["operation"]

        resolved_tasks = self.resolver.resolve(

            artifact=artifact,

            operation=operation,

        )

        steps = []

        for task in resolved_tasks:

            arguments = self._build_arguments(

                task_name=task["task"],

                entities=entities,

            )

            steps.append(

                PlanStep(

                    skill=task["skill"],

                    task=task["task"],

                    arguments=arguments,

                )

            )

        return ExecutionPlan(

            goal=goal,

            intent=intent,

            steps=steps,

        )

    # =====================================================
    # BUILD ARGUMENTS
    # =====================================================

    def _build_arguments(
        self,
        task_name: str,
        entities: dict,
    ) -> dict:

        arguments = {}

        # -----------------------------------------
        # Patient
        # -----------------------------------------

        if task_name == "find_patient":

            if "patient_name" in entities:

                arguments["name"] = entities["patient_name"]

        # -----------------------------------------
        # Reports
        # -----------------------------------------

        if task_name == "generate_report":

            if "report_type" in entities:

                arguments["report_type"] = entities["report_type"]

        # -----------------------------------------
        # Therapy
        # -----------------------------------------

        if task_name == "generate_therapy_plan":

            if "diagnosis" in entities:

                arguments["diagnosis"] = entities["diagnosis"]

            if "therapy_type" in entities:

                arguments["therapy_type"] = entities["therapy_type"]

        return arguments