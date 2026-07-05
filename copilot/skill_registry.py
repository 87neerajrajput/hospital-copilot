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
                    "Search the clinical knowledge base.",

                "requires": [],

                "produces": [
                    "knowledge"
                ]

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
                    "Search patient.",

                "requires": [],

                "produces": [
                    "patient"
                ]

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
                ]

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
                ]

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
                ]

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
                    "Generate therapy plan.",

                "requires": [
                    "patient",
                    "knowledge"
                ],

                "produces": [
                    "therapy_plan"
                ]

            },

            "load_latest_plan": {

                "purpose":
                    "Retrieve the patient's most recent saved therapy plan. Use when viewing an existing therapy plan.",

                "operation": "read",

                "description":
                    "Load the latest therapy plan.",

                "requires": [
                    "patient"
                ],

                "produces": [
                    "therapy_plan"
                ]

            },

            "save_plan": {

                "purpose":
                    "Persist a newly generated therapy plan into the database.",

                "operation": "write",

                "description":
                    "Save therapy plan.",

                "requires": [
                    "therapy_plan"
                ],

                "produces": [
                    "saved_plan"
                ]

            }

        }

    },

    "qa": {

        "description": "Therapy quality assurance",

        "tasks": {

            "validate_therapy_plan": {

                "purpose":
                    "Review a generated therapy plan for completeness, consistency, and clinical quality before approval.",

                "operation": "validate",

                "description":
                    "Validate therapy plan.",

                "requires": [
                    "therapy_plan"
                ],

                "produces": [
                    "qa_result"
                ]
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
                    "Generate reports.",

                "requires": [
                    "therapy_plan"
                ],

                "produces": [
                    "report"
                ]

            },

            "save_report": {

                "purpose":
                    "Persist generated reports into the database.",

                "operation": "write",
                
                "description":
                    "Save reports.",

                "requires": [
                    "report"
                ],

                "produces": [
                    "saved_report"
                ]

            }

        }

    },

}