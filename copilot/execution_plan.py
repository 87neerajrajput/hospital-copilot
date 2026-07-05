from typing import Dict, List

from pydantic import BaseModel, Field


class PlanStep(BaseModel):

    skill: str

    task: str

    arguments: Dict = Field(default_factory=dict)


class ExecutionPlan(BaseModel):

    goal: str

    intent: str

    steps: List[PlanStep]