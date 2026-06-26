from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import HealthcareState

load_dotenv()

class QAResult(BaseModel):
    status: str
    concern_coverage: bool
    knowledge_alignment: bool
    completeness: bool
    clinical_quality: bool
    internal_consistency: bool
    issues: List[str]
    suggestions: List[str]


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

structured_llm = llm.with_structured_output(QAResult)


def qa_agent(state: HealthcareState):

    print("\n=== QA AGENT ===")

    patient_info = state["patient_info"]
    retrieved_docs = state["retrieved_docs"]
    therapy_plan = state["therapy_plan"]
    therapy_goals = therapy_plan["therapy_goals"]
    weekly_schedule = therapy_plan["weekly_schedule"]
    home_program = therapy_plan["home_program"]

    knowledge_context = "\n\n".join(retrieved_docs)

    PROMPT = f"""
    You are a senior pediatric occupational therapist performing quality assurance on a therapy plan.

    Your role is to identify MAJOR clinical, safety, or structural problems.

    You are NOT performing an academic review and you are NOT looking for perfection.

    Assume the therapy plan was created by a competent therapist unless there is clear evidence otherwise.

    ==================================================
    PATIENT INFORMATION
    ==================================================

    {patient_info}

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

    1. Focus only on clinically meaningful issues.

    2. Do not fail a plan simply because:
    - It could be more detailed.
    - It could be more measurable.
    - Additional activities could be added.
    - Better wording is possible.
    - More advanced clinical reasoning could be applied.

    3. Prefer suggestions over failures.

    4. When uncertain, assume the therapist's recommendation is reasonable.

    5. PASS should be the default outcome unless a significant problem exists.

    ==================================================
    CONCERN COVERAGE
    ==================================================

    Verify that major patient concerns are reasonably addressed.

    A concern is considered addressed if:

    - At least one therapy goal targets it, OR
    - At least one therapy activity targets it, OR
    - At least one home program activity supports it.

    Do NOT require every concern to appear in every section.

    Only fail if a major concern is completely ignored.

    ==================================================
    KNOWLEDGE BASE ALIGNMENT
    ==================================================

    Verify that recommendations are generally consistent with the retrieved knowledge.

    Do NOT fail because:
    - Other activities could have been included.
    - The plan is not exhaustive.
    - The plan uses alternative but reasonable approaches.

    Only fail if recommendations clearly contradict the retrieved knowledge.

    ==================================================
    COMPLETENESS
    ==================================================

    Verify that the plan contains:

    Therapy Goals
    - At least 3 goals

    Weekly Schedule
    - Week 1 through Week 4
    - Focus Area
    - Activities
    - Expected Outcome

    Home Program
    - Activity Name
    - Instructions
    - Recommended Frequency

    Only fail if a required section is missing.

    ==================================================
    CLINICAL QUALITY
    ==================================================

    Evaluate whether recommendations are:

    - Safe
    - Reasonable
    - Age appropriate
    - Practical for caregivers

    Do NOT fail because:
    - Goals could be more measurable.
    - Activities could be more detailed.
    - Instructions could be expanded.

    Only fail if there is a clear clinical concern.

    ==================================================
    INTERNAL CONSISTENCY
    ==================================================

    Verify that:

    - Therapy goals generally align with activities.
    - Home program generally supports therapy goals.
    - Expected outcomes generally support therapy goals.

    Do NOT require perfect alignment.

    Minor gaps should be suggestions.

    Only fail if there is a major contradiction.

    ==================================================
    EVIDENCE REQUIREMENT
    ==================================================

    Every issue must include:

    1. The issue.
    2. Evidence from the plan.
    3. Why it matters clinically.

    Do not invent issues.

    Do not speculate.

    ==================================================
    FINAL DECISION
    ==================================================

    Return PASS if:

    - Required sections exist.
    - Major concerns are reasonably addressed.
    - Recommendations are safe.
    - No major contradictions exist.

    Return FAIL only if:

    - A required section is missing.
    - A major concern is completely unaddressed.
    - Recommendations are unsafe.
    - Recommendations clearly contradict the knowledge base.
    - Major contradictions exist.

    ==================================================
    MINOR IMPROVEMENTS
    ==================================================

    Use suggestions instead of failures for:

    - Better goal wording.
    - Additional activities.
    - More measurable goals.
    - Additional home activities.
    - More detailed caregiver instructions.
    - Optional clinical enhancements.

    ==================================================
    IMPORTANT
    ==================================================

    When uncertain:

    PASS with suggestions.

    Do not fail a therapy plan unless there is strong evidence that a significant clinical issue exists.

    ==================================================
    OUTPUT
    ==================================================

    Return:

    - status
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