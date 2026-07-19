class TherapyJourneyAnalyzer:

    @staticmethod
    def generate(plans):

        journey = []

        previous_goals = set()

        # oldest → newest
        for plan in reversed(plans):

            therapy = plan.get("therapy_plan", {})

            goals = therapy.get(
                "therapy_goals",
                []
            )

            focus = []

            for week in therapy.get(
                "weekly_schedule",
                []
            ):

                area = week.get("focus_area")

                if area and area not in focus:

                    focus.append(area)

            current_goals = set(goals)

            added = sorted(
                current_goals - previous_goals
            )

            removed = sorted(
                previous_goals - current_goals
            )

            journey.append(

                {

                    "date": plan["created_at"],

                    "focus": focus,

                    "goal_count": len(goals),

                    "added": added,

                    "removed": removed,

                }

            )

            previous_goals = current_goals

        return journey