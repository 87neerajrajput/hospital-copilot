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

    #"Generate a therapy plan for Aston Martin.",

    #"Show Aston Martin's latest therapy plan.",

    #"Show Aston Martin's previous therapy plan."

    #"Show Aston Martin's oldest therapy plan."

    #"Show Aston Martin's therapy history."

    #"Find Aston Martin's therapy history."
    
    # "List Aston Martin's therapy plans."

    #"Show all therapy plans for Aston Martin."

    #"Compare Aston Martin's latest and previous therapy plans.",

    # "Compare the latest two therapy plans for Aston Martin.",

    # "Compare plan 82 with plan 87 for Aston Martin.",

    #"What changed between Aston Martin's latest and previous therapy plans?",

    # "Compare today's therapy plan with the previous one for Aston Martin.",

    # ---------------------------------------------
    # Therapy Review
    # ---------------------------------------------

    #"Review Aston Martin's therapy plan."

    # ---------------------------------------------
    # Reports
    # ---------------------------------------------

    # "Generate report for Aston Martin.",

    # "Generate a clinical report for Aston Martin.",

    # ---------------------------------------------
    # QA
    # ---------------------------------------------

    #"Validate Aston Martin's therapy plan.",

    # ---------------------------------------------
    # Knowledge
    # ---------------------------------------------

    #"What is sensory integration?",

    #"Explain dyspraxia.",

    # "How has Rehan's therapy evolved?"

    #"Is Rehan making progress?",

    #"Has Rehan plateaued?"

    #"Is therapy working for Rehan?"

    #"Has Rehan regressed?"
    "Generate a therapy plan for Rehan."

]

for question in questions:

    print("\n")
    print("=" * 100)

    print(question)

    print("=" * 100)

    plan = supervisor.plan(question)

    print("\nExecution Plan\n")

    pprint(plan.model_dump())