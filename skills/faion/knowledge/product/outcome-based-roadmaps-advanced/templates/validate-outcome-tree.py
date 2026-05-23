#!/usr/bin/env python3
"""validate-outcome-tree.py — fail on outcomes missing leading indicators, evidence, or experiments.

Input:  outcome tree YAML with structure:
  goal: "str"
  outcomes:
    - name: "str"
      leading_indicator: "str"
      confidence: low|medium|high
      evidence: "str"        # required when confidence=high
      experiments:           # list of 2-3 candidate experiments
        - "str"
Output: violation lines, exits 1 if any found.
"""
import sys
import yaml


def check_node(node: dict, path: str = "") -> list[str]:
    errs: list[str] = []
    outcomes = node.get("outcomes", [])

    if len(outcomes) > 4:
        errs.append(
            f"{path}: {len(outcomes)} outcomes exceed the hard cap of 4 — "
            "collapse to focus on fewer goals"
        )

    for outcome in outcomes:
        name = outcome.get("name", "?")
        p = f"{path}/{name}" if path else name

        if not outcome.get("leading_indicator"):
            errs.append(f"{p}: missing leading_indicator")

        confidence = outcome.get("confidence", "")
        if confidence not in ("low", "medium", "high"):
            errs.append(f"{p}: confidence must be low|medium|high, got '{confidence}'")

        if confidence == "high" and not outcome.get("evidence"):
            errs.append(
                f"{p}: confidence=high requires evidence field "
                "(cite query/dashboard URL or mark 'TO BE INSTRUMENTED')"
            )

        experiments = outcome.get("experiments", [])
        if len(experiments) < 2:
            errs.append(
                f"{p}: must list 2-3 candidate experiments, found {len(experiments)}"
            )

        # recurse into nested outcomes
        if "outcomes" in outcome:
            errs.extend(check_node(outcome, path=p))

    return errs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate-outcome-tree.py <outcome-tree.yaml>")
        sys.exit(2)

    with open(sys.argv[1]) as f:
        tree = yaml.safe_load(f)

    errors = check_node(tree)
    for e in errors:
        print(e)
    sys.exit(1 if errors else 0)
