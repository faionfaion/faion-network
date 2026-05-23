#!/usr/bin/env python3
"""validate-outcomes.py — fail roadmap YAML with missing fields or < 2 candidate solutions.

Usage: python validate-outcomes.py roadmap.yaml
Exit 0 = all outcome rows are valid.
Exit 1 = violations found (list printed to stdout).

Expected YAML structure:
  outcomes:
    - id: "row-id"
      problem: "..."
      outcome_metric: "..."
      baseline: 0.18
      target: 0.12
      horizon: "Q2 2026"
      candidate_solutions: ["option 1", "option 2"]
      kill_criterion: "..."
"""
import sys

REQUIRED_FIELDS = {
    "problem",
    "outcome_metric",
    "baseline",
    "target",
    "horizon",
    "candidate_solutions",
    "kill_criterion",
}

VAGUE_VERBS = {"improve", "enhance", "optimize", "increase", "decrease", "better"}


def lint(path: str) -> list[str]:
    try:
        import yaml
    except ImportError:
        return ["ERROR: PyYAML not installed. Run: pip install pyyaml"]

    with open(path) as f:
        doc = yaml.safe_load(f)

    errors: list[str] = []

    for row in doc.get("outcomes", []):
        row_id = row.get("id", "?")

        missing = REQUIRED_FIELDS - set(row.keys())
        if missing:
            errors.append(f"{row_id}: missing fields: {sorted(missing)}")

        solutions = row.get("candidate_solutions", [])
        if isinstance(solutions, list) and len(solutions) < 2:
            errors.append(
                f"{row_id}: needs at least 2 candidate_solutions "
                f"(found {len(solutions)})"
            )

        metric = str(row.get("outcome_metric", "")).lower().split()[0]
        if metric in VAGUE_VERBS:
            errors.append(
                f"{row_id}: vague outcome_metric starts with '{metric}' — "
                "add a specific measurable KPI"
            )

        baseline = row.get("baseline")
        if isinstance(baseline, str) and not baseline.startswith("TBI"):
            errors.append(
                f"{row_id}: baseline is a string but not marked as TBI. "
                "Use a number or 'TBI: owner=X'"
            )

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: validate-outcomes.py <roadmap.yaml>")
        sys.exit(1)

    errors = lint(sys.argv[1])
    for e in errors:
        print(e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
