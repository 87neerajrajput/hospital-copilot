from datetime import datetime

from ui.dashboard.goal_evolution_analyzer import (
    GoalEvolutionAnalyzer,
)


class ClinicalAlertsAnalyzer:

    @staticmethod
    def generate(plans, latest_plan, previous_plan):

        alerts = []

        # ---------------------------------------
        # No Therapy Plan
        # ---------------------------------------

        if not plans:

            alerts.append({

                "type": "error",

                "title": "No Therapy Plan",

                "message": "No therapy plan has been generated.",

            })

            return alerts

        # ---------------------------------------
        # Therapy Review Due
        # ---------------------------------------

        latest_date = plans[0]["created_at"]

        days = (datetime.now() - latest_date).days

        if days > 30:

            alerts.append({

                "type": "warning",

                "title": "Therapy Review Due",

                "message": f"Last therapy plan was created {days} days ago.",

            })

        # ---------------------------------------
        # Long Duration Case
        # ---------------------------------------

        first_date = plans[-1]["created_at"]

        therapy_weeks = (latest_date - first_date).days / 7

        if therapy_weeks > 16:

            alerts.append({

                "type": "info",

                "title": "Long-term Therapy",

                "message": f"Patient has been in therapy for {round(therapy_weeks)} weeks.",

            })

        # ---------------------------------------
        # Goal Changes
        # ---------------------------------------

        if previous_plan:

            evolution = GoalEvolutionAnalyzer.generate(
                previous_plan,
                latest_plan,
            )

            if (
                len(evolution["added"]) == 0
                and
                len(evolution["removed"]) == 0
            ):

                alerts.append({

                    "type": "warning",

                    "title": "Goals Unchanged",

                    "message": "Therapy goals are unchanged from the previous plan.",

                })

        # ---------------------------------------
        # Home Program Size
        # ---------------------------------------

        if latest_plan:

            home_program = (
                latest_plan
                .get("therapy_plan", {})
                .get("home_program", [])
            )

            if len(home_program) > 8:

                alerts.append({

                    "type": "info",

                    "title": "Large Home Program",

                    "message": f"{len(home_program)} home activities prescribed. Monitor caregiver compliance.",

                })

        return alerts