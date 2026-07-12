
from datetime import datetime

class CopilotFormatter:

    @staticmethod
    def patient(patient: dict) -> str:

        concerns = patient.get("concerns", [])

        if concerns:
            concerns_text = "\n".join(
                f"- {concern}" for concern in concerns
            )
        else:
            concerns_text = "Not Available"

        return f"""#### 👤 Patient Found

**Name:** {patient["name"]}

**Age:** {patient["age"]} years

**Diagnosis:** {patient["diagnosis"]}

**Primary Concerns:**

{concerns_text}
"""

    @staticmethod
    def no_patient() -> str:

        return (
            "❌ No matching patient was found."
        )
    


    @staticmethod
    def therapy_history(plans: list) -> str:

        if not plans:

            return (
                "❌ No therapy plans were found for this patient."
            )

        report = "#### 📚 Therapy History\n\n"

        report += (
            f"**Total Therapy Plans:** {len(plans)}\n\n"
        )

        report += "**Available Plans**\n\n"

        for plan in plans:

            created = plan["created_at"]

            if isinstance(created, datetime):

                created = created.strftime(
                    "%d %b %Y, %I:%M %p"
                )

            report += (
                f"- **Plan #{plan['id']}**"
                f" ({created})\n"
            )

        return report
    


    @staticmethod
    def therapy_saved() -> str:

        return """
#### ✅ Therapy Plan Saved

The therapy plan has been approved and saved successfully.

You can now:

- View the latest therapy plan
- Compare it with a previous plan
- Generate a parent report
- Generate a clinical report
"""

    @staticmethod
    def therapy_rejected() -> str:

        return """
#### ❌ Therapy Plan Rejected

The generated therapy plan was rejected.

No changes have been saved.
"""

    @staticmethod
    def comparison_ready() -> str:

        return """
#### ✅ Therapy Comparison Completed

The clinical comparison has been completed successfully.
"""

    @staticmethod
    def therapy_loaded() -> str:

        return """
#### ✅ Therapy Plan Loaded
"""