class GoalEvolutionAnalyzer:

    @staticmethod
    def generate(previous_plan, latest_plan):

        previous_goals = set()

        latest_goals = set()

        if previous_plan:

            previous_goals = set(
                previous_plan
                .get("therapy_plan", {})
                .get("therapy_goals", [])
            )

        if latest_plan:

            latest_goals = set(
                latest_plan
                .get("therapy_plan", {})
                .get("therapy_goals", [])
            )

        return {

            "added": sorted(
                latest_goals - previous_goals
            ),

            "removed": sorted(
                previous_goals - latest_goals
            ),

            "continued": sorted(
                previous_goals & latest_goals
            ),

        }