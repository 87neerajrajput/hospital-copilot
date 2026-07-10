"""
comparison_formatter.py

Formats AI-generated therapy plan comparisons into a
therapist-friendly report.
"""


class ComparisonFormatter:

    @staticmethod
    def format(comparison: dict) -> str:

        report = f"""
        ============================================================
        THERAPY PLAN COMPARISON
        ============================================================

        SUMMARY
        ------------------------------------------------------------

        {comparison["summary"]}


        TREATMENT EVOLUTION
        ------------------------------------------------------------

        {comparison["treatment_evolution"]}


        GOALS ADDED
        ------------------------------------------------------------
        """

        if comparison.get("goals_added"):

            for goal in comparison["goals_added"]:

                report += f"\n• {goal}"

        else:

            report += "\nNone"

        report += """



        GOALS REMOVED
        ------------------------------------------------------------
        """

        if comparison.get("goals_removed"):

            for goal in comparison["goals_removed"]:

                report += f"\n• {goal}"

        else:

            report += "\nNone"

        report += f"""



        WEEKLY SCHEDULE CHANGES
        ------------------------------------------------------------

        {comparison["weekly_schedule_changes"]}


        HOME PROGRAM CHANGES
        ------------------------------------------------------------

        {comparison["home_program_changes"]}


        CLINICAL PROGRESSION
        ------------------------------------------------------------

        {comparison["clinical_progression"]}

        """

        return report.strip()