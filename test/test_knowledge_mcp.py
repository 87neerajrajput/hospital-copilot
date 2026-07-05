from hospital_mcp.hospital_client import HospitalMCPClient
import asyncio


async def main():

    client = HospitalMCPClient()

    docs = await client.search_knowledge(
        query="Unsafe swallowing,high choking risk,poor swallowing coordination",
        k=3,
    )

    print(docs)


asyncio.run(main())