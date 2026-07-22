from typing import List
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from prompts.agent_planner_prompt import PLANNER_SYSTEM_PROMPT
from graph.state import HealthcareState
from hospital_mcp.hospital_client import mcp

# 1. Define the structural schema using Pydantic
class WeeklyPlan(BaseModel):
    week: str
    focus_area: str
    activities: List[str]
    expected_outcome: str

class HomeProgramActivity(BaseModel):
    activity_name: str
    instructions: str
    recommended_frequency: str

class TherapyPlan(BaseModel):    
    therapy_goals: List[str] = Field(description="Therapy goals and recommendations")
    weekly_schedule: List[WeeklyPlan]
    home_program: List[HomeProgramActivity]


# 4. Define your execution prompt
async def planning_agent(state: HealthcareState, auto_save: bool = True):
    print("\n=== Planning Agent ===")
    patient_info = state['patient_info']
    retrieved_docs = state["retrieved_docs"]
    knowledge_context = "\n\n".join(retrieved_docs)
    assessment_summary = state.get("assessment_summary")
    clinical_memory = state.get("clinical_memory", {},)

    # -----------------------------------------
    # Assessment Context
    # -----------------------------------------

    assessment_context = ""

    if assessment_summary:

        assessment_context = f"""
        Assessment Findings
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
    You are a senior pediatric occupational therapist with expertise in:

    • Autism Spectrum Disorder
    • ADHD
    • Developmental Delay
    • Sensory Integration
    • Pediatric Neurology
    • Early Intervention

    Always integrate:

    1. Patient demographics
    2. Assessment findings
    3. Clinical memory
    4. Retrieved clinical knowledge

    Your therapy plans should always be individualized rather than diagnosis-based.

    Every recommendation must be clinically justified using the available assessment findings and evidence from the knowledge base whenever possible.

    ==================================================================
    PATIENT INFORMATION
    ==================================================================

    {patient_info}

    ==================================================================
    ASSESSMENT FINDINGS
    ==================================================================

    {assessment_context}

    ==================================================================
    CLINICAL MEMORY
    ==================================================================

    {clinical_memory}

    Clinical Memory may contain one or more previous approved therapy plans.

    When previous therapy plans are available:

    - Review previous therapy goals before creating new ones.
    - Continue goals that remain clinically relevant.
    - Progress goals instead of restarting them whenever appropriate.
    - Avoid repeating identical weekly schedules.
    - Avoid repeating identical home program activities unless continued practice is clinically justified.
    - Build naturally on previous interventions.
    - If introducing new goals or interventions, ensure they are supported by current assessment findings.
    - If regression or plateau is evident, modify the treatment approach accordingly.
    - Maintain continuity of care across therapy sessions.

    If no previous therapy plan exists, generate a completely new therapy plan.

    ==================================================================
    KNOWLEDGE BASE CONTEXT
    ==================================================================

    {knowledge_context}

    Create a clinically appropriate, evidence-based and individualized therapy plan.

    Requirements:

    1. Use BOTH patient information and assessment findings.

    2. Use Clinical Memory to maintain continuity of care.

    3. Prioritize functional limitations identified in the assessment.

    4. If sensory processing findings exist,
    integrate sensory-based interventions.

    5. If communication deficits exist,
    include communication-supportive activities.

    6. If ADL limitations exist,
    include functional independence goals.

    7. If behavioural observations exist,
    include regulation and behaviour management strategies.

    8. Address ALL identified concerns.

    9. Use recommendations supported by the retrieved clinical knowledge.

    10. Create specific, measurable, age-appropriate SMART goals.

    11. Ensure weekly activities progressively build toward long-term goals.

    12. Ensure home program activities directly reinforce the weekly intervention.

    13. Avoid unnecessary duplication of previous therapy plans.

    14. The new therapy plan should represent the patient's current stage of therapy, not restart treatment from the beginning.

    Generate:

    -----------------------------------------
    THERAPY GOALS
    -----------------------------------------

    Provide 3-5 SMART goals.

    Each goal must be:

    - Specific
    - Measurable
    - Achievable
    - Relevant
    - Time-bound

    -----------------------------------------
    WEEKLY THERAPY SCHEDULE
    -----------------------------------------

    Provide a progressive 4-week schedule.

    For each week include:

    - Week
    - Focus Area
    - Activities
    - Expected Outcome

    Each week's activities should naturally progress from the previous week.

    -----------------------------------------
    HOME PROGRAM
    -----------------------------------------

    Provide 5-10 caregiver-friendly activities.

    For each activity include:

    - Activity Name
    - Instructions
    - Recommended Frequency

    Home activities should reinforce the therapy goals and weekly intervention plan.

    Ensure the Therapy Goals, Weekly Schedule and Home Program are internally consistent and clinically aligned.
    """

    # 5. Invoke the structured model
    # The output is NOT a string or markdown text. It is a Python Pydantic Object.

    # 2. Create the structured wrapper
    # This forces the LLM to output data fitting the Pydantic schema perfectly
    
    from services.llm_service import get_llm

    llm = get_llm()
    
    structured_llm = llm.with_structured_output(TherapyPlan)

    profile = structured_llm.invoke([
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=PROMPT)
    ])

    therapy_plan = profile.model_dump()

    plan_id = None

    if auto_save:

        result = await mcp.save_therapy_plan(
            state["patient_id"],
            patient_info,
            therapy_plan,
        )

        if result["success"]:

            plan_id = result["plan_id"]

            print(result["message"])

        else:

            print(result["message"])

    return {
        "therapy_plan": therapy_plan,
        "plan_id": plan_id,
    }