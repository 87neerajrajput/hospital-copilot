"""
test_supervisor.py

End-to-end test of the planning pipeline.

This test verifies that the Supervisor can:

1. Classify therapist intent.
2. Extract workflow entities.
3. Build an execution plan.
4. Validate the plan.

No MCP calls are made.
No execution occurs.
"""

from pprint import pprint

from copilot.supervisor import ClinicalSupervisor

supervisor = ClinicalSupervisor()

questions = [

    # ---------------------------------------------
    # Patient
    # ---------------------------------------------

    #"Find Aston Martin.",

    # ---------------------------------------------
    # Therapy
    # ---------------------------------------------

    #"Show Aston Martin's latest therapy plan.",

    #"Generate a therapy plan for Aston Martin.",

    # ---------------------------------------------
    # Reports
    # ---------------------------------------------

    "Generate report for Aston Martin.",

    # ---------------------------------------------
    # QA
    # ---------------------------------------------

    #"Validate Aston Martin's therapy plan.",

    # ---------------------------------------------
    # Knowledge
    # ---------------------------------------------

    #"What is sensory integration?",

]

for question in questions:

    print("\n")
    print("=" * 100)

    print(question)

    print("=" * 100)

    plan = supervisor.plan(question)

    print("\nExecution Plan\n")

    pprint(plan.model_dump())