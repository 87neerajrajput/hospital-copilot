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

    report_types: list[str] | None = None


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
        """Return ONLY:

        - intent
        - reason
        - report_types

        Rules:

        - report_types should only be populated when the intent is report_generation.
        - For all other intents, return null.
        """
    )

    prompt.append(
        "Do NOT generate workflows.\n"
    )

    prompt.append(
        "Do NOT generate execution steps.\n"
    )

    prompt.append(
        """
        Classification Rules
        ====================

        1. If the therapist refers to a patient by name
        (for example: "Find John", "Show John's therapy plan",
        "Generate report for John"), always choose the patient-
        related intent, NOT knowledge_search.

        2. knowledge_search is ONLY for requests asking for
        general clinical information or definitions, such as:
        - What is sensory integration?
        - Explain dyspraxia.
        - What causes toe walking?

        3. patient_search is ONLY for locating an existing patient.

        If the therapist refers to ONE therapy plan
        (latest, previous, oldest, plan #84, or a plan by date),
        choose therapy_lookup.

        If the therapist refers to MULTIPLE therapy plans
        (history, all plans, previous plans, therapy history),
        choose therapy_history.

        4. therapy_lookup

            Choose this intent when the therapist wants to retrieve
            ONE specific therapy plan.

            This includes selecting a plan by:

            - latest
            - previous
            - oldest
            - plan number
            - date

            Examples:

            - Show Aston Martin's latest therapy plan.
            - Show Aston Martin's previous therapy plan.
            - Show Aston Martin's oldest therapy plan.
            - Open therapy plan #84.
            - Open Aston Martin's July 5 therapy plan.

        ------------------------------------

        5. therapy_history

            Choose this intent ONLY when the therapist wants to
            browse or inspect MULTIPLE therapy plans.

            Examples:

            - Show Aston Martin's therapy history.
            - List Aston Martin's therapy plans.
            - Show all therapy plans.
            - Show previous therapy plans.
            - How many therapy plans does Aston Martin have?

            
        ------------------------------------

        6. therapy_comparison

            Choose this intent when the therapist wants to compare
            two therapy plans for the same patient.

            Examples:

            - Compare Aston Martin's latest and previous therapy plans.
            - Compare the latest two therapy plans.
            - Compare today's plan with the previous plan.
            - Compare plan 82 with plan 87.
            - What changed between Aston Martin's last two therapy plans?
            - Compare the current therapy plan with the previous one.

        Do NOT choose therapy_lookup when the therapist asks to compare plans.

        Comparison is a separate workflow and should always use
        therapy_comparison.

        ------------------------------------------

        7. therapy_evolution

            Use this intent when the therapist wants an overall summary of how a patient's therapy has evolved across multiple therapy plans over time.

            Examples:
            - How has Aston's therapy evolved?
            - Show therapy evolution.
            - Summarize therapy progression.
            - How has treatment changed over time?
            - How has the patient's therapy progressed?

            Do NOT use this intent when the therapist specifies two particular plans to compare. Those requests should use therapy_comparison.

        ------------------------------------------

        8. therapy_trend

            Use this intent when the therapist wants to understand
            overall clinical progress rather than simply describing
            how therapy evolved.

            Examples:

            • Is Rehan improving?
            • Has therapy plateaued?
            • Is there regression?
            • Which therapy domains improved the most?
            • What should be prioritized next?
            • How is the patient's overall progress?

        ------------------------------------------

        9. therapy_generation

            Choose this intent when the therapist wants to create
            a NEW therapy plan.

            Examples:
            - Generate a therapy plan.
            - Create a therapy plan.
            - Make a therapy plan.

        ------------------------------------

        10. therapy_review

            Choose this intent when the therapist wants a clinical
            evaluation or quality review of an existing therapy plan.

            Examples:

            - Review Aston Martin's therapy plan.
            - Re-review Aston Martin's therapy plan.
            - Clinically review Aston Martin's therapy plan.

        ------------------------------------

        11. qa validates a newly generated therapy plan before
        human approval.

        12. report_generation

        Choose this intent when the therapist wants to generate
        clinical reports or parent reports from an existing therapy plan.

        Examples:
        - Generate a parent report.
        - Generate a clinical report.
        - Generate both reports.


        13. If the intent is report_generation, determine which report(s) the therapist requested.

        Report Types:

        - "parent" → Parent Report
        - "clinical" → Clinical Report

        Examples:

        "Generate a parent report for John."
        → report_types = ["parent"]

        "Generate a clinical report for John."
        → report_types = ["clinical"]

        "Generate a parent and clinical report for John."
        → report_types = ["parent", "clinical"]

        "Generate a report for John."
        → report_types = ["parent", "clinical"]

        Examples

        User:
        Generate a parent report for Aston Martin.

        Output:
        {{
        "intent": "report_generation",
        "reason": "The therapist wants a parent report for an existing therapy plan.",
        "report_types": ["parent"]
        }}

        User:
        Generate a clinical report for Aston Martin.

        Output:
        {{
        "intent": "report_generation",
        "reason": "The therapist wants a clinical report for an existing therapy plan.",
        "report_types": ["clinical"]
        }}

        User:
        Generate a report for Aston Martin.

        Output:
        {{
        "intent": "report_generation",
        "reason": "The therapist wants both reports for an existing therapy plan.",
        "report_types": ["parent", "clinical"]
        }}

        """
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

        print(f"Report Types : {decision.report_types}")

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

    question = "Find Aston Martin."

    plan = supervisor.plan(question)

    print("\n========== EXECUTION PLAN ==========\n")

    pprint(plan.model_dump())

    print("\n====================================")