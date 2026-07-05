"""
tests/test_registry.py

Verify that the Skill Registry has been indexed correctly.
"""

from pprint import pprint

from copilot.registry_index import RegistryIndex

registry = RegistryIndex()

print("\n" + "=" * 80)
print("REGISTERED TASKS")
print("=" * 80)

for (skill, task), info in sorted(registry.tasks.items()):

    print(f"\n{skill}.{task}")

    pprint(info["definition"])

print("\n" + "=" * 80)
print("TOTAL TASKS :", len(registry.tasks))
print("=" * 80)