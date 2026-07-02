import asyncio

from copilot.skills.report import ReportSkill


async def main():

    skill = ReportSkill()

    result = await skill.execute(

        task="save_report",

        arguments={

            "report_type": "Parent Report"

        },

        context={

            "patient": {

                "id": 64

            },

            "report": "This is a sample report."

        }

    )

    print(result)


asyncio.run(main())