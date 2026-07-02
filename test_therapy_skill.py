import asyncio

from copilot.skills.therapy import TherapySkill


async def main():

    skill = TherapySkill()

    result = await skill.execute(

        task="load_latest_plan",

        arguments={},

        context={

            "patient": {

                "id": 65

            }

        }

    )

    print(result)


asyncio.run(main())