"""
comparison_formatter.py

Formats AI-generated therapy plan comparisons into a
therapist-friendly report.
"""


class ComparisonFormatter:

    @staticmethod
    def format(comparison: dict) -> str:

        report = "#### 🩺 Therapy Plan Comparison\n\n"

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        report += "#### 📋 Summary\n\n"

        report += comparison["summary"] + "\n\n"

        # ---------------------------------------------------------
        # Treatment Evolution
        # ---------------------------------------------------------

        report += "#### 🔄 Treatment Evolution\n\n"

        report += comparison["treatment_evolution"] + "\n\n"

        # ---------------------------------------------------------
        # Goals Added
        # ---------------------------------------------------------

        report += "#### ➕ Goals Added\n\n"

        if comparison.get("goals_added"):

            for goal in comparison["goals_added"]:

                report += f"- {goal}\n"

        else:

            report += "_None_\n"

        report += "\n"

        # ---------------------------------------------------------
        # Goals Removed
        # ---------------------------------------------------------

        report += "#### ➖ Goals Removed\n\n"

        if comparison.get("goals_removed"):

            for goal in comparison["goals_removed"]:

                report += f"- {goal}\n"

        else:

            report += "_None_\n"

        report += "\n"

        # ---------------------------------------------------------
        # Weekly Schedule Changes
        # ---------------------------------------------------------

        report += "#### 📅 Weekly Schedule Changes\n\n"

        report += comparison["weekly_schedule_changes"] + "\n\n"

        # ---------------------------------------------------------
        # Home Program Changes
        # ---------------------------------------------------------

        report += "#### 🏠 Home Program Changes\n\n"

        report += comparison["home_program_changes"] + "\n\n"

        # ---------------------------------------------------------
        # Clinical Progression
        # ---------------------------------------------------------

        report += "#### 📈 Clinical Progression\n\n"

        report += comparison["clinical_progression"]

        return report.strip()