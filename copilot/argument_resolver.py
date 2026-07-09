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

        # =====================================================
        # Load patient plans
        # =====================================================

        if task == "load_patient_plans":

            patient = context.get("patient")

            if patient:

                patient_id = patient.get("id")

                if patient_id:

                    arguments.setdefault(
                        "patient_id",
                        patient_id,
                    )

        # =====================================================
        # Load latest therapy plan
        # =====================================================

        elif task == "load_latest_plan":

            patient = context.get("patient")

            if patient:

                arguments.setdefault(
                    "patient_id",
                    patient["id"],
                )

            plans = context.get("therapy_plan_list", [])

            if plans:

                selector = arguments.get(
                    "plan_selector",
                    "latest",
                )

                if selector == "latest":

                    selected_plan = plans[0]

                elif selector == "previous":

                    selected_plan = (
                        plans[1]
                        if len(plans) > 1
                        else plans[0]
                    )

                else:
                    # fallback
                    selected_plan = plans[0]

                arguments["plan_id"] = selected_plan["id"]

        # =====================================================
        # Generate therapy plan
        # =====================================================

        elif task == "generate_therapy_plan":

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

            report_type = step.arguments.get("report_type")

            if report_type:

                arguments.setdefault(
                    "report_type",
                    report_type,
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


    

        # =====================================================
        # Save Therapy Plan
        # =====================================================

        elif task == "save_plan":

            patient = context.get("patient")
            therapy_plan = context.get("therapy_plan")

            if patient:

                arguments.setdefault(
                    "patient_id",
                    patient["id"],
                )

                arguments.setdefault(
                    "patient_info",
                    patient,
                )

            if therapy_plan:

                arguments.setdefault(
                    "therapy_plan",
                    therapy_plan,
                )

        from pprint import pprint

        print("\n========== RESOLVED ARGUMENTS ==========")
        print(f"Task : {task}")
        pprint(arguments)
        print("========================================")

        return arguments