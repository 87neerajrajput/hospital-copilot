from datetime import datetime


class TimelineFormatter:

    @staticmethod
    def format(plans):

        report = "#### 🕒 Therapy Timeline\n\n"

        report += (
            f"**Total Therapy Plans:** "
            f"{len(plans)}\n\n"
        )

        report += "---\n\n"

        for index, plan in enumerate(plans):

            created = plan["created_at"]

            if isinstance(created, datetime):

                created = created.strftime(
                    "%d %b %Y • %I:%M %p"
                )

            report += (
                f"##### 📋 Plan #{plan['id']}\n\n"

                f"**Created:** {created}\n\n"
            )

            if index == 0:

                report += (
                    "🟢 **Current Active Therapy Plan**\n\n"
                )

            elif index == 1:

                report += (
                    "🟡 Previous Therapy Plan\n\n"
                )

            report += "---\n\n"

        return report.strip()