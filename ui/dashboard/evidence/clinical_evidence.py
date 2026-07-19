from dataclasses import dataclass


@dataclass
class ClinicalEvidence:

    goal_evolution: dict

    goal_persistence: list

    focus_evolution: list

    alerts: list

    therapy_journey: list