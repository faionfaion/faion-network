#!/usr/bin/env python3
"""spec_lint.py — validate spec JSON for structural completeness.

Input (stdin): spec JSON.
Schema: {
  "non_goals": [str],
  "goals": [{"name": str, "metric": str, "target": str}],
  "functional_requirements": [{"id": str, "text": str, "priority": "M"|"S"|"C"}],
  "acceptance_criteria": [{"feature_id": str, "scenarios": [...]}],
  "open_questions": [{"q": str, "owner": str, "status": str}]
}
Output (stdout): {"ok": bool, "errors": [str]}
Exit: 0 if ok, 1 if errors found.
"""
import json
import re
import sys


def main() -> None:
    spec = json.load(sys.stdin)
    errs: list[str] = []

    if not spec.get("non_goals"):
        errs.append("non_goals required and must be non-empty (min 3 items)")
    elif len(spec["non_goals"]) < 3:
        errs.append(f"non_goals has {len(spec['non_goals'])} items (min 3)")

    if not spec.get("goals"):
        errs.append("goals required")
    for g in spec.get("goals", []):
        if not g.get("metric") or not g.get("target"):
            errs.append(f"goal '{g.get('name')}' missing metric or target")

    frs = spec.get("functional_requirements", [])
    fr_ids = set()
    for fr in frs:
        if not re.match(r"^FR-\d+$", fr.get("id", "")):
            errs.append(f"bad FR id: {fr.get('id')} (expected FR-N)")
        if fr.get("priority") not in ("M", "S", "C"):
            errs.append(f"{fr.get('id')} missing M/S/C priority")
        fr_ids.add(fr.get("id"))

    acs_for = {ac["feature_id"] for ac in spec.get("acceptance_criteria", [])}
    for fr_id in fr_ids:
        if fr_id not in acs_for:
            errs.append(f"{fr_id} has no acceptance_criteria")

    oqs = spec.get("open_questions")
    if oqs is None:
        errs.append("open_questions field missing (use [] with a note if all knowns verified)")

    print(json.dumps({"ok": not errs, "errors": errs}, indent=2))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
