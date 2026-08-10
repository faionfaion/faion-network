#!/usr/bin/env python3
"""validate-handoff-id-payload.py

Purpose:
    Validate a handoff payload against the schema in content/02-output-contract.xml.
    Confirms only `task_id`, `target_agent`, `decision_metadata` keys are present
    and no forbidden conversation-history fields appear.

Inputs:
    --file PATH      Handoff JSON
    --self-test      Validate the built-in smoke fixture

Outputs:
    Stdout: validation report
    Exit 0 on pass, 1 on failure, 2 on usage error.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TASK_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")
ALLOWED = {"task_id", "target_agent", "decision_metadata"}
FORBIDDEN = {"history", "messages", "raw_input", "conversation"}
HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    extra = set(obj.keys()) - ALLOWED
    if extra:
        errs.append(f"unexpected keys: {sorted(extra)} (only task_id/target_agent/decision_metadata allowed)")
    forbidden = set(obj.keys()) & FORBIDDEN
    if forbidden:
        errs.append(f"forbidden conversation-history keys: {sorted(forbidden)}")
    tid = obj.get("task_id")
    if not isinstance(tid, str) or not TASK_ID_RE.match(tid):
        errs.append(f"task_id: {tid!r} does not match pattern")
    if not obj.get("target_agent"):
        errs.append("target_agent: required non-empty string")
    if not isinstance(obj.get("decision_metadata"), dict):
        errs.append("decision_metadata: required object (may be empty)")
    return errs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--file", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    target = SMOKE if args.self_test else args.file
    if target is None:
        p.error("either --file or --self-test must be given")
    if not target.exists():
        sys.stdout.write(f"FAIL: file not found: {target}\n")
        return 1
    obj = json.loads(target.read_text(encoding="utf-8"))
    obj = {k: v for k, v in obj.items() if not k.startswith("_")}
    errs = validate(obj)
    if errs:
        sys.stdout.write(f"FAIL: {target}\n")
        for e in errs:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write(f"OK: {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
