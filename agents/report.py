from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import HealthcareState
from tools.db_tools import save_report


class Reports(BaseModel):

    clinical_report: str = Field(description="Detailed clinical report")

    parent_report: str = Field(description="Parent-friendly report")


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

structured_llm = llm.with_structured_output(Reports)


def report_agent(state: HealthcareState):

    print("\n=== REPORT AGENT ===")

    patient_info = state["patient_info"]
    therapy_plan = state["therapy_plan"]
    therapy_goals = therapy_plan["therapy_goals"]
    weekly_schedule = therapy_plan["weekly_schedule"]
    home_program = therapy_plan["home_program"]

    qa_result = state["qa_result"]

    prompt = f"""
    You are an experienced pediatric occupational therapist responsible for creating professional therapy documentation.

    PATIENT INFORMATION
    ===================
    {patient_info}

    THERAPY GOALS
    =============
    {therapy_goals}

    WEEKLY THERAPY SCHEDULE
    =======================
    {weekly_schedule}

    HOME PROGRAM
    ============
    {home_program}

    QA REVIEW RESULT
    ================
    {qa_result}

    Use QA results only to improve report quality and completeness.

    Do NOT mention:
    - PASS or FAIL status
    - QA findings
    - Internal review comments
    - Validation results
    - Review suggestions

    The reports should appear as final clinical documentation.

    Generate TWO reports.

    ====================================================
    REPORT 1: CLINICAL REPORT
    ====================================================

    Audience:
    - Occupational Therapists
    - Clinical Supervisors
    - Hospital Records

    Include the following sections:

    1. Patient Demographics
    - Name
    - Age
    - Diagnosis

    2. Presenting Concerns
    - Summary of primary challenges

    3. Clinical Assessment Summary
    - Functional impact of identified concerns
    - Areas affecting participation and daily activities

    4. Therapy Goals
    - Present all therapy goals clearly

    5. Weekly Therapy Schedule

    Organize by Week 1 through Week 4.

    For each week include:

    - Focus Area
    - Activities
    - Expected Outcomes

    6. Home Program Recommendations

    For each activity include:

    - Activity Name
    - Instructions
    - Recommended Frequency
    - Caregiver Involvement

    7. Clinical Recommendations

    Include:

    - Key treatment recommendations
    - Areas requiring monitoring
    - Suggested review timeline
    - Expected progress indicators

    Requirements:

    - Use professional clinical language.
    - Maintain a formal documentation style.
    - Ensure consistency with therapy goals and activities.
    - Present information in a structured format.

    ====================================================
    REPORT 2: PARENT REPORT
    ====================================================

    Audience:
    - Parents
    - Caregivers

    Use simple, supportive, non-clinical language.

    Include:

    1. Understanding Your Child's Needs

    - Brief explanation of current challenges
    - Focus on strengths and areas for improvement

    2. Therapy Goals

    - Explain goals in parent-friendly language

    3. What We Will Work On In Therapy

    Summarize:

    - Weekly focus areas
    - Key therapy activities
    - Expected benefits

    4. How Parents Can Help At Home

    For each home activity include:

    - Activity Name
    - Simple Instructions
    - Recommended Frequency
    - Practical Tips for Caregivers

    5. Expected Progress

    Explain:

    - What improvements parents may observe
    - How home practice supports progress

    6. Important Notes

    Include:

    - Importance of consistency
    - Importance of caregiver participation
    - Encouragement and positive reinforcement

    Requirements:

    - Use positive and encouraging language.
    - Avoid medical jargon.
    - Keep recommendations practical.
    - Make instructions easy to follow.
    - Keep the report reassuring and family-friendly.

    ====================================================
    FORMATTING REQUIREMENTS
    ====================================================

    - Use clear section headings.
    - Use professional formatting.
    - Do not return JSON.
    - Do not return markdown code blocks.
    - Return plain formatted report text.

    Return:

    1. Clinical Report
    2. Parent Report
    """

    reports = structured_llm.invoke([
        SystemMessage(
            content="""
            You are a senior pediatric occupational therapist responsible for creating professional therapy documentation.

            Your responsibilities are:

            - Create accurate clinical reports suitable for therapists, supervisors, and hospital records.
            - Create parent-friendly reports that explain therapy plans in simple language.
            - Maintain consistency with the therapy goals, weekly schedule, and home program.
            - Present information clearly and professionally.
            - Use clinical language in clinical reports.
            - Use supportive, non-technical language in parent reports.

            Do not mention internal QA processes, validation results, or review comments.

            Generate reports that are practical, professional, and ready for clinical use.
            """
        ),
        HumanMessage(content=prompt)
    ])

    result = reports.model_dump()

    print("\nClinical Report Generated")
    print("\nParent Report Generated")

    patient_id = state["patient_id"]

    clinical_report_id = save_report(
        patient_id=patient_id,
        report_type="clinical",
        report_content=result["clinical_report"]
    )

    parent_report_id = save_report(
        patient_id=patient_id,
        report_type="parent",
        report_content=result["parent_report"]
    )

    return {
        "clinical_report": result["clinical_report"],
        "parent_report": result["parent_report"],
        "clinical_report_id": clinical_report_id,
        "parent_report_id": parent_report_id
    }