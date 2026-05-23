#!/usr/bin/env python3
"""validate-trade-off-technical-debt.py

Validate a debt-record artefact against the schema declared in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to debt-record JSON
    --self-test       run built-in fixtures (OK + BAD)
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEBT_ID_RE = re.compile(r"^DEBT-[0-9]{3,5}$")
INTENT = {"deliberate", "inadvertent"}
PRUDENCE = {"prudent", "reckless"}
SEVERITY = {"localized", "systemic"}
OPERATORS = {">", ">=", "<", "<=", "==", "!="}
BANNED_TRIGGER_WORDS = ("someday", "later", "when we have time", "tbd", "soon")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]

    required = ("debt_id", "title", "intent", "prudence", "severity",
                "code_area", "shortcut", "better_solution",
                "repayment_trigger", "budget_cost_pct")
    for k in required:
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "debt_id" in obj and not DEBT_ID_RE.match(str(obj["debt_id"])):
        errs.append(f"debt_id must match ^DEBT-[0-9]{{3,5}}$: got {obj['debt_id']!r}")
    if obj.get("intent") not in INTENT:
        errs.append(f"intent must be in {sorted(INTENT)}: got {obj.get('intent')!r}")
    if obj.get("prudence") not in PRUDENCE:
        errs.append(f"prudence must be in {sorted(PRUDENCE)}: got {obj.get('prudence')!r}")
    if obj.get("severity") not in SEVERITY:
        errs.append(f"severity must be in {sorted(SEVERITY)}: got {obj.get('severity')!r}")

    code_area = obj.get("code_area") or []
    if not (isinstance(code_area, list) and len(code_area) >= 1):
        errs.append("code_area must be non-empty list")
    if obj.get("severity") == "systemic":
        errs.append("severity=systemic must escalate to ATAM, not debt-record (localized-or-systemic rule)")

    for k in ("shortcut", "better_solution"):
        v = obj.get(k, "")
        if len(v) < 16:
            errs.append(f"{k} too short (<16 chars): {len(v)}")

    trig = obj.get("repayment_trigger") or {}
    for k in ("metric", "operator", "threshold", "source"):
        if k not in trig:
            errs.append(f"repayment_trigger missing {k}")
    if trig.get("operator") not in OPERATORS:
        errs.append(f"repayment_trigger.operator must be in {sorted(OPERATORS)}: got {trig.get('operator')!r}")
    # Banned vague words in any trigger field
    for k, v in trig.items():
        if isinstance(v, str) and any(b in v.lower() for b in BANNED_TRIGGER_WORDS):
            errs.append(f"repayment_trigger.{k} contains banned vague word: {v!r}")

    budget = obj.get("budget_cost_pct")
    total = obj.get("current_total_debt_pct", 0)
    if isinstance(budget, (int, float)) and isinstance(total, (int, float)):
        if budget + total > 20:
            errs.append(f"current_total_debt_pct + budget_cost_pct > 20: {total} + {budget} = {total+budget}")

    return errs


OK = {
    "debt_id": "DEBT-0014",
    "title": "Inline auth check in /orders POST; not extracted to middleware",
    "intent": "deliberate",
    "prudence": "prudent",
    "severity": "localized",
    "code_area": ["api/orders.py"],
    "shortcut": "Auth check inlined to ship Q2 launch on time.",
    "better_solution": "Extract to FastAPI dependency injector; covers /orders + 6 future endpoints.",
    "repayment_trigger": {
        "metric": "endpoints_requiring_same_auth_check",
        "operator": ">=",
        "threshold": 3,
        "source": "git grep + endpoint count",
    },
    "budget_cost_pct": 0.6,
    "current_total_debt_pct": 14.2,
}

BAD = {
    "debt_id": "x",
    "title": "auth",
    "intent": "deliberate",
    "prudence": "prudent",
    "severity": "systemic",
    "code_area": ["api/", "billing/", "auth/", "frontend/"],
    "shortcut": "x",
    "better_solution": "y",
    "repayment_trigger": {"metric": "later", "operator": "==", "threshold": "someday", "source": "feels"},
    "budget_cost_pct": 8.0,
    "current_total_debt_pct": 23.0,
}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"OK fixture rejected: {errs_ok}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to debt-record JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"cannot parse JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
