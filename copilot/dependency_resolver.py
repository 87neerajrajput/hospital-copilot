"""
dependency_resolver.py

Builds an executable task chain from the Skill Registry.

Responsibilities
----------------
- Resolve dependencies recursively
- Produce an ordered execution plan
- Detect circular dependencies
- Avoid duplicate tasks

No workflow templates.

No LLM.

No execution.

Pure dependency resolution.
"""

from copilot.registry_index import RegistryIndex


class DependencyResolver:

    def __init__(self):

        self.registry = RegistryIndex()

    # ---------------------------------------------------------

    def resolve(
        self,
        artifact: str,
        operation: str,
    ):

        available = set()

        resolved = []

        planned_tasks = set()

        visiting = set()

        self._resolve(

            artifact=artifact,

            operation=operation,

            available=available,

            resolved=resolved,

            planned_tasks=planned_tasks,

            visiting=visiting,

        )

        return resolved

    # ---------------------------------------------------------

    def _resolve(

        self,

        artifact,

        operation,

        available,

        resolved,

        planned_tasks,

        visiting,

    ):

        # Already available

        if artifact in available:

            return

        # Circular dependency detection

        if artifact in visiting:

            cycle = " -> ".join(

                list(visiting) + [artifact]

            )

            raise RuntimeError(

                f"Circular dependency detected: {cycle}"

            )

        visiting.add(artifact)

        # Find candidate producers

        candidates = self.registry.producers_of(

            artifact,

            operation,

        )

        if not candidates:

            raise RuntimeError(

                f"No producer found for '{artifact}' "

                f"with operation '{operation}'."

            )

        # -------------------------------------------------
        # Producer selection
        #
        # Current strategy:
        #
        # Use the first producer.
        #
        # Future:
        #
        # This is the ONLY place that should evolve
        # when introducing cost-based selection,
        # caching, AI selection, etc.
        # -------------------------------------------------

        producer = candidates[0]

        # Resolve requirements first

        for requirement in producer["definition"]["requires"]:

            self._resolve(

                artifact=requirement,

                operation="read",

                available=available,

                resolved=resolved,

                planned_tasks=planned_tasks,

                visiting=visiting,

            )

        # Add task only once

        task_name = producer["task"]

        if task_name not in planned_tasks:

            resolved.append(producer)

            planned_tasks.add(task_name)

        # Mark outputs as available

        available.update(

            producer["definition"]["produces"]

        )

        visiting.remove(artifact)