import asyncio
from pprint import pprint

from copilot.supervisor import ClinicalSupervisor
from copilot.executor import Executor


TEST_REQUESTS = [

    # "Find Aston Martin.",

    # "Show Aston Martin's latest therapy plan.",

    # "Generate a therapy plan for Aston Martin.",

    # "Review Aston Martin's therapy plan.",

     "Generate report for Aston Martin.",
 
]


async def main():

    supervisor = ClinicalSupervisor()

    executor = Executor()

    for request in TEST_REQUESTS:

        print("\n" + "=" * 100)

        print(request)

        print("=" * 100)

        # --------------------------------------------------
        # Planning
        # --------------------------------------------------

        plan = supervisor.plan(request)

        print("\nExecution Plan\n")

        pprint(plan.model_dump())

        # --------------------------------------------------
        # Execution
        # --------------------------------------------------

        state = await executor.execute(plan)

        print("\nReturned Execution State\n")

        print("Status :", state.status)
        print("Waiting:", state.waiting_for_approval)
        print("Pending:", state.pending_step)

        if state.waiting_for_approval:

            decision = input(
                "\nApprove? (approve/reject): "
            ).strip().lower()

            if decision not in (
                "approve",
                "approved",
                "reject",
                "rejected",
                "y",
                "yes",
                "n",
                "no",
            ):
                print("Invalid decision.")
                return

            state = await executor.resume(
                state=state,
                decision=decision,
            )

        print("\n========== AFTER RESUME ==========\n")

        print("Status :", state.status)

        print("Current Step :", state.current_step)

        print("Waiting :", state.waiting_for_approval)

        print("Plan ID :", state.context.get("plan_id"))

        print("\nContext\n")

        pprint(state.context)


if __name__ == "__main__":

    asyncio.run(main())