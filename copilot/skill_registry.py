"""
skill_registry.py

Single source of truth for all business skills
available to the Clinical Supervisor.
"""

SKILLS = {

    "knowledge": {

        "description": "Clinical knowledge retrieval",

        "tasks": {

            "search_information":
                "Search clinical knowledge base"
        }

    },

    "patient": {

        "description": "Patient management",

        "tasks": {

            "find_patient":
                "Search patient",

            "load_patient":
                "Load patient details",

            "create_patient":
                "Create new patient",

            "update_patient":
                "Update patient information"

        }

    },

    "therapy": {

        "description": "Therapy planning",

        "tasks": {

            "generate_therapy_plan":
                "Generate therapy plan",

            "load_latest_plan":
                "Load latest therapy plan",

            "save_plan":
                "Save therapy plan"

        }

    },

    "report": {

        "description": "Clinical report generation",

        "tasks": {

            "generate_report":
                "Generate report",

            "save_report":
                "Save report"

        }

    }

}