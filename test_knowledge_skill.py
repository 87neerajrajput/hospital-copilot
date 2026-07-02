import asyncio

from copilot.skills.knowledge import KnowledgeSkill


async def main():

    skill = KnowledgeSkill()

    result = await skill.execute(

        task="search_information",

        arguments={
            "query": "Activities for poor joint attention"
        },

        context={}

    )

    print(result)


asyncio.run(main())