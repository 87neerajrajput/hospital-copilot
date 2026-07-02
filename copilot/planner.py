"""
planner.py

Milestone 9.1

LLM Planner

Receives a therapist request and converts it into a
structured execution plan.

The planner ONLY creates plans.

It NEVER executes anything.
"""

from typing import List, Dict

from pydantic import BaseModel, Field

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from copilot.skill_registry import SKILLS

load_dotenv()

# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)

# ==========================================================
# PLAN MODELS
# ==========================================================


class PlanStep(BaseModel):

    skill: str = Field(
        description="Business skill to use"
    )

    task: str = Field(
        description="Business task inside the skill"
    )

    arguments: Dict = Field(
        default_factory=dict
    )


class ExecutionPlan(BaseModel):

    goal: str

    steps: List[PlanStep]


# ==========================================================
# STRUCTURED LLM
# ==========================================================

planner_llm = llm.with_structured_output(
    ExecutionPlan
)


# ==========================================================
# BUILD SKILL PROMPT
# ==========================================================

def build_skill_prompt():

    prompt = []

    prompt.append("Available Skills\n")

    for skill_name, skill in SKILLS.items():

        prompt.append(f"{skill_name.title()}")

        prompt.append("-" * len(skill_name))

        prompt.append(skill["description"])

        prompt.append("")

        prompt.append("Tasks:")

        for task, description in skill["tasks"].items():

            prompt.append(
                f"- {task}: {description}"
            )

        prompt.append("")

    return "\n".join(prompt)


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = f"""
You are the Clinical Planner.

Your ONLY responsibility is to convert the therapist's request
into an execution plan.

You NEVER answer the therapist.

You NEVER explain your reasoning.

You ONLY create execution plans.

{build_skill_prompt()}

Rules

1. Use ONLY the available skills.

2. Skill names MUST exactly match the registry. Use lowercase only.

3. Use ONLY the available tasks.

4. Generate the minimum number of steps.

5. Extract patient names whenever possible.

6. Never invent runtime values.

For example:

If patient_id is not yet known, leave arguments empty.

The Executor will fill them later.

7. Never invent skills.

8. Never invent tasks.
"""

# ==========================================================
# BUILD PLAN
# ==========================================================


def build_plan(user_request: str) -> ExecutionPlan:

    prompt = f"""
    {SYSTEM_PROMPT}

    Therapist Request:

    {user_request}
    """

    plan = planner_llm.invoke(prompt)

    return plan


# ==========================================================
# DEBUG
# ==========================================================

if __name__ == "__main__":

    questions = [

        "Give activities for poor joint attention.",

        "Find patient Miller.",

        "Show Miller's latest therapy plan.",

        "Generate therapy plan for Miller.",

        "Generate report for Miller."

    ]

    for question in questions:

        print("\n=======================================")

        print(question)

        plan = build_plan(question)

        print(plan.model_dump_json(indent=2))