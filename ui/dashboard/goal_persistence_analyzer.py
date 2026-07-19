from collections import Counter


class GoalPersistenceAnalyzer:

    @staticmethod
    def generate(plans):

        counter = Counter()

        latest_seen = {}

        total_plans = len(plans)

        for plan in plans:

            goals = (
                plan.get("therapy_plan", {})
                .get("therapy_goals", [])
            )

            # Count each goal only once per plan
            for goal in set(goals):

                counter[goal] += 1

                latest_seen[goal] = plan["created_at"]

        results = []

        for goal, count in counter.items():

            percent = round(
                (count / total_plans) * 100
            ) if total_plans else 0

            results.append({

                "goal": goal,

                "count": count,

                "percent": percent,

                "last_seen": latest_seen[goal],

            })

        results.sort(
            key=lambda x: x["count"],
            reverse=True,
        )

        return results