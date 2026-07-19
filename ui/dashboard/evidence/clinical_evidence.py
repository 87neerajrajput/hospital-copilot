from dataclasses import dataclass, field


@dataclass
class ClinicalEvidence:

    goal_evolution: dict

    goal_persistence: list

    focus_evolution: list

    alerts: list

    therapy_journey: list

    trajectory: dict = field(default_factory=dict)

    ai_summary: str = ""