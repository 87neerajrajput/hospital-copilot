"""
approval.py

Approval state transitions.

This module contains no UI logic.

It simply changes the execution state.
"""

from enum import Enum

from copilot.execution_state import ExecutionState


class ApprovalStatus(str, Enum):

    WAITING = "WAITING_APPROVAL"

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"


class ApprovalService:

    @staticmethod
    def wait_for_approval(
        state: ExecutionState,
    ):

        state.status = ApprovalStatus.WAITING

        state.waiting_for_approval = True

    # -----------------------------------------------------

    @staticmethod
    def approve(
        state: ExecutionState,
    ):

        state.status = ApprovalStatus.APPROVED

        state.waiting_for_approval = False

    # -----------------------------------------------------

    @staticmethod
    def reject(
        state: ExecutionState,
    ):

        state.status = ApprovalStatus.REJECTED

        state.waiting_for_approval = False