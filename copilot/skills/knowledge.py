"""
knowledge.py

Milestone 9.2

Knowledge Skill

Responsibilities
----------------
Execute knowledge-related business tasks.

Current Tasks
-------------
- search_information
"""
from hospital_mcp.hospital_client import mcp

class KnowledgeSkill:

    def __init__(self):

        self.mcp = mcp

    # ======================================================
    # EXECUTE
    # ======================================================

    async def execute(
        self,
        task: str,
        arguments: dict,
        context: dict,
    ):

        if task == "search_information":

            return await self.search_information(
                arguments,
                context,
            )

        raise ValueError(
            f"Unknown Knowledge task: {task}"
        )

    # ======================================================
    # SEARCH KNOWLEDGE
    # ======================================================

    async def search_information(
        self,
        arguments: dict,
        context: dict,
    ):

        query = arguments.get("query", "")

        print("\n========== KNOWLEDGE SKILL ==========")
        print("Query :", repr(query))
        print("Arguments :", arguments)
        print("=====================================\n")

        documents = await self.mcp.search_knowledge(
            query=query,
            k=3,
        )

        print("Retrieved docs:", len(documents))

        return {

            "knowledge": documents

        }