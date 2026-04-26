#!/usr/bin/env python3
"""Validate wbs.yaml: 100% rule (weight_pct children sum) + 8-80h leaf effort rule.

Input YAML structure:
  items:
    - id: "1"
      name: "Project Management"
      weight_pct: 15
      children:
        - id: "1.1"
          name: "Planning Documentation"
          effort_hours: 20

Usage: wbs-validate.py <wbs.yaml>
Exit 0 = valid. Exit 1 = failures found.
"""
import sys
import yaml

REQUIRED_PACKAGES = {
    "project management", "qa", "quality", "testing",
    "deployment", "documentation", "training", "transition",
}
ERR: list[str] = []


def walk(node: dict) -> None:
    children = node.get("children", [])
    if children:
        weights = [c.get("weight_pct", 0) for c in children]
        total = sum(weights)
        if abs(total - 100) > 0.5:
            ERR.append(
                f"{node['id']} '{node['name']}': children sum to {total:.1f}%, expected 100"
            )
        for child in children:
            walk(child)
    else:
        hours = node.get("effort_hours")
        if hours is None:
            ERR.append(f"{node['id']} '{node['name']}': leaf missing effort_hours")
        elif not (8 <= float(hours) <= 80):
            ERR.append(
                f"{node['id']} '{node['name']}': effort {hours}h violates 8-80 rule"
            )
        deliverable = node.get("deliverable") or node.get("acceptance_criteria")
        if not deliverable:
            ERR.append(f"{node['id']} '{node['name']}': leaf missing deliverable or acceptance_criteria")


def collect_names(node: dict, names: set) -> None:
    names.add(node["name"].lower())
    for child in node.get("children", []):
        collect_names(child, names)


def check_overhead(items: list) -> None:
    all_names: set[str] = set()
    for item in items:
        collect_names(item, all_names)
    for pkg in REQUIRED_PACKAGES:
        if not any(pkg in name for name in all_names):
            ERR.append(f"WBS: missing required overhead package '{pkg}'")


def main(path: str) -> None:
    doc = yaml.safe_load(open(path))
    items = doc.get("items", doc) if isinstance(doc, dict) else doc
    for top in items:
        walk(top)
    check_overhead(items)
    if ERR:
        for e in ERR:
            print(f"[FAIL] {e}")
        sys.exit(1)
    print("WBS valid")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: wbs-validate.py <wbs.yaml>")
        sys.exit(2)
    main(sys.argv[1])
