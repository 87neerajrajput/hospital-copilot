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
from copilot.workflow_events import workflow_events
import uuid


class Executor:

    WORKFLOW_MESSAGES = {

        # --------------------------------------------------
        # Patient
        # --------------------------------------------------

        ("patient", "find_patient"): {

            "running": "Finding patient...",

            "completed": "Patient found",

        },

        # --------------------------------------------------
        # Knowledge
        # --------------------------------------------------

        ("knowledge", "search_information"): {

            "running": "Searching clinical knowledge...",

            "completed": "Clinical knowledge retrieved",

        },

        # --------------------------------------------------
        # Therapy
        # --------------------------------------------------

        ("therapy", "load_patient_plans"): {

            "running": "Loading previous therapy plans...",

            "completed": "Previous therapy plans loaded",

        },

        ("therapy", "build_clinical_memory"): {

            "running": "Building clinical memory...",

            "completed": "Clinical memory built",

        },

        ("therapy", "generate_therapy_plan"): {

            "running": "Generating therapy plan...",

            "completed": "Therapy plan generated",

        },

        ("therapy", "load_latest_plan"): {

            "running": "Loading latest therapy plan...",

            "completed": "Latest therapy plan loaded",

        },

        ("therapy", "load_selected_plans"): {

            "running": "Loading selected therapy plans...",

            "completed": "Selected therapy plans loaded",

        },

        ("therapy", "save_plan"): {

            "running": "Saving therapy plan...",

            "completed": "Therapy plan saved",

        },

        # --------------------------------------------------
        # Comparison
        # --------------------------------------------------

        ("comparison", "compare_plans"): {

            "running": "Comparing therapy plans...",

            "completed": "Therapy comparison completed",

        },

        ("comparison", "analyze_evolution"): {

            "running": "Analyzing therapy evolution...",

            "completed": "Therapy evolution analyzed",

        },

        ("comparison", "analyze_trend"): {

            "running": "Analyzing clinical trends...",

            "completed": "Clinical trend analysis completed",

        },

        # --------------------------------------------------
        # QA
        # --------------------------------------------------

        ("qa", "validate_therapy_plan"): {

            "running": "Performing clinical quality checks...",

            "completed": "Clinical quality checks passed",

        },

        # --------------------------------------------------
        # Approval
        # --------------------------------------------------

        ("approval", "review_plan"): {

            "running": "Waiting for therapist approval...",

            "completed": "Therapy plan approved",

        },

        # --------------------------------------------------
        # Reports
        # --------------------------------------------------

        ("report", "generate_reports"): {

            "running": "Generating reports...",

            "completed": "Reports generated",

        },

    }

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
        workflow_id: str | None = None,
    ):

        if workflow_id is None:

            workflow_id = str(uuid.uuid4())

        state = ExecutionState(
            plan=plan,
            workflow_id=workflow_id,
        )

        print("Executor EventBus:", id(workflow_events))

        workflow_events.publish(

            workflow_id=state.workflow_id,

            step=0,

            total_steps=len(plan.steps),

            skill="system",

            task="workflow",

            status="running",

            message="Workflow started",

        )

        state.context["intent"] = plan.intent

        print("\n========== EXECUTOR ==========\n")

        await self._run_steps(

            state,

        )

        # -----------------------------------------
        # Debug Workflow Events
        # -----------------------------------------

        print("\n========== WORKFLOW EVENTS ==========\n")

        for event in workflow_events.get_history(state.workflow_id):

            print(
                f"[{event.status.upper()}] "
                f"Step {event.step}/{event.total_steps} "
                f"- {event.message}"
            )

        print("\n====================================\n")

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

            # ------------------------------------------------------
            # Publish workflow started event
            # ------------------------------------------------------

            workflow_events.publish(

                workflow_id=state.workflow_id,

                step=index + 1,

                total_steps=len(state.plan.steps),

                skill=step.skill,

                task=step.task,

                status="running",

                message=self._workflow_message(step, "running",),

            )

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

        workflow_events.publish(

                workflow_id=state.workflow_id,

                step=index + 1,

                total_steps=len(state.plan.steps),

                skill=step.skill,

                task=step.task,

                status="completed",

                message=self._workflow_message(step, "completed",),

            )


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
    

    def _workflow_message(
        self,
        step,
        status: str,
    ):

        messages = self.WORKFLOW_MESSAGES.get(

            (step.skill, step.task)

        )

        if messages:

            return messages.get(

                status,

                f"{step.task} {status}",

            )

        if status == "running":

            return f"Running {step.skill}.{step.task}..."

        return f"{step.task} completed"