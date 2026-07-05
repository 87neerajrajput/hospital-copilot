"""
supervisor.py

AI Clinical Supervisor

Responsibilities
----------------
1. Classify the therapist's intent.
2. Extract structured workflow information.
3. Build a deterministic execution plan.
4. Validate the execution plan.

The Supervisor NEVER determines execution steps.

Execution planning is delegated to:

    WorkflowBuilder
        ↓
    DependencyResolver
"""

from pydantic import BaseModel, Field

from langchain_groq import ChatGroq

from copilot.intent_registry import INTENTS

from copilot.planner import build_workflow_request

from copilot.workflow_builder import WorkflowBuilder

from copilot.plan_validator import (
    PlanValidator,
    PlanValidationError,
)


# ==========================================================
# SUPERVISOR OUTPUT
# ==========================================================

class SupervisorDecision(BaseModel):

    intent: str = Field(
        description="Detected therapist intent."
    )

    reason: str = Field(
        description="Reason for selecting the intent."
    )


# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    temperature=0,

)

structured_llm = llm.with_structured_output(
    SupervisorDecision
)


# ==========================================================
# BUILD PROMPT
# ==========================================================

def build_supervisor_prompt() -> str:
    """
    Build the supervisor prompt dynamically from
    the Intent Registry.

    This avoids duplicating intent definitions.
    """

    prompt = []

    prompt.append(
        "You are an AI Clinical Supervisor.\n"
    )

    prompt.append(
        "Your ONLY responsibility is to classify the therapist's request.\n"
    )

    prompt.append(
        "Return ONLY the detected intent and a short reason.\n"
    )

    prompt.append(
        "Do NOT generate workflows.\n"
    )

    prompt.append(
        "Do NOT generate execution steps.\n"
    )

    prompt.append(
        "\nAvailable Intents\n"
    )

    prompt.append("=================\n")

    for intent_name, info in INTENTS.items():

        prompt.append(f"{intent_name}")

        prompt.append(
            f"Description: {info['description']}"
        )

        prompt.append("")

    return "\n".join(prompt)


# ==========================================================
# CLINICAL SUPERVISOR
# ==========================================================

class ClinicalSupervisor:

    def __init__(self):

        self.workflow_builder = WorkflowBuilder()

        self.validator = PlanValidator()

    # ======================================================
    # PLAN
    # ======================================================

    def plan(
        self,
        user_request: str,
    ):

        # --------------------------------------------------
        # 1. Intent Classification
        # --------------------------------------------------

        decision = structured_llm.invoke(

            f"""
            {build_supervisor_prompt()}

            Therapist Request

            {user_request}
            """

        )

        print("\n========== SUPERVISOR ==========\n")

        print(f"Intent : {decision.intent}")

        print(f"Reason : {decision.reason}")

        print("\n===============================\n")

        # --------------------------------------------------
        # 2. Workflow Request
        # --------------------------------------------------

        workflow_request = build_workflow_request(

            user_request=user_request,

            intent=decision.intent,

        )

        print("\n========== WORKFLOW REQUEST ==========\n")

        print("Goal :")

        print(workflow_request.goal)

        print("\nIntent :")

        print(workflow_request.intent)

        print("\nEntities :")

        print(workflow_request.entities)

        print("\n======================================\n")

        # --------------------------------------------------
        # 3. Deterministic Planning
        # --------------------------------------------------

        execution_plan = self.workflow_builder.build(

            intent=workflow_request.intent,

            goal=workflow_request.goal,

            entities=workflow_request.entities,

        )

        # --------------------------------------------------
        # 4. Validation
        # --------------------------------------------------

        try:

            self.validator.validate(

                execution_plan

            )

        except PlanValidationError:

            print("\n========== PLAN VALIDATION ==========\n")

            raise

        return execution_plan
    

# ==========================================================
# DEBUG
# ==========================================================

from pprint import pprint

if __name__ == "__main__":

    supervisor = ClinicalSupervisor()

    question = "Validate Aston Martin's therapy plan."

    plan = supervisor.plan(question)

    print("\n========== EXECUTION PLAN ==========\n")

    pprint(plan.model_dump())

    print("\n====================================")