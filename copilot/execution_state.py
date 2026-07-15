"""
execution_state.py

Represents the runtime state of an executing workflow.

ExecutionState is mutable runtime state.

It is intentionally separate from ExecutionPlan.

ExecutionPlan answers:

    "What should be executed?"

ExecutionState answers:

    "What has already been executed?"

This separation allows workflows to pause,
resume, retry, or recover without rebuilding
the execution plan.
"""

from typing import Literal

from pydantic import BaseModel, Field

from copilot.execution_plan import ExecutionPlan


class ExecutionState(BaseModel):

    # ---------------------------------------------------------
    # Immutable execution plan
    # ---------------------------------------------------------

    plan: ExecutionPlan

    # ---------------------------------------------------------
    # Workflow Identity
    # ---------------------------------------------------------

    workflow_id: str

    # ---------------------------------------------------------
    # Runtime state
    # ---------------------------------------------------------

    current_step: int = 0

    context: dict = Field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Workflow status
    # ---------------------------------------------------------

    status: Literal[
        "RUNNING",
        "WAITING_FOR_APPROVAL",
        "COMPLETED",
    ] = "RUNNING"

    # --------------------------------------------------
    # Human Review
    # --------------------------------------------------

    waiting_for_approval: bool = False

    pending_step: int | None = None

    # --------------------------------------------------
    # Result
    # --------------------------------------------------

    error: str | None = None