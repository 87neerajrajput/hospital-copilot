"""
planner.py

Natural Language Understanding (NLU) layer for the Copilot.

Responsibilities
----------------
1. Understand the therapist request.
2. Extract structured workflow information.
3. Return a WorkflowRequest.

The Planner NEVER creates execution plans.

Execution planning is handled by:

    WorkflowBuilder
        ↓
    DependencyResolver
"""

from pydantic import BaseModel, Field

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

# ==========================================================
# MODELS
# ==========================================================


class WorkflowRequest(BaseModel):

    goal: str

    intent: str

    entities: dict = Field(default_factory=dict)


# ==========================================================
# STRUCTURED OUTPUT
# ==========================================================

workflow_llm = llm.with_structured_output(
    WorkflowRequest
)

# ==========================================================
# BUILD WORKFLOW REQUEST
# ==========================================================


def build_workflow_request(
    user_request: str,
    intent: str,
) -> WorkflowRequest:
    """
    Convert a therapist request into a structured
    WorkflowRequest.

    The Supervisor already determines the intent.

    This function only extracts entities.
    """

    prompt = f"""
    You are the Natural Language Understanding component
    of a Hospital Therapist Copilot.

    Your ONLY responsibility is to extract structured
    information from the therapist request.

    You NEVER create execution steps.

    You NEVER create workflows.

    You NEVER mention skills.

    You NEVER mention tasks.

    The intent has already been determined.

    Use this exact intent:

    {intent}

    --------------------------------------

    Return ONLY:

    goal

    intent

    entities

    --------------------------------------

    Known entity names

    patient_name

    report_type
        - "parent"
        - "clinical"
        - "both"

    diagnosis

    therapy_type

    plan_selector

    --------------------------------------

    Examples

    Therapist:
    Find Miller and load his latest therapy plan.

    Output

    goal:
    Find Miller and load his latest therapy plan.

    intent:
    therapy_lookup

    entities:
    {{
        "patient_name": "Miller"
    }}

    --------------------------------------

    Therapist:
    Generate a parent report for Miller.

    entities:
    {{
        "patient_name": "Miller",
        "report_type": "parent"
    }}

    --------------------------------------

    Therapist:
    Generate a clinical report for Miller.

    entities:
    {{
        "patient_name": "Miller",
        "report_type": "clinical"
    }}

    --------------------------------------

    Therapist:
    Generate parent and clinical report for Miller.

    entities:
    {{
        "patient_name": "Miller",
        "report_type": "both"
    }}

    --------------------------------------

    Therapist:
    Generate report for Miller.

    entities:
    {{
        "patient_name": "Miller",
        "report_type": "both"
    }}

    --------------------------------------

    Therapist:

    Show Aston Martin's latest therapy plan.

    Output

    goal:
    Show Aston Martin's latest therapy plan.

    intent:
    therapy_lookup

    entities:
    {{
        "patient_name": "Aston Martin",
        "plan_selector": "latest"
    }}

    --------------------------------------

    Therapist:

    Show Aston Martin's previous therapy plan.

    Output

    goal:
    Show Aston Martin's previous therapy plan.

    intent:
    therapy_lookup

    entities:
    {{
        "patient_name": "Aston Martin",
        "plan_selector": "previous"
    }}

    --------------------------------------

    Therapist:

    Show Aston Martin's oldest therapy plan.

    Output

    goal:
    Show Aston Martin's oldest therapy plan.

    intent:
    therapy_lookup

    entities:
    {{
        "patient_name": "Aston Martin",
        "plan_selector": "oldest"
    }}

    --------------------------------------

    Therapist Request

    {user_request}
    """

    request = workflow_llm.invoke(prompt)

    request.intent = intent

    request.goal = user_request

    return request