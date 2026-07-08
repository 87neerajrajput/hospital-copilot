from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import HealthcareState
#from tools.db_tools import save_therapy_plan

from hospital_mcp.hospital_client import HospitalMCPClient

load_dotenv()

# ==========================================================
# MCP CLIENT
# ==========================================================

mcp = HospitalMCPClient()

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

# 2. Initialize the Groq model
# Low temperature (0) keeps the extraction strict and deterministic
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    #model="llama-3.1-8b-instant",
    temperature=0
)

# 3. Create the structured wrapper
# This forces the LLM to output data fitting the Pydantic schema perfectly
structured_llm = llm.with_structured_output(TherapyPlan)

# 4. Define your execution prompt



async def planning_agent(state: HealthcareState, auto_save: bool = True):
    print("\n=== Planning Agent ===")
    patient_info = state['patient_info']
    retrieved_docs = state["retrieved_docs"]
    knowledge_context = "\n\n".join(retrieved_docs)
    assessment_summary = state.get("assessment_summary")

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

    3. Clinical observations

    4. Retrieved clinical knowledge

    Your therapy plans should be individualized rather than diagnosis-based.

    Every recommendation must be clinically justified by the available assessment findings whenever possible.

    PATIENT INFORMATION
    ===================
    {patient_info}

    ASSESSMENT FINDINGS
    ===================
    {assessment_context}

    KNOWLEDGE BASE CONTEXT
    ======================
    {knowledge_context}

    Create a clinically appropriate and individualized therapy plan.

    Requirements:

    1. Use BOTH the patient information and assessment findings.

    2. Prioritize functional limitations identified in the assessment.

    3. If sensory processing findings exist,
    integrate sensory-based interventions.

    4. If communication deficits exist,
    include communication-supportive activities.

    5. If ADL limitations exist,
    include functional independence goals.

    6. If behavioural observations exist,
    include regulation and behaviour management strategies.

    7. Address ALL identified concerns.

    8. Use recommendations supported by the retrieved clinical knowledge.

    9. Create specific, measurable, age-appropriate SMART goals.

    10. Ensure weekly activities progressively build toward long-term goals.

    11. Ensure every home program activity directly reinforces the weekly intervention.
    
    Generate:

    -----------------------------------------
    THERAPY GOALS
    -----------------------------------------
    3-5 SMART goals.

    Each goal should:
    - Be specific
    - Be measurable
    - Be achievable
    - Be clinically meaningful

    -----------------------------------------
    WEEKLY THERAPY SCHEDULE
    -----------------------------------------
    Provide 4 weeks.

    For each week include:
    - Week
    - Focus Area
    - Activities
    - Expected Outcome

    Expected outcomes should clearly contribute toward therapy goals.

    -----------------------------------------
    HOME PROGRAM SUGGESTIONS
    -----------------------------------------
    Provide 5-10 home activities.

    For each activity include:
    - Activity Name
    - Instructions
    - Recommended Frequency

    Instructions should be practical and easy for caregivers to follow.

    Ensure the therapy goals, weekly schedule, and home program are fully aligned.
    """

    # 5. Invoke the structured model
    # The output is NOT a string or markdown text. It is a Python Pydantic Object.
    profile = structured_llm.invoke([
        SystemMessage(content="""
        You are a senior pediatric occupational therapist.

        Create high-quality therapy plans that will undergo clinical quality assurance review.

        Requirements:

        - Address every identified concern.
        - Create specific and measurable therapy goals.
        - Generate a complete 4-week therapy schedule.
        - Ensure weekly activities support therapy goals.
        - Ensure home program activities reinforce therapy goals.
        - Use recommendations supported by retrieved knowledge.
        - Ensure recommendations are safe, practical, and age appropriate.

        Your output should be internally consistent and clinically defensible.
        """),
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