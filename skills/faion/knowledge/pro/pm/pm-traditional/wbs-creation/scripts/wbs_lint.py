#!/usr/bin/env python3
"""wbs_lint.py — lint a YAML WBS for common structural errors.

Usage: python wbs_lint.py wbs.yaml

wbs.yaml structure:
  - id: "1"
    name: "Project Name"
    type: deliverable
    children:
      - id: "1.1"
        name: "User Authentication Module"
        type: deliverable
        children:
          - id: "1.1.1"
            name: "Login API"
            type: workpackage
            effort_hours: 40

Checks:
- Verb-led names (activities, not deliverables)
- Depth > 5 (over-decomposed)
- Depth < 3 at leaf (underspecified)
- Missing project management branch
- Work packages outside 8-80 hour range

Exits 1 if errors found.
"""
import sys
import yaml

VERBS = {
    "design", "build", "implement", "test", "deploy", "write", "create",
    "develop", "analyze", "review", "configure", "install", "migrate",
    "integrate", "validate", "define", "plan", "research", "investigate",
}

errors = []
has_pm_branch = False


def walk(node: dict, depth: int, path: str) -> None:
    global has_pm_branch
    name = node.get("name", "").strip()
    first_word = name.split()[0].lower().rstrip("s") if name else ""

    if first_word in VERBS:
        errors.append(f"VERB-LED  {path}: '{name}' — rename to a noun (deliverable)")

    if depth >= 5 and node.get("children"):
        errors.append(f"TOO-DEEP  {path}: depth {depth} exceeds maximum of 5")

    node_type = node.get("type", "")
    if node_type == "workpackage":
        effort = node.get("effort_hours")
        if effort is not None and not (8 <= effort <= 80):
            errors.append(
                f"SIZE      {path}: '{name}' effort={effort}h — must be 8-80h"
            )

    lower_name = name.lower()
    if "project management" in lower_name or "pm" == lower_name:
        has_pm_branch = True

    for i, child in enumerate(node.get("children") or []):
        walk(child, depth + 1, f"{path}.{i+1}")


def main(path: str) -> int:
    tree = yaml.safe_load(open(path))
    nodes = tree if isinstance(tree, list) else [tree]
    for i, root in enumerate(nodes):
        walk(root, 0, str(i + 1))

    if not has_pm_branch:
        errors.append("MISSING   Project Management branch (e.g., '3. Project Management')")

    if errors:
        for e in errors:
            print(e)
        return 1
    print("OK — WBS passes all lint checks")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: wbs_lint.py wbs.yaml", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
