import asyncio
from pprint import pprint

from copilot.supervisor import ClinicalSupervisor
from copilot.executor import Executor


TEST_REQUESTS = [

    # "Find Aston Martin.",

    # "Show Aston Martin's latest therapy plan.",

    # "Generate a therapy plan for Aston Martin.",

    # "Generate a parent report for Aston Martin.",

    #"Validate Aston Martin's therapy plan.",

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

        context = await executor.execute(plan)

        print("\nReturned Context\n")

        pprint(context)


if __name__ == "__main__":

    asyncio.run(main())