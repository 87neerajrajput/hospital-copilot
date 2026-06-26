from langgraph.types import interrupt

from graph.state import HealthcareState


def human_review(state: HealthcareState):

    print("\n=== HUMAN REVIEW ===")

    approval = interrupt(
        {
            "patient_info": state["patient_info"],
            "therapy_plan": state["therapy_plan"],
            "qa_result": state["qa_result"],
            "message": "Approve or reject therapy plan"
        }
    )

    return {
        "approval_status": approval
    }