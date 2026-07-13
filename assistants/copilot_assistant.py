from assistants.chat_assistant import ask_ai
import streamlit as st
from copilot.formatters.therapy_plan_formatter import TherapyPlanFormatter
from copilot.supervisor import ClinicalSupervisor
from copilot.executor import Executor
from copilot.formatters.copilot_formatter import CopilotFormatter
from copilot.formatters.workflow_formatter import WorkflowFormatter


class CopilotAssistant:

    def __init__(self):

        self.supervisor = ClinicalSupervisor()

        self.executor = Executor()


    def _get_execution_state(self):

        return st.session_state.get("execution_state")


    def _set_execution_state(self, state):

        st.session_state.execution_state = state


    async def ask(
        self,
        question: str,
        patient=None,
        chat_history=None,
    ):
        """
        Main entry point for the AI Copilot.

        """

        execution_state = self._get_execution_state()

        if (
            execution_state and execution_state.waiting_for_approval
        ):
             
            decision = question.strip().lower()

            state = await self.executor.resume(

                state=execution_state,

                decision=decision,

            )

            if state.status == "REJECTED":

                self._set_execution_state(None)

                return CopilotFormatter.therapy_rejected()
            

            if state.waiting_for_approval:

                self._set_execution_state(state)

                return (
                    "Waiting for another approval."
                )

            self._set_execution_state(None)

            return WorkflowFormatter.format(
                state.plan.intent,
                state.context,
            )
    

        # ---------------------------------------
        # Ask the Supervisor to classify
        # ---------------------------------------

        plan = self.supervisor.plan(question)

        print("\n========== COPILOT ==========")
        print("Intent :", plan.intent)
        print("=============================\n")

        # ---------------------------------------
        # Workflow request?
        # ---------------------------------------

        WORKFLOW_INTENTS = {

            "patient_search",

            "therapy_lookup",

            "therapy_history",

            "therapy_generation",

            "therapy_review",

            "therapy_comparison",

            "therapy_evolution",

            "report_generation",

        }

        if plan.intent in WORKFLOW_INTENTS:

            execution_state = await self.executor.execute(plan)

            if execution_state.waiting_for_approval:

                self._set_execution_state(execution_state)

                therapy_plan = execution_state.context.get("therapy_plan")

                report = TherapyPlanFormatter.format(
                    therapy_plan,
                    review_mode=True,
                )

                return report


            return WorkflowFormatter.format(
                plan.intent,
                execution_state.context,
            )

        # ---------------------------------------
        # Otherwise use normal chat
        # ---------------------------------------

        return await ask_ai(
            question=question,
            patient=patient,
            chat_history=chat_history,
        )

