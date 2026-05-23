#!/usr/bin/env python3
"""moscow-lint.py — enforce MoSCoW invariants in a requirements YAML file.

Checks:
  - At least one MUST requirement exists
  - Every MUST has acceptance_criteria
  - No requirement is both MUST and Wont
  - MoSCoW cap: MUST count <= 60% of total (configurable)

Usage: python moscow-lint.py requirements.yaml [--must-cap 0.6]
Exit 1 if violations found, 0 if clean.
"""
import sys
import yaml


MUST_CAP = 0.6  # max fraction of requirements that can be MUST


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "requirements.yaml"
    cap = float(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] == "--must-cap" else MUST_CAP

    spec = yaml.safe_load(open(path))
    errs = []

    musts = [r for r in spec if r.get("priority", "").lower() == "must"]
    if not musts:
        errs.append("No MUST requirements — scope is undefined")

    must_ratio = len(musts) / len(spec) if spec else 0
    if must_ratio > cap:
        errs.append(
            f"MUST count {len(musts)}/{len(spec)} ({must_ratio:.0%}) exceeds cap {cap:.0%}; "
            f"force prioritization trade-offs"
        )

    for r in spec:
        req_id = r.get("id", "?")
        priority = r.get("priority", "").lower()

        if priority == "must" and not r.get("acceptance_criteria", "").strip():
            errs.append(f"{req_id}: MUST requirement missing acceptance_criteria")

        if priority == "must" and r.get("status", "").lower() == "wont":
            errs.append(f"{req_id}: MUST requirement has status 'Wont' — project will fail")

    if errs:
        for e in errs:
            print(f"[FAIL] {e}")
        sys.exit(1)

    print(f"OK: {len(spec)} requirements pass MoSCoW invariants "
          f"({len(musts)} MUST = {must_ratio:.0%})")


if __name__ == "__main__":
    main()
