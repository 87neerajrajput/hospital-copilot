
from pydantic import BaseModel, Field

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import HealthcareState
from typing import Optional

from hospital_mcp.hospital_client import mcp

load_dotenv()

class Reports(BaseModel):

    clinical_report: Optional[str] = Field(default=None, description="Detailed clinical report")

    parent_report: Optional[str] = Field(default=None, description="Parent-friendly report")


llm = ChatGroq(
    #model="llama-3.3-70b-versatile",
    model="llama-3.1-8b-instant",
    temperature=0
)

structured_llm = llm.with_structured_output(Reports)


async def report_agent(state: HealthcareState):

    print("\n=== REPORT AGENT ===")

    patient_info = state["patient_info"]
    therapy_plan = state["therapy_plan"]
    therapy_goals = therapy_plan["therapy_goals"]
    weekly_schedule = therapy_plan["weekly_schedule"]
    home_program = therapy_plan["home_program"]

    qa_result = state["qa_result"]

    report_types = state["report_types"]

    if report_types is None:
        report_types = ["clinical", "parent"]
    
    print(f"\n=== {report_types} ===")


    PROMPT = f"""
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

    REQUESTED REPORT TYPES
    ======================
    {", ".join(report_types)}

    Generate ONLY the requested report(s).

    Rules:

    If only "clinical" is requested:
    - Generate ONLY the Clinical Report.

    If only "parent" is requested:
    - Generate ONLY the Parent Report.

    If both are requested:
    - Generate TWO completely independent reports.

    The Clinical Report and Parent Report must NOT be rewritten versions of each other.


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

    Return ONLY the requested report(s).

    Examples:

    If Clinical is requested:
    Return only the Clinical Report.

    If Parent is requested:
    Return only the Parent Report.

    If both are requested:
    Return both reports.

    Each Report should not be more than 700 words.

    """

    SYSTEM_PROMPT = """
    You are a senior pediatric occupational therapist responsible for producing high-quality therapy documentation.

    You may be asked to generate one or more report types.

    The supported report types are:

    1. Clinical Report
    - Audience:
        Occupational therapists, clinical supervisors, physicians, hospital records.
    - Style:
        Formal, professional, clinically precise.
    - Include:
        Clinical terminology, assessment findings, treatment rationale, measurable therapy goals, functional outcomes, recommendations, and monitoring plans.

    2. Parent Report
    - Audience:
        Parents and caregivers.
    - Style:
        Warm, supportive, encouraging, easy to understand.
    - Include:
        Simple explanations, week-wise Therapy Goals plan, practical home guidance, positive reinforcement, and realistic expectations.
    - Avoid medical jargon whenever possible.

    When both reports are requested:

    - Treat them as TWO independent documents.
    - Do NOT paraphrase one report into the other.
    - Do NOT duplicate sections unnecessarily.
    - Tailor the language, structure, and level of detail to the intended audience.

    Maintain consistency with the therapy plan while adapting the presentation appropriately.

    Never mention:
    - Internal QA
    - Validation
    - Review comments
    - PASS/FAIL
    - Internal workflow
    """

    reports = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=PROMPT)
    ])

    response = reports.model_dump(exclude_none=True)

    patient_id = state["patient_id"]

    if response.get("clinical_report"):

        print("\nClinical Report Generated")

        clinical_result = await mcp.save_report(
            patient_id=patient_id,
            report_type="clinical",
            report_content=response["clinical_report"],
        )

        if clinical_result["success"]:

            clinical_report_id = clinical_result["report_id"]
            print(clinical_result["message"])

        else:

            print(clinical_result["message"])


    if response.get("parent_report"):

        print("\nParent Report Generated")

        parent_result = await mcp.save_report(
            patient_id=patient_id,
            report_type="parent",
            report_content=response["parent_report"],
        )

        if parent_result["success"]:

            parent_report_id = parent_result["report_id"]
            print(parent_result["message"])

        else:

            print(parent_result["message"])

    return {
        "clinical_report": response.get("clinical_report"),
        "parent_report": response.get("parent_report"),
        "clinical_report_id": clinical_report_id,
        "parent_report_id": parent_report_id,
    }