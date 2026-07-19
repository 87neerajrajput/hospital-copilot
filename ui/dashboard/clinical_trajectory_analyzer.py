from ui.dashboard.goal_evolution_analyzer import GoalEvolutionAnalyzer
from ui.dashboard.goal_persistence_analyzer import GoalPersistenceAnalyzer
from ui.dashboard.focus_area_evolution_analyzer import FocusAreaEvolutionAnalyzer


class ClinicalTrajectoryAnalyzer:

    @staticmethod
    def generate(plans, latest_plan, previous_plan):

        reasons = []

        positive = 0
        negative = 0

        # -----------------------------------------
        # Goal Evolution
        # -----------------------------------------

        if previous_plan:

            evolution = GoalEvolutionAnalyzer.generate(
                previous_plan,
                latest_plan,
            )

            if evolution["added"]:

                positive += 1

                reasons.append(
                    "Therapy goals continue to evolve."
                )

            if (
                len(evolution["added"]) == 0
                and
                len(evolution["removed"]) == 0
            ):

                negative += 1

                reasons.append(
                    "Therapy goals have not changed."
                )

        # -----------------------------------------
        # Goal Persistence
        # -----------------------------------------

        persistence = GoalPersistenceAnalyzer.generate(
            plans
        )

        persistent = [

            goal

            for goal in persistence

            if goal["percent"] >= 75

        ]

        if persistent:

            negative += 1

            reasons.append(
                f"{len(persistent)} goals have persisted across most therapy plans."
            )

        # -----------------------------------------
        # Focus Area Diversity
        # -----------------------------------------

        focus = FocusAreaEvolutionAnalyzer.generate(
            plans
        )

        if len(focus) >= 4:

            positive += 1

            reasons.append(
                "Therapy has addressed multiple functional domains."
            )

        # -----------------------------------------
        # Therapy Duration
        # -----------------------------------------

        if len(plans) >= 6:

            negative += 1

            reasons.append(
                "Long-term therapy suggests ongoing clinical needs."
            )

        # -----------------------------------------
        # Final Classification
        # -----------------------------------------

        score = positive - negative

        if score >= 2:

            status = "Improving"

            confidence = "High"

        elif score == 1:

            status = "Stable"

            confidence = "Medium"

        elif score == 0:

            status = "Plateauing"

            confidence = "Medium"

        else:

            status = "Needs Review"

            confidence = "High"

        return {

            "status": status,

            "confidence": confidence,

            "score": score,

            "reasons": reasons,

        }