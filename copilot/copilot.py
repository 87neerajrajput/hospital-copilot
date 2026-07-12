"""
copilot.py

Public API for the Hospital Copilot.

The Streamlit UI should only call run_copilot().
"""

from copilot.supervisor import ClinicalSupervisor
from copilot.executor import Executor


async def run_copilot(
    request: str,
):

    supervisor = ClinicalSupervisor()

    executor = Executor()

    plan = supervisor.plan(request)

    state = await executor.execute(plan)

    return state