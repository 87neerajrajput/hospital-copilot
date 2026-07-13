
from agents.comparison import comparison_agent, analyze_evolution
from langchain_core.messages import HumanMessage

class ComparisonSkill:

    async def execute(
        self,
        task: str,
        arguments: dict,
        context: dict,
    ):

        if task == "compare_plans":

            return await self.compare_plans(
                arguments,
                context,
            )
        
        elif task == "analyze_evolution":

            return await self.analyze_evolution(
                arguments,
                context,
            )

        raise ValueError(
            f"Unknown Comparison task: {task}"
        )

    async def compare_plans(
        self,
        arguments: dict,
        context: dict,
    ):

        selected_plans = context.get("selected_plans")

        if selected_plans is None:

            raise ValueError(
                "Selected therapy plans not found."
            )

        if len(selected_plans) != 2:

            raise ValueError(
                "Exactly two therapy plans are required."
            )

        left_plan = selected_plans[0]

        right_plan = selected_plans[1]

        comparison = await comparison_agent(
            left_plan,
            right_plan,
        )

        from copilot.formatters.comparison_formatter import (
            ComparisonFormatter
        )

        formatted_report = ComparisonFormatter.format(
            comparison
        )

        return {

            "therapy_comparison": comparison,

            "comparison_report": formatted_report,

        }
    

    # ======================================================
    # ANALYZE EVOLUTION
    # ======================================================

    async def analyze_evolution(
        self,
        arguments: dict,
        context: dict,
    ):

        plans = context.get("therapy_plan_list", [])

        if len(plans) < 2:

            return {
                "therapy_evolution": {
                    "summary": (
                        "Only one therapy plan is available. "
                        "Evolution analysis requires multiple plans."
                    )
                }
            }

        # Keep chronological order

        plans = sorted(
            plans,
            key=lambda p: p["created_at"],
        )

        history = []

        for plan in plans:

            therapy = plan["therapy_plan"]

            history.append(

                {
                    "plan_id": plan["id"],
                    "created_at": str(plan["created_at"]),
                    "therapy_goals": therapy.get(
                        "therapy_goals",
                        [],
                    ),
                    "weekly_schedule": therapy.get(
                        "weekly_schedule",
                        [],
                    ),
                    "home_program": therapy.get(
                        "home_program",
                        [],
                    ),
                }

            )

        evolution = analyze_evolution(history)

        return {

            "therapy_evolution": evolution

        }