from typing_extensions import TypedDict

class HealthcareState(TypedDict):

    user_query: str

    patient_info: dict | None

    patient_id: int | None

    therapy_plan: dict | None

    plan_id: int | None

    retrieved_docs: list[str] | None

    qa_result: dict | None

    approval_status: str | None

    clinical_report: str | None
    parent_report: str | None

    clinical_report_id: int | None
    parent_report_id: int | None

    next_agent: str