class EvolutionFormatter:

    @staticmethod
    def format(evolution: dict) -> str:

        report = "#### 🧬 Therapy Evolution\n\n"

        report += "##### 📈 Overall Summary\n\n"

        report += evolution.get(
            "summary",
            "Not available."
        )

        report += "\n\n"

        report += "##### 🛤️ Treatment Journey\n\n"

        report += evolution.get(
            "treatment_journey",
            "Not available."
        )

        report += "\n\n"

        report += "##### 🎯 Goal Progression\n\n"

        report += evolution.get(
            "goal_progression",
            "Not available."
        )

        report += "\n\n"

        report += "##### 🔄 Therapy Focus Shift\n\n"

        report += evolution.get(
            "therapy_focus_shift",
            "Not available."
        )

        report += "\n\n"

        report += "##### 🏠 Caregiver / Home Program Progression\n\n"

        report += evolution.get(
            "caregiver_progression",
            "Not available."
        )

        report += "\n\n"

        report += "##### 🩺 Clinical Reasoning\n\n"

        report += evolution.get(
            "clinical_reasoning",
            "Not available."
        )

        report += "\n\n"

        report += "##### ➡️ Recommended Next Phase\n\n"

        report += evolution.get(
            "next_recommendations",
            "Not available."
        )

        return report.strip()