from datetime import datetime


class ClinicalSummaryAnalyzer:

    @staticmethod
    def generate(patient, plans, latest_plan):

        summary = {}

        # ----------------------------------
        # Therapy Duration
        # ----------------------------------

        if plans:

            first_plan = plans[-1]["created_at"]
            last_plan = plans[0]["created_at"]

            weeks = max(
                1,
                round((last_plan - first_plan).days / 7)
            )

        else:

            weeks = 0

        summary["therapy_duration"] = f"{weeks} weeks"

        # ----------------------------------
        # Number of Therapy Plans
        # ----------------------------------

        summary["therapy_plans"] = len(plans)

        # ----------------------------------
        # Latest Plan
        # ----------------------------------

        if plans:

            latest = plans[0]["created_at"]

            days = (datetime.now() - latest).days

            if days == 0:
                latest_text = "Today"

            elif days == 1:
                latest_text = "Yesterday"

            else:
                latest_text = f"{days} days ago"

        else:

            latest_text = "-"

        summary["latest_plan"] = latest_text

        # ----------------------------------
        # Primary Focus Areas
        # ----------------------------------

        focus_areas = []

        if latest_plan:

            schedule = latest_plan.get(
                "therapy_plan",
                {}
            ).get(
                "weekly_schedule",
                []
            )

            for week in schedule:

                area = week.get(
                    "focus_area"
                )

                if area and area not in focus_areas:

                    focus_areas.append(area)

        summary["focus_areas"] = focus_areas

        return summary