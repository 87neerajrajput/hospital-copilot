import os
from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import HealthcareState
from tools.db_tools import save_therapy_plan

load_dotenv()

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
    temperature=0
)

# 3. Create the structured wrapper
# This forces the LLM to output data fitting the Pydantic schema perfectly
structured_llm = llm.with_structured_output(TherapyPlan)

# 4. Define your execution prompt



def planning_agent(state: HealthcareState):
    print("\n=== Planning Agent ===")
    patient_info = state['patient_info']
    retrieved_docs = state["retrieved_docs"]
    knowledge_context = "\n\n".join(retrieved_docs)

    PROMPT = f"""
    You are a senior pediatric occupational therapist.

    PATIENT INFORMATION
    ===================
    {patient_info}

    KNOWLEDGE BASE CONTEXT
    ======================
    {knowledge_context}

    Create a clinically appropriate and individualized therapy plan.

    Requirements:

    1. Address ALL identified concerns.
    2. Use recommendations supported by the knowledge base.
    3. Create specific and measurable therapy goals.
    4. Ensure goals are age-appropriate and functional.
    5. Create a 4-week therapy schedule.
    6. Ensure weekly activities directly support therapy goals.
    7. Create practical home program activities that caregivers can easily implement.
    8. Ensure home program activities reinforce therapy goals.
    9. Maintain consistency between goals, weekly schedule, and home program.

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

    print("\nGenerated Therapy Plan:")
    print(therapy_plan)

    plan_id = save_therapy_plan(
        state["patient_id"],
        patient_info,
        therapy_plan
    )

    return {
        "therapy_plan": therapy_plan,
        "plan_id": plan_id
    }