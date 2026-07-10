"""
skill_registry.py

Single source of truth for all business skills
available to the Clinical Supervisor.
"""

SKILLS = {

    "knowledge": {

        "description": "Clinical knowledge retrieval",

        "tasks": {

            "search_information": {

                "purpose":
                    "Retrieve clinical knowledge and evidence required for therapy planning.",

                "operation": "read",

                "description":
                    "Retrieve relevant clinical knowledge to support therapy plan generation.",

                "requires": [],

                "produces": [
                    "knowledge"
                ],

                "requires_approval": False,

            }

        }

    },

    "patient": {

        "description": "Patient management",

        "tasks": {

            "find_patient": {

                "purpose":
                    "Locate an existing patient using name or search criteria. Returns the complete patient record.",

                "operation": "read",      

                "description":
                    "Locate an existing patient by name or other identifying information.",

                "requires": [],

                "produces": [
                    "patient"
                ],

                "requires_approval": False,

            },

            "load_patient": {

                "purpose":
                    "Reload a patient when only a patient ID already exists. Do not use immediately after find_patient.",

                "operation": "read",

                "description":
                    "Load additional patient information.",

                "requires": [
                    "patient"
                ],

                "produces": [
                    "patient"
                ],

                "requires_approval": False,

            },

            "create_patient": {

                "purpose":
                    "Create a new patient record when the patient does not already exist.",

                "operation": "create",

                "description":
                    "Create a patient.",

                "requires": [],

                "produces": [
                    "patient"
                ],

                "requires_approval": False,

            },

            "update_patient": {

                "purpose":
                    "Update an existing patient's demographic or clinical information.",

                "operation": "update",

                "description":
                    "Update patient information.",

                "requires": [
                    "patient"
                ],

                "produces": [
                    "patient"
                ],

                "requires_approval": False,

            }

        }

    },

    "therapy": {

        "description": "Therapy planning",

        "tasks": {

            "generate_therapy_plan": {

                "purpose":
                    "Create a brand-new therapy plan when one needs to be generated from assessment findings.",

                "operation": "create",

                "description":
                    "Generate a new therapy plan using the patient's assessment and clinical knowledge.",

                "requires": [
                    "patient",
                    "knowledge"
                ],

                "produces": [
                    "therapy_plan"
                ],

                "requires_approval": True,

            },

            "load_patient_plans": {

                "purpose":
                    "Retrieve all therapy plans belonging to a patient.",

                "operation": "read",

                "description":
                    "Retrieve the complete therapy plan history for a patient.",

                "requires": [
                    "patient"
                ],

                "produces": [
                    "therapy_plan_list"
                ],

                "requires_approval": False,

            },

            "load_latest_plan": {

                "purpose":
                    "Retrieve the patient's most recent saved therapy plan. Use when viewing an existing therapy plan.",

                "operation": "read",

                "description":
                    "Load the most recent therapy plan for a patient.",

                "requires": [
                    "therapy_plan_list"
                ],

                "produces": [
                    "therapy_plan"
                ],

                "requires_approval": False,

            },


            "load_selected_plans": {

                "purpose": (
                    "Load two therapy plans selected from a patient's therapy history."
                ),

                "operation": "read",

                "description": (
                    "Select two therapy plans (for example latest, previous, or specific plan IDs)."
                ),

                "requires": [
                    "therapy_plan_list",
                ],

                "produces": [
                    "selected_plans",
                ],

                "requires_approval": False,

            },


            "save_plan": {

                "purpose":
                    "Persist a newly generated therapy plan into the database.",

                "operation": "write",

                "description":
                    "Save an approved therapy plan to the patient's clinical record.",

                "requires": [
                    "therapy_plan"
                ],

                "produces": [
                    "saved_plan"
                ],

                "requires_approval": False,

            }

        }

    },


    "comparison": {

        "description": (
            "Clinical comparison of therapy plans."
        ),

        "tasks": {

            "compare_plans": {

                "purpose": (
                    "Compare two therapy plans and summarize the clinical differences."
                ),

                "operation": "compare",

                "description": (
                    "Generate a comparison between two therapy plans."
                ),

                "requires": [
                    "selected_plans",
                ],

                "produces": [
                    "therapy_comparison",
                    "comparison_report",
                ],

                "requires_approval": False,

            },

        },

    },


    "qa": {

        "description": "Therapy quality assurance",

        "tasks": {

            "validate_therapy_plan": {

                "purpose":
                    "Review a generated therapy plan for completeness, consistency, and clinical quality before approval.",

                "operation": "validate",

                "description":
                    "Perform an internal quality review of a newly generated therapy plan before approval.",

                "requires": [
                    "therapy_plan"
                ],

                "produces": [
                    "qa_result"
                ],

                "requires_approval": False,
            },

            "review_therapy_plan": {
                "purpose": "Review an existing therapy plan for clinical quality.",
                "operation": "read",
                "description": "Perform a clinical review of an existing therapy plan at the therapist's request.",
                "requires": [
                    "therapy_plan"
                ],
                "produces": [
                    "therapy_review"
                ],
                "requires_approval": False,
            }

        }

    },


    "approval": {

        "description": "Human approval workflow",

        "tasks": {

            "review_plan": {

                "purpose":
                    "Pause execution and request therapist approval before continuing the workflow.",

                "operation": "approve",

                "description":
                    "Request therapist approval before saving a newly generated therapy plan.",

                "requires": [
                    "therapy_plan"
                ],

                "produces": [
                    "approval_status"
                ],

                "requires_approval": False,

            }

        }

    },

    "report": {

        "description": "Clinical reporting",

        "tasks": {

            "generate_report": {

                "purpose":
                    "Generate clinical and parent reports from an approved therapy plan.",

                "operation": "create",

                "description":
                    "Generate parent reports, clinical reports, or both from an existing therapy plan.",

                "requires": [
                    "therapy_plan"
                ],

                "produces": [
                    "report"
                ],

                "requires_approval": False,

            },

            "save_report": {

                "purpose":
                    "Persist generated reports into the database.",

                "operation": "write",
                
                "description":
                    "Save generated reports to the patient's clinical record.",

                "requires": [
                    "report"
                ],

                "produces": [
                    "saved_report"
                ],

                "requires_approval": False,

            }

        }

    },

}