class DashboardAnalyzer:

    @staticmethod
    def generate(plan):

        insights = []

        if not plan:
            return insights

        therapy = plan.get("therapy_plan", {})

        goals = therapy.get("therapy_goals", [])
        home_program = therapy.get("home_program", [])
        schedule = therapy.get("weekly_schedule", [])

        # -----------------------------
        # Therapy Goals
        # -----------------------------

        insights.append({
            "type": "success",
            "icon": "🎯",
            "title": "Therapy Goals",
            "message": f"{len(goals)} active therapy goals."
        })

        # -----------------------------
        # Home Program
        # -----------------------------

        insights.append({
            "type": "info",
            "icon": "🏠",
            "title": "Home Program",
            "message": f"{len(home_program)} home activities prescribed."
        })

        # -----------------------------
        # Weekly Plan
        # -----------------------------

        insights.append({
            "type": "warning",
            "icon": "📅",
            "title": "Treatment Schedule",
            "message": f"{len(schedule)} weeks planned."
        })

        return insights