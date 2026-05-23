#!/usr/bin/env python3
"""
purpose: lint a spatial spec for zone + anchor + chin-region violations
consumes: spatial-spec.json
produces: exit-1 with violations on stderr, exit-0 on clean
depends-on: content/01-core-rules.xml three-field-zones + no-interactive-in-far-field rules
token-budget-impact: ~250 tokens when loaded as context
"""
import json, sys
from pathlib import Path
if len(sys.argv) < 2:
    print("usage: spatial-spec-linter.py <spec.json>", file=sys.stderr); sys.exit(2)
obj = json.loads(Path(sys.argv[1]).read_text())
errs = []
for i, e in enumerate(obj.get("elements") or []):
    if e.get("interactive") and e.get("zone") == "far":
        errs.append(f"elements[{i}] interactive control in far field")
    if e.get("interactive") and e.get("anchor") == "world-locked":
        errs.append(f"elements[{i}] primary interactive anchored world-locked")
    if e.get("in_chin_region"):
        errs.append(f"elements[{i}] in chin region")
ra = obj.get("recenter_affordance") or {}
if not ra.get("button") or not ra.get("voice_command"):
    errs.append("recenter_affordance missing button and/or voice_command")
if errs:
    for e in errs:
        print(f"VIOLATION: {e}", file=sys.stderr)
    sys.exit(1)
print("OK")
