
import asyncio
from graph.state import HealthcareState
from services.hospital_service import HospitalService

# ============================================================
# Merge therapist-entered information with AI assessment
# ============================================================

def merge_patient_information(
    manual: dict,
    assessment: dict | None,
) -> dict:
    """
    Merge therapist-entered information with
    AI extracted assessment information.

    Therapist-entered values always take priority.
    """

    if assessment is None:
        return manual

    merged = {}

    # --------------------------------------------------
    # Name
    # --------------------------------------------------

    merged["name"] = (
        manual.get("name")
        or assessment.get("name")
    )

    # --------------------------------------------------
    # Age
    # --------------------------------------------------

    merged["age"] = (
        manual.get("age")
        or assessment.get("age")
    )

    # --------------------------------------------------
    # Diagnosis
    # --------------------------------------------------

    merged["diagnosis"] = (
        manual.get("diagnosis")
        or assessment.get("diagnosis")
    )

    # --------------------------------------------------
    # Concerns
    # --------------------------------------------------

    merged_concerns = []

    for concern in (
        manual.get("concerns", [])
        + assessment.get("concerns", [])
    ):

        concern = concern.strip()

        if (
            concern
            and concern not in merged_concerns
        ):

            merged_concerns.append(concern)

    merged["concerns"] = merged_concerns

    return merged


# ============================================================
# Intake Agent
# ============================================================

def intake_agent(state: HealthcareState):

    print("\n========== Intake Agent ==========")

    print("Manual Form:")

    print(state["patient_form"])

    print("\nAssessment Summary:")

    print(state.get("assessment_summary"))

    print("=================================\n")

    # --------------------------------------------------
    # Manual therapist-entered information
    # --------------------------------------------------

    patient_info = state["patient_form"].copy()

    # --------------------------------------------------
    # Merge Assessment Summary
    # --------------------------------------------------

    patient_info = merge_patient_information(

        manual=patient_info,

        assessment=state.get(
            "assessment_summary"
        ),
    )

    print("\nMerged Patient Information:")

    print(patient_info)

    # --------------------------------------------------
    # Save / Update Patient
    # --------------------------------------------------

    if state.get("patient_id"):

        patient_id = state["patient_id"]

        result = HospitalService.update_patient(
            patient_id,
            patient_info,
        )

        if result["success"]:
            print("Patient updated: ", result["message"])
        else:
            print(result["message"])

    else:

        result = HospitalService.save_patient(
            patient_info
        )
        
        if result["success"]:

            print("Patient saved: ", result["message"])
            patient_id = result["patient_id"]

        else:
            print(result["message"])

        

    # --------------------------------------------------
    # Return Workflow State
    # --------------------------------------------------

    return {

        "patient_info": patient_info,

        "patient_id": patient_id,
    }