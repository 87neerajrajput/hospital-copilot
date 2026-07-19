from collections import Counter


class FocusAreaEvolutionAnalyzer:

    @staticmethod
    def generate(plans):

        counter = Counter()

        latest_seen = {}

        for plan in plans:

            schedule = (
                plan.get("therapy_plan", {})
                .get("weekly_schedule", [])
            )

            unique_focus = set()

            for week in schedule:

                area = week.get("focus_area")

                if area:

                    unique_focus.add(area)

            for area in unique_focus:

                counter[area] += 1

                latest_seen[area] = plan["created_at"]

        results = []

        # Percentage based on number of therapy plans
        total_plans = len(plans)

        for area, count in counter.items():

            percent = round(
                (count / total_plans) * 100
            ) if total_plans else 0

            results.append({

                "focus_area": area,

                "count": count,

                "percent": percent,

                "last_seen": latest_seen[area],

            })

        results.sort(
            key=lambda x: x["count"],
            reverse=True,
        )

        return results