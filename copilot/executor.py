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
from copilot.skills.comparison import ComparisonSkill
from copilot.skills.knowledge import KnowledgeSkill
from copilot.skills.qa import QASkill
from copilot.skills.approval import ApprovalSkill
from copilot.skills.report import ReportSkill

from copilot.execution_state import ExecutionState

from copilot.approval import (
    ApprovalService,
    ApprovalStatus,
)
from graph import state


class Executor:

    def __init__(self):

        self.registry = RegistryIndex()

        self.approval = ApprovalService()

        self.skills = {

            "patient": PatientSkill(),

            "therapy": TherapySkill(),

            "knowledge": KnowledgeSkill(),

            "qa": QASkill(),

            "report": ReportSkill(),

            "approval": ApprovalSkill(),

            "comparison": ComparisonSkill(),

        }

    # ======================================================
    # EXECUTE PLAN
    # ======================================================

    async def execute(
        self,
        plan: ExecutionPlan,
    ):

        state = ExecutionState(
            plan=plan,
        )

        state.context["intent"] = plan.intent

        print("\n========== EXECUTOR ==========\n")

        await self._run_steps(

            state,

        )

        if state.status == ApprovalStatus.WAITING:
            return state

        return state


    # ======================================================
    # EXECUTE HUMAN APPROVAL PLAN
    # ======================================================

    async def _run_steps(
        self,
        state: ExecutionState,
    ):

        for index in range(
            state.current_step,
            len(state.plan.steps),
        ):

            step = state.plan.steps[index]

            print(f"Executing Step {index + 1}")

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

                context=state.context,

            )

            # ---------------------------------------------
            # Workflow control step
            # ---------------------------------------------

            if step.skill == "approval":

                print("\n========== WAITING FOR HUMAN APPROVAL ==========\n")

                ApprovalService.wait_for_approval(state)

                state.pending_step = index

                return

            print(f"Resolved Args : {resolved_arguments}")

            # ---------------------------------------------
            # Human Approval
            # ---------------------------------------------

            if (
                step.skill == "approval"
                and step.task == "review_plan"
            ):

                print("\n========== WAITING FOR HUMAN APPROVAL ==========\n")

                ApprovalService.wait_for_approval(state)

                state.pending_step = index

                state.current_step = index

                return

            # ---------------------------------------------
            # Execute Skill
            # ---------------------------------------------

            if step.skill == "approval":

                result = await skill.execute(

                    task=step.task,

                    arguments=resolved_arguments,

                    context=state.context,

                    state=state,

                )

            else:

                result = await skill.execute(

                    task=step.task,

                    arguments=resolved_arguments,

                    context=state.context,

                )

            print("Result")

            print(result)

            print()

            # ---------------------------------------------
            # Approval pauses execution
            # ---------------------------------------------

            if state.waiting_for_approval:

                state.pending_step = index

                return state


            self._update_context(

                step=step,

                context=state.context,

                result=result,

            )

            state.current_step = index + 1

        state.status = "COMPLETED"


        if state.current_step == len(state.plan.steps):

            state.status = "COMPLETED"

            print("\n========== FINAL CONTEXT ==========\n")

            print(state.context)

            print("\n===================================\n")



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


    # ======================================================
    # RESUME EXECUTION
    # ======================================================

    async def resume(
        self,
        state: ExecutionState,
        decision: str,
    ) -> ExecutionState:
        """
        Resume execution after a human approval.
        """

        print("\n========== RESUME ==========")
        print("Decision received:", decision)
        print("============================")


        if not state.waiting_for_approval:
            return state

        # ----------------------------------------
        # Get the pending approval step
        # ----------------------------------------

        pending = state.pending_step

        step = state.plan.steps[pending]


        # This should always be the approval skill
        skill = self.skills[step.skill]

        # ----------------------------------------
        # Execute approval node
        # ----------------------------------------

        result = await skill.execute(

            task=step.task,

            arguments={
                "decision": decision,
            },

            context=state.context,

            state=state,

        )


        self._update_context(

                    step=step,

                    context=state.context,

                    result=result,

                )

        state.waiting_for_approval = False
        state.pending_step = None

        if result["approval_status"] == "rejected":

            state.waiting_for_approval = False
            state.pending_step = None
            state.status = "REJECTED"
            return state
        

        # ----------------------------------------
        # Clear waiting state
        # ----------------------------------------

        # Continue with the step AFTER approval
        state.current_step = pending + 1

        # ----------------------------------------
        # Continue remaining workflow
        # ----------------------------------------

        await self._run_steps(state)

        return state