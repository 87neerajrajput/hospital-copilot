from typing_extensions import TypedDict

class HealthcareState(TypedDict):

    patient_form: dict | None

    user_query: str

    assessment_summary: dict | None

    patient_info: dict | None

    patient_id: int | None

    clinical_memory: dict | None

    therapy_plan: dict | None

    plan_id: int | None

    retrieved_docs: list[str] | None

    qa_result: dict | None

    approval_status: str | None

    report_types: list[str] | None

    clinical_report: str | None
    parent_report: str | None

    clinical_report_id: int | None
    parent_report_id: int | None

    next_agent: str