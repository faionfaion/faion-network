#!/usr/bin/env python3
# purpose: WBS YAML helper validator (100% rule + 8-80h + overhead)
# consumes: wbs.yaml tree
# produces: validation report; exit 0 valid / 1 fail
# depends-on: content/01-core-rules.xml#hundred-percent-rule, eight-eighty-sizing
# token-budget-impact: ~250 tokens
"""Validate wbs.yaml: 100% rule (weight_pct children sum) + 8-80h leaf rule.

Input YAML structure:
  items:
    - id: "1"
      name: "Project Management"
      weight_pct: 15
      children:
        - id: "1.1"
          name: "Planning Documentation"
          effort_hours: 20
"""
import sys
import yaml

REQUIRED_PACKAGES = {
    "project management", "qa", "quality", "deployment",
    "documentation", "training", "transition",
}
ERR = []


def walk(node):
    children = node.get("children", [])
    if children:
        weights = [c.get("weight_pct", 0) for c in children]
        total = sum(weights)
        if abs(total - 100) > 0.5:
            ERR.append(
                f"{node['id']} '{node['name']}': children sum to {total}%, expected 100"
            )
        for child in children:
            walk(child)
    else:
        hours = node.get("effort_hours")
        if hours is None:
            ERR.append(f"{node['id']} '{node['name']}': leaf missing effort_hours")
        elif not (8 <= hours <= 80):
            ERR.append(
                f"{node['id']} '{node['name']}': effort {hours}h violates 8-80 rule"
            )


def check_overhead(nodes):
    all_names = set()

    def collect(n):
        all_names.add(n["name"].lower())
        for c in n.get("children", []):
            collect(c)

    for n in nodes:
        collect(n)

    for pkg in REQUIRED_PACKAGES:
        if not any(pkg in name for name in all_names):
            ERR.append(f"WBS: missing required overhead package '{pkg}'")


def main(path):
    doc = yaml.safe_load(open(path))
    items = doc.get("items", doc) if isinstance(doc, dict) else doc
    for top in items:
        walk(top)
    check_overhead(items)
    if ERR:
        print("\n".join(f"[FAIL] {e}" for e in ERR))
        sys.exit(1)
    print("WBS valid")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: wbs-validate.py <wbs.yaml>")
        sys.exit(2)
    main(sys.argv[1])
