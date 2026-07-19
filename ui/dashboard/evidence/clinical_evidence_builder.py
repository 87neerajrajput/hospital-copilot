from ui.dashboard.goal_evolution_analyzer import (
    GoalEvolutionAnalyzer,
)

from ui.dashboard.goal_persistence_analyzer import (
    GoalPersistenceAnalyzer,
)

from ui.dashboard.focus_area_evolution_analyzer import (
    FocusAreaEvolutionAnalyzer,
)

from ui.dashboard.clinical_alerts_analyzer import (
    ClinicalAlertsAnalyzer,
)

from ui.dashboard.therapy_journey_analyzer import (
    TherapyJourneyAnalyzer,
)

from ui.dashboard.evidence.clinical_evidence import (
    ClinicalEvidence,
)


class ClinicalEvidenceBuilder:

    @staticmethod
    def build(

        plans,

        latest_plan,

        previous_plan,

    ):

        evidence = ClinicalEvidence(

            goal_evolution=GoalEvolutionAnalyzer.generate(

                previous_plan,

                latest_plan,

            ),

            goal_persistence=GoalPersistenceAnalyzer.generate(
                plans
            ),

            focus_evolution=FocusAreaEvolutionAnalyzer.generate(
                plans
            ),

            alerts=ClinicalAlertsAnalyzer.generate(

                plans,

                latest_plan,

                previous_plan,

            ),

            therapy_journey=TherapyJourneyAnalyzer.generate(
                plans
            ),

        )

        return evidence