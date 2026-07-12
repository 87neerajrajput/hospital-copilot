class TherapyPlanFormatter:

    @staticmethod
    def format(plan: dict, review_mode=False) -> str:

        report = "#### 🧾 Therapy Plan\n"

        # =====================================================
        # Therapy Goals
        # =====================================================

        report += "#### 🎯 Therapy Goals\n"

        for goal in plan.get("therapy_goals", []):

            report += f"- {goal}\n"

        # =====================================================
        # Weekly Schedule
        # =====================================================

        report += "\n---\n"
        report += "#### 📅 Weekly Therapy Schedule\n"

        for week in plan.get("weekly_schedule", []):

            report += f"\n##### {week['week']}\n"

            report += (
                f"**Focus Area**"
                f": {week['focus_area']}\n"
            )

            report += "\n**Activities**:\n"

            for activity in week.get("activities", []):

                report += f"- {activity}\n"

            report += (
                f"\n**Expected Outcome**"
                f": {week['expected_outcome']}\n"
            )

        # =====================================================
        # Home Program
        # =====================================================

        report += "\n---\n"
        report += "#### 🏠 Home Program\n"

        for activity in plan.get("home_program", []):

            report += f"\n##### {activity['activity_name']}\n"

            report += (
                f"**Instructions**"
                f": {activity['instructions']}\n\n"
            )

            report += (
                f"**Recommended Frequency**"
                f": {activity['recommended_frequency']}\n"
            )

        # =====================================================
        # Review
        # =====================================================

        report += "\n---\n"

        if review_mode:

            report += "#### ✅ Review Required\n"

            report += (
                "Please review the therapy plan above before it is saved.\n\n"
                "**Type `Approve`** to save the therapy plan.\n"
                "**Type `Reject`** to discard it."
            )

        return report