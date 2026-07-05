"""
tests/test_dependency_resolver.py

Verify recursive dependency resolution.
"""

from copilot.dependency_resolver import DependencyResolver

resolver = DependencyResolver()

examples = [

    ("patient", "read"),

    ("therapy_plan", "read"),

    ("therapy_plan", "create"),

    ("report", "create"),

    ("qa_result", "validate"),

    ("knowledge", "read"),

]

for artifact, operation in examples:

    print("\n" + "=" * 90)

    print(f"Artifact  : {artifact}")

    print(f"Operation : {operation}")

    print("=" * 90)

    tasks = resolver.resolve(

        artifact=artifact,

        operation=operation,

    )

    print()

    for index, task in enumerate(tasks, start=1):

        print(

            f"{index}. "

            f"{task['skill']}."

            f"{task['task']}"

        )