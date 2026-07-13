"""
intent_registry.py

Single source of truth for therapist intents.

Each intent defines:

1. Description
   Human-readable explanation of the intent.
   Used by the Supervisor prompt.

2. Artifact
   The business artifact the therapist ultimately wants.

3. Operation
   The type of business operation required.

   read
       Retrieve existing information.

   create
       Generate new information.

   update
       Modify existing information.

   validate
       Review generated information.

   write
       Persist generated information.

4. Allowed Skills
   Skills that the Planner / Supervisor may consider
   while understanding the therapist request.

WorkflowBuilder uses:

    artifact
    operation

DependencyResolver discovers the actual execution steps.
"""

INTENTS = {

    # =====================================================
    # Patient
    # =====================================================

    "patient_search": {

        "description": (
            "Find or retrieve an existing patient."
        ),

        "artifact": "patient",

        "operation": "read",

        "allowed_skills": [

            "patient",

        ],
    },

    "patient_update": {

        "description": (
            "Update an existing patient's information."
        ),

        "artifact": "patient",

        "operation": "update",

        "allowed_skills": [

            "patient",

        ],
    },

    # =====================================================
    # Therapy
    # =====================================================

    "therapy_lookup": {

        "description": (
           "Retrieve a single therapy plan for a patient."
        ),

        "artifact": "therapy_plan",

        "operation": "read",

        "allowed_skills": [

            "patient",
            "therapy",

        ],
    },

    "therapy_history": {

        "description": (
            "Retrieve the therapy history for an existing patient."
        ),

        "artifact": "therapy_plan_list",

        "operation": "read",

        "allowed_skills": [

            "patient",
            "therapy",

        ],
    },

    "therapy_generation": {

        "description": (
            "Generate a new therapy plan."
        ),

        "artifact": "therapy_plan",

        "operation": "create",

        "allowed_skills": [

            "patient",
            "knowledge",
            "therapy",

        ],
    },

    "therapy_comparison": {

        "description": (
            "Compare two existing therapy plans for a patient."
        ),

        "artifact": "therapy_comparison",

        "operation": "compare",

        "allowed_skills": [

            "patient",
            "therapy",
            "comparison",

        ],
    },


    "therapy_evolution": {

        "description": (
            "Summarize how a patient's therapy has evolved "
            "across multiple therapy plans over time."
        ),

        "artifact": "therapy_evolution",

        "operation": "read",

        "allowed_skills": [

            "patient",
            "therapy",
            "comparison",

        ],
    },


    # =====================================================
    # QA
    # =====================================================

    "qa": {

        "description": (
            "Review or validate a generated therapy plan."
        ),

        "artifact": "qa_result",

        "operation": "validate",

        "allowed_skills": [

            "therapy",
            "qa",

        ],
    },


    # =====================================================
    # THERAPY REVIEW FOR EXISTING PLANS
    # =====================================================

    "therapy_review": {

        "description": (
            "Review an existing therapy plan."
        ),

        "artifact": "therapy_review",

        "operation": "read",

        "allowed_skills": [

            "patient",
            "therapy",
            "qa",

        ],
    },

    # =====================================================
    # Reports
    # =====================================================

    "report_generation": {

        "description": (
            "Generate a clinical or parent report."
        ),

        "artifact": "report",

        "operation": "create",

        "allowed_skills": [

            "patient",
            "therapy",
            "report",

        ],
    },

    # =====================================================
    # Knowledge
    # =====================================================

    "knowledge_search": {

        "description": (
            "Retrieve clinical knowledge."
        ),

        "artifact": "knowledge",

        "operation": "read",

        "allowed_skills": [

            "knowledge",

        ],
    },
}