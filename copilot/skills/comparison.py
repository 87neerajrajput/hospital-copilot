
from agents.comparison import comparison_agent

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