from pydantic import BaseModel

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)


class TherapyComparison(BaseModel):

    summary: str

    goals_added: list[str]

    goals_removed: list[str]

    weekly_schedule_changes: str

    home_program_changes: str

    treatment_evolution: str

    clinical_progression: str


class TherapyEvolution(BaseModel):

    summary: str

    treatment_journey: str

    goal_progression: str

    therapy_focus_shift: str

    caregiver_progression: str

    clinical_reasoning: str

    next_recommendations: str


structured_llm = llm.with_structured_output(
    TherapyComparison
)

structured_evolution_llm = llm.with_structured_output(
    TherapyEvolution
)

# ------------------------
# Helper function
# ------------------------
def format_plan_for_comparison(plan: dict) -> str:

    therapy = plan

    text = []

    text.append("THERAPY GOALS")

    for goal in therapy.get("therapy_goals", []):

        text.append(f"- {goal}")

    text.append("")

    text.append("WEEKLY SCHEDULE")

    for week in therapy.get("weekly_schedule", []):

        text.append(
            f"{week['week']} | {week['focus_area']}"
        )

        for activity in week["activities"]:

            text.append(f"  • {activity}")

    text.append("")

    text.append("HOME PROGRAM")

    for item in therapy.get("home_program", []):

        text.append(
            f"- {item['activity_name']}: {item['instructions']}"
        )

    return "\n".join(text)


# ------------------------
# comparison_agent()
# ------------------------

async def comparison_agent(
    left_plan: dict,
    right_plan: dict,
):
    
    from pprint import pprint

    print("\n========== LEFT PLAN ==========")
    pprint(left_plan)
    print("\n========== RIGHT PLAN ==========")
    pprint(right_plan)
    
    left_plan_text = format_plan_for_comparison(left_plan)

    right_plan_text = format_plan_for_comparison(right_plan)
    
    prompt = f"""
    You are a senior Pediatric Occupational Therapist responsible for reviewing the progression of therapy plans over time.

    Your task is NOT simply to list differences.

    Your responsibility is to perform a professional clinical comparison between two therapy plans and explain how therapy has evolved.

    The audience for this comparison includes:

    - Occupational Therapists
    - Clinical Supervisors
    - Rehabilitation Teams

    The comparison should help clinicians quickly understand how the patient's treatment plan has evolved over time.

    =========================
    THERAPY PLAN A
    =========================

    {left_plan_text}

    =========================
    THERAPY PLAN B
    =========================

    {right_plan_text}

    ==================================================
    COMPARISON INSTRUCTIONS
    ==================================================

    Compare Therapy Plan A and Therapy Plan B.

    Each plan includes metadata such as the plan ID and creation date.

    Use the creation date to determine chronological order whenever it is available.

    If Therapy Plan A is older than Therapy Plan B, describe how therapy progressed from Plan A to Plan B.

    If Therapy Plan B is older than Therapy Plan A, describe progression from Plan B to Plan A.

    If chronological order cannot be determined, simply describe the similarities and differences without assuming which plan came first.

    Focus on clinical reasoning rather than wording differences.


    ==================================================
    IMPORTANT RULES
    ==================================================

    Do NOT invent therapy goals.

    Do NOT assume clinical improvement unless supported by the plans.

    Do NOT infer patient outcomes that are not reflected in the therapy plans.

    Do NOT compare formatting, wording, or writing style.

    Base every conclusion on evidence present in the two therapy plans.
    When describing weekly schedule changes, refer only to activities explicitly present in the plans.

    Do not infer or invent therapy activities.

    ==================================================
    YOUR RESPONSIBILITIES
    ==================================================

    Compare the plans clinically.

    Consider:

    • Therapy goals
    • Weekly therapy schedule
    • Home program
    • Functional progression
    • Clinical reasoning

    Do not compare formatting.

    Do not compare wording.

    Focus on therapeutic progression.

    ==================================================
    GOALS ADDED
    ==================================================

    Identify the new therapeutic goals introduced in the newer plan.

    Summarize each goal in a concise clinical phrase.

    Do not copy the full SMART goal wording.

    ==================================================
    GOALS REMOVED
    ==================================================

    Identify the new therapeutic goals introduced in the newer plan.

    Summarize each goal in a concise clinical phrase.

    Do not copy the full SMART goal wording.

    If none, return an empty list.

    ==================================================
    WEEKLY SCHEDULE CHANGES
    ==================================================

    Explain:

    • What activities changed
    • Which weeks became more advanced
    • Any new therapeutic focus
    • Whether therapy intensity increased or decreased

    ==================================================
    HOME PROGRAM CHANGES
    ==================================================

    Explain:

    • New caregiver activities
    • Activities removed
    • Increased complexity
    • Increased independence


    ==================================================
    OVERALL TREATMENT EVOLUTION
    ==================================================

    Describe how the overall treatment strategy changed between the two plans.

    Examples:

    - foundational skills → functional independence

    - impairment-focused → participation-focused

    - feeding safety → self-feeding independence

    - sensory regulation → classroom participation

    Focus on the evolution of therapeutic priorities rather than listing individual changes.

    ==================================================
    CLINICAL PROGRESSION
    ==================================================

    Explain The therapy plan progressed...

    Examples:

    • Improved fine motor control
    • Better sensory regulation
    • Increased independence
    • Improved bilateral coordination
    • Improved feeding safety

    Base your reasoning ONLY on the therapy plans.

    When describing weekly schedule changes, refer only to activities explicitly present in the plans.

    Do not infer or invent therapy activities.

    ==================================================
    SUMMARY
    ==================================================

    SUMMARY

    Write an executive summary that could be pasted directly into a patient's clinical record.

    The summary should explain:

    - the major changes between the two plans
    - the clinical reasoning behind those changes
    - the patient's overall therapeutic trajectory

    Limit the summary to 150 words.

    Use professional clinical documentation language.
    """


    comparison = structured_llm.invoke([
    SystemMessage(
        content="""
        You are an experienced pediatric occupational therapist specializing in longitudinal treatment planning.

        Your job is to compare therapy plans clinically, not grammatically.

        Focus on therapeutic progression, treatment evolution, and clinical reasoning.

        Return structured data only.
        """
            ),
            HumanMessage(content=prompt)
        ])
    

    return comparison.model_dump()



def analyze_evolution(history):

    prompt = f"""
    You are an experienced pediatric occupational therapist specializing in
    longitudinal treatment planning.

    Below is the complete chronological therapy history of one child.

    {history}

    Analyze how therapy evolved across all therapy plans.

    Focus on:

    • Overall treatment journey
    • Progression of therapy goals
    • Changes in therapy focus
    • Evolution of caregiver/home program
    • Clinical reasoning behind these changes
    • Recommendations for the next phase of therapy

    Return structured data only.
    """

    evolution = structured_evolution_llm.invoke(
        [
            SystemMessage(
                content="""
You are an experienced pediatric occupational therapist.

Your job is to analyze long-term therapy progression across multiple therapy plans.

Focus on longitudinal clinical reasoning rather than comparing only two plans.

Return structured data only.
"""
            ),
            HumanMessage(content=prompt),
        ]
    )

    return evolution.model_dump()