import asyncio

from copilot.skills.therapy import TherapySkill


async def main():


    skill = TherapySkill()

    result = await skill.execute(

        task="load_patient_plans",

        arguments={

            "patient_id": 65,

        },

        context={},

    )

    print("\nResult\n")

    print(result)


if __name__ == "__main__":

    asyncio.run(main())