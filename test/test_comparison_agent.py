import asyncio

from hospital_mcp.hospital_client import HospitalMCPClient
from agents.comparison import comparison_agent


async def main():

    mcp = HospitalMCPClient()

    left = await mcp.get_therapy_plan(82)
    right = await mcp.get_therapy_plan(87)

    left_plan = {
        "plan_id": 82,
        "created_at": "2026-07-05",
        "therapy_plan": left["therapy_plan"]
    }

    right_plan = {
        "plan_id": 87,
        "created_at": "2026-07-08",
        "therapy_plan": right["therapy_plan"]
    }

    result = await comparison_agent(
        left_plan,
        right_plan
    )

    from pprint import pprint
    pprint(result)


asyncio.run(main())