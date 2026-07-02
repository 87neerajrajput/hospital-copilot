"""
supervisor.py

Milestone 9.1

Clinical Supervisor

Responsibilities
----------------
1. Receive therapist request
2. Ask Planner for an execution plan
3. Return the execution plan

NOTE:
The Supervisor DOES NOT execute anything.
Execution will be added in later milestones.
"""

from pprint import pprint

from copilot.planner import build_plan


class ClinicalSupervisor:

    def __init__(self):

        pass

    # ======================================================
    # PLAN
    # ======================================================

    def plan(
        self,
        user_request: str,
    ):

        execution_plan = build_plan(user_request)

        return execution_plan


# ==========================================================
# DEBUG
# ==========================================================

if __name__ == "__main__":

    supervisor = ClinicalSupervisor()

    question = "Find Miller and show his latest therapy plan."

    plan = supervisor.plan(question)

    print("\n========== EXECUTION PLAN ==========\n")

    pprint(plan.model_dump_json(indent=2))

    print("\n====================================")