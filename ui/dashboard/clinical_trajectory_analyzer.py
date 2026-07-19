from ui.dashboard.evidence.clinical_evidence import (
    ClinicalEvidence,
)


class ClinicalTrajectoryAnalyzer:

    @staticmethod
    def generate(
        evidence: ClinicalEvidence,
    ):

        positive = 0
        negative = 0

        reasons = []

        # -----------------------------------------
        # Goal Evolution
        # -----------------------------------------

        evolution = evidence.goal_evolution

        if evolution:

            if evolution["added"]:

                positive += 1

                reasons.append(
                    "Therapy goals continue to evolve."
                )

            if (
                not evolution["added"]
                and
                not evolution["removed"]
            ):

                negative += 1

                reasons.append(
                    "Therapy goals have not changed."
                )

        # -----------------------------------------
        # Goal Persistence
        # -----------------------------------------

        persistent = [

            goal

            for goal in evidence.goal_persistence

            if goal["percent"] >= 75

        ]

        if persistent:

            negative += 1

            reasons.append(

                f"{len(persistent)} goals have persisted across most therapy plans."

            )

        # -----------------------------------------
        # Focus Evolution
        # -----------------------------------------

        if len(evidence.focus_evolution) >= 4:

            positive += 1

            reasons.append(

                "Therapy has addressed multiple functional domains."

            )

        # -----------------------------------------
        # Alerts
        # -----------------------------------------

        high_alerts = [

            a

            for a in evidence.alerts

            if a["type"] == "error"

        ]

        if high_alerts:

            negative += 1

            reasons.append(

                "Critical clinical alerts are present."

            )

        # -----------------------------------------
        # Classification
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