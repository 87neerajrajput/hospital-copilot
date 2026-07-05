"""
tests/test_plan_validator.py

Verify that PlanValidator accepts valid execution plans
and rejects invalid ones.
"""

from pprint import pprint

from copilot.workflow_builder import WorkflowBuilder
from copilot.plan_validator import (
    PlanValidator,
    PlanValidationError,
)
from copilot.execution_plan import (
    ExecutionPlan,
    PlanStep,
)

builder = WorkflowBuilder()

validator = PlanValidator()

# ==========================================================
# VALID PLANS
# ==========================================================

valid_examples = [

    (
        "patient_search",
        "Find Aston Martin.",
        {
            "patient_name": "Aston Martin"
        },
    ),

    (
        "therapy_lookup",
        "Show latest therapy plan.",
        {
            "patient_name": "Aston Martin"
        },
    ),

    (
        "therapy_generation",
        "Generate therapy plan.",
        {
            "patient_name": "Aston Martin"
        },
    ),

    (
        "report_generation",
        "Generate parent report.",
        {
            "patient_name": "Aston Martin",
            "report_type": "parent",
        },
    ),

    (
        "qa",
        "Validate therapy plan.",
        {
            "patient_name": "Aston Martin"
        },
    ),

]

print("\n")
print("=" * 90)
print("VALID PLANS")
print("=" * 90)

for intent, goal, entities in valid_examples:

    print(f"\nIntent : {intent}")

    plan = builder.build(

        intent=intent,

        goal=goal,

        entities=entities,

    )

    pprint(plan.model_dump())

    try:

        validator.validate(plan)

        print("✅ VALID\n")

    except PlanValidationError as e:

        print("❌ FAILED")

        print(e)

# ==========================================================
# INVALID PLAN
# ==========================================================

print("\n")
print("=" * 90)
print("INVALID PLAN")
print("=" * 90)

bad_plan = ExecutionPlan(

    goal="Broken Plan",

    intent="report_generation",

    steps=[

        PlanStep(

            skill="report",

            task="generate_report",

            arguments={},

        )

    ],

)

pprint(bad_plan.model_dump())

try:

    validator.validate(bad_plan)

    print("Unexpected success!")

except PlanValidationError as e:

    print("\nExpected Validation Error")

    print(e)