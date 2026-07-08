"""
registry_index.py

Indexes the Skill Registry.

The Registry Index answers one question only:

    "Who can produce artifact X?"

It performs no planning or decision making.
"""

from collections import defaultdict

from copilot.skill_registry import SKILLS

import inspect
import copilot.skill_registry as sr


class RegistryIndex:

    def __init__(self):

        self.by_output = defaultdict(list)

        self.tasks = {}

        self._build_indexes()

    # ---------------------------------------------------------

    def _build_indexes(self):

        for skill_name, skill in SKILLS.items():

            for task_name, definition in skill["tasks"].items():

                task_info = {

                    "skill": skill_name,

                    "task": task_name,

                    "definition": definition,

                }

                self.tasks[(skill_name, task_name)] = task_info

                for artifact in definition["produces"]:

                    self.by_output[artifact].append(task_info)

    # ---------------------------------------------------------

    def producers_of(

        self,

        artifact: str,

        operation: str,

    ):

        return [

            task

            for task in self.by_output.get(

                artifact,

                []

            )

            if task["definition"]["operation"] == operation

        ]
    

    # ---------------------------------------------------------
    # GET TASK
    # ---------------------------------------------------------

    def get_task(
        self,
        skill: str,
        task: str,
    ):
        """
        Return the task definition for a given
        (skill, task) pair.
        """

        return self.tasks.get(

            (skill, task)

        )

    # ---------------------------------------------------------
    # TASK EXISTS
    # ---------------------------------------------------------

    def task_exists(
        self,
        skill: str,
        task: str,
    ) -> bool:

        return (

            (skill, task) in self.tasks

        )
    

    # ---------------------------------------------------------
    # HUMAR APPROVAL
    # ---------------------------------------------------------

    def requires_approval(
        self,
        skill: str,
        task: str,
    ) -> bool:

        task_info = self.get_task(
            skill,
            task,
        )

        if not task_info:

            return False

        return task_info["definition"].get(
            "requires_approval",
            False,
        )