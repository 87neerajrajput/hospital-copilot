"""
tests/test_workflow_builder.py

Verify that WorkflowBuilder correctly converts a
WorkflowRequest into an executable ExecutionPlan.
"""

from pprint import pprint

from copilot.workflow_builder import WorkflowBuilder

builder = WorkflowBuilder()

examples = [

    (
        "patient_search",
        "Find Aston Martin.",
        {
            "patient_name": "Aston Martin"
        },
    ),

    (
        "therapy_lookup",
        "Show Aston Martin's latest therapy plan.",
        {
            "patient_name": "Aston Martin"
        },
    ),

    (
        "therapy_generation",
        "Generate therapy plan for Aston Martin.",
        {
            "patient_name": "Aston Martin"
        },
    ),

    (
        "report_generation",
        "Generate parent report for Aston Martin.",
        {
            "patient_name": "Aston Martin",
            "report_type": "parent",
        },
    ),

    (
        "qa",
        "Validate Aston Martin's therapy plan.",
        {
            "patient_name": "Aston Martin"
        },
    ),

    (
        "knowledge_search",
        "What is sensory integration?",
        {},
    ),

]

for intent, goal, entities in examples:

    print("\n" + "=" * 90)

    print("Intent :", intent)

    print("Goal   :", goal)

    print("Entities")

    pprint(entities)

    print("=" * 90)

    plan = builder.build(

        intent=intent,

        goal=goal,

        entities=entities,

    )

    print("\nExecution Plan\n")

    for index, step in enumerate(plan.steps, start=1):

        print(

            f"{index}. "

            f"{step.skill}.{step.task}"

        )

        print(

            f"   arguments : {step.arguments}"

        )

    print("\nModel Dump\n")

    pprint(plan.model_dump())