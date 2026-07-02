from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import HealthcareState

load_dotenv()

class QAResult(BaseModel):

    status: str

    assessment_alignment: str

    concern_coverage: str

    knowledge_alignment: str

    completeness: str

    clinical_quality: str

    internal_consistency: str

    issues: List[str]

    suggestions: List[str]


llm = ChatGroq(
    #model="llama-3.3-70b-versatile",
    model="llama-3.1-8b-instant",
    temperature=0
)

structured_llm = llm.with_structured_output(QAResult)


def qa_agent(state: HealthcareState):

    print("\n=== QA AGENT ===")

    patient_info = state["patient_info"]
    retrieved_docs = state["retrieved_docs"]
    therapy_plan = state["therapy_plan"]
    assessment_summary = state["assessment_summary"]
    therapy_goals = therapy_plan["therapy_goals"]
    weekly_schedule = therapy_plan["weekly_schedule"]
    home_program = therapy_plan["home_program"]

    knowledge_context = "\n\n".join(retrieved_docs)

    assessment_context = ""

    if assessment_summary:

        assessment_context = f"""
        ASSESSMENT FINDINGS
        ===================

        Diagnosis Confidence:
        {assessment_summary.get("diagnosis_confidence","Not Available")}

        Diagnosis Reason:
        {assessment_summary.get("diagnosis_reason","Not Available")}

        Clinical Findings:
        {assessment_summary.get("clinical_findings","Not Available")}

        Developmental Findings:
        {assessment_summary.get("developmental_findings","Not Available")}

        Sensory Findings:
        {assessment_summary.get("sensory_findings","Not Available")}

        Communication Findings:
        {assessment_summary.get("communication_findings","Not Available")}

        Behaviour Findings:
        {assessment_summary.get("behavior_findings","Not Available")}

        ADL Findings:
        {assessment_summary.get("adl_findings","Not Available")}
        """


    PROMPT = f"""
    You are a senior pediatric occupational therapist performing quality assurance on an AI-generated therapy plan.

    Your responsibility is to identify ONLY clinically significant problems.

    Assume the therapy plan was created by a competent pediatric therapist unless there is strong evidence otherwise.

    ==================================================
    PATIENT INFORMATION
    ==================================================

    {patient_info}

    ==================================================
    ASSESSMENT FINDINGS
    ==================================================

    {assessment_context}

    ==================================================
    KNOWLEDGE BASE CONTEXT
    ==================================================

    {knowledge_context}

    ==================================================
    THERAPY GOALS
    ==================================================

    {therapy_goals}

    ==================================================
    WEEKLY THERAPY SCHEDULE
    ==================================================

    {weekly_schedule}

    ==================================================
    HOME PROGRAM
    ==================================================

    {home_program}

    ==================================================
    REVIEW PRINCIPLES
    ==================================================

    PASS should be the default outcome.

    Focus ONLY on clinically meaningful issues.

    Do NOT fail because:

    - Goals could be more measurable.
    - Activities could be more detailed.
    - Additional interventions could be included.
    - Better wording is possible.
    - Alternative reasonable interventions exist.

    Provide suggestions instead of failures whenever possible.

    ==================================================
    ASSESSMENT ALIGNMENT
    ==================================================

    Use the assessment findings as the primary clinical reference.

    Verify that the therapy plan reasonably addresses:

    - Functional limitations
    - Developmental findings
    - Sensory findings
    - Communication findings
    - Behavioural findings
    - ADL findings

    Do NOT expect every assessment finding to become a therapy goal.

    Only fail if a major functional problem identified in the assessment has been completely ignored.

    ==================================================
    PATIENT CONCERN COVERAGE
    ==================================================

    Verify that major patient concerns are reasonably addressed.

    A concern is considered addressed if it appears in ANY of:

    - Therapy Goals
    - Weekly Activities
    - Home Program

    Do NOT require every concern to appear in every section.

    Only fail if a major concern is completely ignored.

    ==================================================
    KNOWLEDGE ALIGNMENT
    ==================================================

    Verify that recommendations are generally consistent with the retrieved clinical knowledge.

    Do NOT fail because:

    - Additional activities could have been included.
    - Multiple acceptable treatment approaches exist.

    Only fail if recommendations clearly contradict accepted clinical knowledge.

    ==================================================
    COMPLETENESS
    ==================================================

    Verify that the therapy plan contains:

    Therapy Goals
    - At least 3 goals

    Weekly Schedule
    - Week 1–Week 4
    - Focus Area
    - Activities
    - Expected Outcome

    Home Program
    - Activity Name
    - Instructions
    - Recommended Frequency

    Only fail if an entire required section is missing.

    ==================================================
    CLINICAL QUALITY
    ==================================================

    Evaluate whether recommendations are:

    - Safe
    - Age appropriate
    - Functional
    - Practical for caregivers
    - Consistent with assessment findings

    Do NOT fail because interventions could be more advanced.

    Only fail if there is a clear clinical concern.

    ==================================================
    INTERNAL CONSISTENCY
    ==================================================

    Verify that:

    - Therapy goals support assessment findings.
    - Weekly activities support therapy goals.
    - Home program supports therapy goals.
    - Expected outcomes support therapy goals.

    Minor inconsistencies should become suggestions.

    Only fail if there is a major contradiction.

    ==================================================
    EVIDENCE REQUIREMENT
    ==================================================

    Every issue must include:

    1. The issue.
    2. Evidence from the therapy plan or assessment.
    3. Why it matters clinically.

    Never invent issues.

    Never speculate.

    ==================================================
    FINAL DECISION
    ==================================================

    Return PASS when:

    - Required sections exist.
    - Major assessment findings are reasonably addressed.
    - Major patient concerns are reasonably addressed.
    - Recommendations are safe.
    - Recommendations are generally evidence-based.
    - No major contradictions exist.

    Return FAIL only when:

    - A required section is missing.
    - A major assessment finding is completely ignored.
    - A major patient concern is completely ignored.
    - Recommendations are unsafe.
    - Recommendations clearly contradict the retrieved knowledge.
    - Major internal contradictions exist.

    ==================================================
    SUGGESTIONS
    ==================================================

    Use suggestions for:

    - Better goal wording.
    - Additional activities.
    - More measurable goals.
    - Optional home activities.
    - Improved caregiver education.
    - Optional clinical enhancements.

    ==================================================
    IMPORTANT
    ==================================================

    When uncertain:

    PASS with suggestions.

    Do not fail a therapy plan unless there is strong evidence of a clinically significant problem.

    ==================================================
    OUTPUT
    ==================================================

    Return:

    - status
    - assessment_alignment
    - concern_coverage
    - knowledge_alignment
    - completeness
    - clinical_quality
    - internal_consistency
    - issues
    - suggestions
    """
    

    qa_result = structured_llm.invoke([
        SystemMessage(
            content="""
            You are a senior pediatric occupational therapist and clinical quality reviewer.

            You review therapy plans for children with developmental,
            neurological, sensory, fine motor, visual motor,
            handwriting, and autism-related challenges.

            Your role is to determine whether a therapy plan is
            clinically acceptable and safe.

            Only identify issues when supported by evidence from:
            - Patient information
            - Therapy goals
            - Weekly schedule
            - Home program
            - Retrieved knowledge base context

            Major issues should be reported as issues.

            Minor improvements should be reported as suggestions.

            When uncertain, prefer suggestions rather than failures.

            Your goal is balanced and evidence-based review.
            """
        ),
        HumanMessage(content=PROMPT)
    ])

    result = qa_result.model_dump()

    print("\nQA Result:")
    print(result)

    return {
        "qa_result": result
    }