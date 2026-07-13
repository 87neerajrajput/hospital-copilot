from copilot.formatters.copilot_formatter import CopilotFormatter
from copilot.formatters.therapy_plan_formatter import TherapyPlanFormatter
from copilot.formatters.comparison_formatter import ComparisonFormatter
from copilot.formatters.evolution_formatter import EvolutionFormatter


class WorkflowFormatter:
    """
    Converts workflow execution results into
    human-readable chat responses.
    """

    @staticmethod
    def format(
        intent: str,
        context: dict,
    ) -> str:

        # -----------------------------------------
        # Patient Search
        # -----------------------------------------

        if intent == "patient_search":

            patient = context.get("patient")

            if patient:

                return CopilotFormatter.patient(patient)

            return CopilotFormatter.no_patient()

        # -----------------------------------------
        # Therapy History
        # -----------------------------------------

        elif intent == "therapy_history":

            plans = context.get(
                "therapy_plan_list",
                [],
            )

            return CopilotFormatter.therapy_history(
                plans
            )

        # -----------------------------------------
        # Therapy Lookup
        # -----------------------------------------

        elif intent == "therapy_lookup":

            therapy_plan = context.get(
                "therapy_plan"
            )

            if therapy_plan is None:

                return "Therapy plan not found."

            return TherapyPlanFormatter.format(
                therapy_plan,
                review_mode=False,
            )

        # -----------------------------------------
        # Therapy Comparison
        # -----------------------------------------

        elif intent == "therapy_comparison":

            comparison = context.get(
                "therapy_comparison"
            )

            if comparison is None:

                return "Comparison not available."

            return ComparisonFormatter.format(comparison)
        

        # -----------------------------------------
        # Therapy Evolution
        # -----------------------------------------

        elif intent == "therapy_evolution":

            evolution = context.get(
                "therapy_evolution"
            )

            if evolution is None:

                return "Therapy evolution not available."

            return EvolutionFormatter.format(
                evolution
            )

        # -----------------------------------------
        # Therapy Generation
        # -----------------------------------------

        elif intent == "therapy_generation":

            return CopilotFormatter.therapy_saved()

        # -----------------------------------------
        # Report Generation
        # -----------------------------------------

        elif intent == "report_generation":

            return "Reports generated successfully."

        # -----------------------------------------
        # Therapy Review
        # -----------------------------------------

        elif intent == "therapy_review":

            return "Therapy review completed."

        # -----------------------------------------
        # Default
        # -----------------------------------------

        return "Workflow completed successfully."