import asyncio

from copilot.copilot import run_copilot


async def main():

    state = await run_copilot(
        "Show Aston Martin's therapy history."
    )

    print(state.status)

    print(state.context)


if __name__ == "__main__":

    asyncio.run(main())