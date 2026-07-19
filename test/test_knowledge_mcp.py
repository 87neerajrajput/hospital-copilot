from hospital_mcp.hospital_client import mcp
import asyncio


async def main():

    client = mcp

    docs = await client.search_knowledge(
        query="Unsafe swallowing,high choking risk,poor swallowing coordination",
        k=3,
    )

    print(docs)


asyncio.run(main())