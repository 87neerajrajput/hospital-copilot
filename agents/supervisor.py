from graph.state import HealthcareState


def supervisor(state: HealthcareState):

    print("\n=== SUPERVISOR ===")

    print("patient_info =", state.get("patient_info"))
    print("retrieved_docs =", state.get("retrieved_docs"))
    print("therapy_plan =", state.get("therapy_plan"))


    if not state.get("patient_info"):
        print("Routing to Intake")
        return {
            "next_agent": "intake"
        }

    if not state.get("retrieved_docs"):
        print("Routing to Retriever")
        return {
            "next_agent": "retriever"
        }
    
    if not state.get("therapy_plan"):
        print("Routing to Planner")
        return {
            "next_agent": "planner"
        }
    
    if not state.get("qa_result"):
        print("Routing to QA")
        return {
            "next_agent": "qa"
        }
    
    if not state.get("approval_status"):
        print("Routing to Human Approval")
        return {
            "next_agent": "human_review"
        }
    
    if state.get("approval_status") != "approved":
        print("\n=== Routing to END ===")
        return {
            "next_agent": "end"
        }
    
    if not state.get("clinical_report"):
        print("Routing to Report Agent")
        return {
            "next_agent": "report"
        }

    print("\n=== Routing to END ===")
    return {
        "next_agent": "end"
    }