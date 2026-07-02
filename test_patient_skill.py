import asyncio

from copilot.skills.patient import PatientSkill


async def main():

    skill = PatientSkill()

    result = await skill.execute(

        task="find_patient",

        arguments={

            "name": "Miller"

        },

        context={}

    )

    print(result)


asyncio.run(main())