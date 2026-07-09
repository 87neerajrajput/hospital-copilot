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

        print("\n========== PLAN COMPARISON ==========")

        print(selected_plans)

        return {
            "comparison": "placeholder"
        }