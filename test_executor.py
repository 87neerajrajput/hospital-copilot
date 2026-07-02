import asyncio

from copilot.supervisor import ClinicalSupervisor
from copilot.executor import Executor


async def main():

    supervisor = ClinicalSupervisor()

    executor = Executor()

    plan = supervisor.plan(

        "Find Miller and show his latest therapy plan."

    )

    await executor.execute(plan)


asyncio.run(main())