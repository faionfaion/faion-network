#!/usr/bin/env python3
"""validate-event-sourcing-agentic.py

Validate a pipeline-run record against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 valid · 1 invalid · 2 usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["aggregate", "stages", "review_outcome"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
STAGE_NAMES = ["aggregate-design", "event-class-codegen", "projection-codegen", "tests-codegen", "antipattern-review"]
MODELS = {"sonnet", "haiku"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "aggregate" in obj and not NAME_RE.match(str(obj["aggregate"])):
        errs.append("aggregate must be PascalCase")
    stages = obj.get("stages") or []
    if len(stages) < 5:
        errs.append("stages must contain all 5 pipeline stages")
    seen = []
    for s in stages:
        if s.get("name") not in STAGE_NAMES:
            errs.append(f"stage name '{s.get('name')}' must be one of {STAGE_NAMES}")
        else:
            seen.append(s["name"])
        if s.get("model") and s["model"] not in MODELS:
            errs.append(f"stage.model '{s.get('model')}' reserved opus forbidden; must be sonnet/haiku")
    ro = obj.get("review_outcome") or {}
    if "all_rules_passed" not in ro:
        errs.append("review_outcome.all_rules_passed required")
    rejected = []
    for s in stages:
        if s.get("accepted") is False:
            rejected.append(s.get("name"))
    if rejected and ro.get("all_rules_passed") is True:
        errs.append(f"stages rejected ({rejected}) but review_outcome.all_rules_passed is true")
    return errs


OK = {
    "aggregate": "Order",
    "stages": [
        {"name": "aggregate-design", "model": "sonnet", "accepted": True, "artefact_path": "design/order.md"},
        {"name": "event-class-codegen", "model": "sonnet", "accepted": True, "artefact_path": "domain/order_events.py"},
        {"name": "projection-codegen", "model": "sonnet", "accepted": True, "artefact_path": "projections/orders.py"},
        {"name": "tests-codegen", "model": "haiku", "accepted": True, "artefact_path": "tests/test_order_es.py"},
        {"name": "antipattern-review", "model": "sonnet", "accepted": True},
    ],
    "review_outcome": {"all_rules_passed": True, "rejected_rule_ids": []},
}
BAD = {
    "aggregate": "order",
    "stages": [
        {"name": "aggregate-design", "model": "opus", "accepted": True},
        {"name": "event-class-codegen", "model": "haiku", "accepted": False, "rejection_reason": "CRUD events"},
    ],
    "review_outcome": {"all_rules_passed": True, "rejected_rule_ids": []},
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
