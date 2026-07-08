"""
approval.py

Approval Skill

Consumes the human approval decision and records it
in the workflow context.

This skill never pauses execution.
"""

from copilot.execution_state import ExecutionState


class ApprovalSkill:

    async def execute(
        self,
        task: str,
        arguments: dict,
        context: dict,
        state: ExecutionState,
    ):

        if task != "review_plan":
            raise ValueError(f"Unknown approval task: {task}")

        decision = arguments["decision"].strip().lower()

        if decision in ("approve", "approved", "y", "yes"):

            state.status = "APPROVED"

            return {
                "approval_status": "approved"
            }

        if decision in ("reject", "rejected", "n", "no"):

            state.status = "REJECTED"

            return {
                "approval_status": "rejected"
            }

        raise ValueError(
            "Decision must be approve/reject (or y/n)."
        )