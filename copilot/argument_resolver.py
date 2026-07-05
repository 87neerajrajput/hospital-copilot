"""
argument_resolver.py

Resolves runtime arguments from the execution context.

Responsibilities
----------------
- Merge planner arguments.
- Inject runtime values from execution context.
- Keep Skills free from orchestration logic.

This resolver is intentionally task-aware.
Business dependency resolution belongs to DependencyResolver.
"""

from copy import deepcopy


class ArgumentResolver:

    @staticmethod
    def resolve(
        step,
        context,
    ):

        arguments = deepcopy(step.arguments)

        task = step.task

        # =====================================================
        # Patient-dependent tasks
        # =====================================================

        if task in (

            "load_latest_plan",

            "generate_therapy_plan",

        ):

            patient = context.get("patient")

            if patient:

                patient_id = patient.get("id")

                if patient_id:

                    arguments.setdefault(

                        "patient_id",

                        patient_id,

                    )

        # =====================================================
        # Report generation
        # =====================================================

        elif task == "generate_report":

            patient = context.get("patient")

            therapy_plan = context.get("therapy_plan")

            if patient:

                arguments.setdefault(

                    "patient",

                    patient,

                )

            if therapy_plan:

                arguments.setdefault(

                    "therapy_plan",

                    therapy_plan,

                )

        elif task == "search_information":

            patient = context.get("patient")

            if patient:

                diagnosis = patient.get("diagnosis", "")

                concerns = patient.get("concerns", [])

                query = diagnosis

                if concerns:
                    query += " " + " ".join(concerns)

                arguments.setdefault("query", query)

        return arguments