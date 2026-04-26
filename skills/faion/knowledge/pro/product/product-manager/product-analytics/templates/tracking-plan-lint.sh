#!/usr/bin/env bash
# tracking-plan-lint.sh — enforce naming + required fields on a markdown Tracking Plan.
# Usage: tracking-plan-lint.sh path/to/tracking-plan.md
# Checks: snake_case, object_action shape, non-empty trigger, non-empty properties.
set -euo pipefail
file="${1:?usage: tracking-plan-lint.sh PLAN.md}"
python3 - "$file" <<'PY'
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
errs = []
# Match table rows with at least 3 pipe-separated cells
row_re = re.compile(r"^\|\s*([a-zA-Z0-9_\[\]]+)\s*\|([^|]+)\|([^|]+)\|", re.M)
seen = {}
for m in row_re.finditer(src):
    name, trigger, props = (s.strip() for s in m.groups())
    # Skip header and separator rows
    if name.lower() in ("event", "property", "metric", "---", "object_action"):
        continue
    if name.startswith("[") or name.startswith("-"):
        continue
    # Check snake_case
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        errs.append(f"{name}: not snake_case")
    # Check object_action shape (must have at least one underscore)
    if "_" not in name:
        errs.append(f"{name}: missing object_action shape (no underscore)")
    # Check non-empty trigger
    if not trigger or trigger.strip().startswith("TODO") or trigger.strip() == "—":
        errs.append(f"{name}: missing or TODO trigger")
    # Check non-empty properties
    if not props or props.strip().startswith("TODO") or props.strip() == "—":
        errs.append(f"{name}: missing or TODO properties")
    # Check for duplicates
    if name in seen:
        errs.append(f"{name}: duplicate event (first seen in: '{seen[name]}')")
    seen[name] = trigger.strip()[:40]

if errs:
    print("Tracking-plan lint errors:")
    for e in errs:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK: {len(seen)} events validated.")
PY
