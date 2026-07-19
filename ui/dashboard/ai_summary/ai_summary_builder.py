import json

from ui.dashboard.ai_summary.ai_summary_prompt import (
    SYSTEM_PROMPT,
)


class AISummaryBuilder:

    @staticmethod
    def build(patient, evidence):

        payload = {

            "patient": {

                "name": patient["name"],

                "age": patient["age"],

                "diagnosis": patient["diagnosis"],

                "concerns": patient["concerns"],

            },

            "trajectory": evidence.trajectory,

            "goal_evolution": evidence.goal_evolution,

            "goal_persistence": evidence.goal_persistence,

            "focus_evolution": evidence.focus_evolution,

            "alerts": evidence.alerts,

        }

        return {

            "system": SYSTEM_PROMPT,

            "user": json.dumps(

                payload,

                indent=2,

                default=str,

            ),

        }