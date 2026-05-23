#!/usr/bin/env python3
"""validate-experiment-verdict-template.py

Validate one experiment verdict card JSON against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to verdict JSON
    --self-test       run built-in fixtures
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

BANNED_OWNER = re.compile(r"^(team|we|us)$", re.I)
EXP_ID = re.compile(r"^EXP-[0-9A-Z-]+$")
VERDICTS = {"ship-treatment", "ship-control", "inconclusive-iterate", "inconclusive-stop", "harmful-rollback"}
CONFIDENCE = {"weak", "moderate", "strong"}
REGRESSION_TOKENS = re.compile(r"(?i)(regress|drop|decline|loss)")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("experiment_id", "hypothesis", "arms", "primary", "secondary", "verdict", "learning", "routed", "closed_at"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    if not EXP_ID.match(obj.get("experiment_id", "")):
        errs.append("experiment_id must match EXP-<id>")
    v = obj.get("verdict")
    if v not in VERDICTS:
        errs.append(f"verdict not in 5-enum: {v!r}")
    learning = obj.get("learning") or {}
    if not isinstance(learning.get("claim"), str) or len(learning.get("claim", "")) < 20:
        errs.append("learning.claim < 20 chars (rule captured-learning)")
    if learning.get("confidence") not in CONFIDENCE:
        errs.append(f"learning.confidence invalid: {learning.get('confidence')!r}")
    routed = obj.get("routed") or {}
    owner = routed.get("owner", "")
    if not owner or len(owner) < 3:
        errs.append("routed.owner missing")
    elif BANNED_OWNER.match(owner.strip()):
        errs.append(f"routed.owner plural: {owner!r}")
    if not routed.get("target_date"):
        errs.append("routed.target_date missing")
    # secondary-metric-gate
    secondaries = obj.get("secondary") or []
    has_regression = any(
        isinstance(s, dict) and REGRESSION_TOKENS.search(s.get("result", ""))
        and "NS" not in s.get("result", "") and "flat" not in s.get("result", "")
        for s in secondaries
    )
    if v == "ship-treatment" and has_regression and not obj.get("exec_sign_off"):
        errs.append("ship-treatment with secondary regression requires exec_sign_off (rule secondary-metric-gate)")
    return errs


OK = {
    "experiment_id": "EXP-X", "hypothesis": "Shortening hero copy improves CTA CTR.", "arms": ["c", "t"],
    "primary": {"metric": "cta_ctr", "lift_pct": 6.2, "ci": [2.1, 10.3], "p_value": 0.004},
    "secondary": [{"metric": "signup_cr", "result": "-1.8% NS"}],
    "verdict": "ship-treatment", "exec_sign_off": None,
    "learning": {"claim": "Shorter hero copy lifts CTR on cold traffic without bottom-of-funnel regression.", "confidence": "moderate"},
    "routed": {"owner": "@marina", "target_date": "2026-05-23", "ticket": "REL-1402"},
    "closed_at": "2026-05-20T17:00:00Z",
}
BAD = {"experiment_id": "EXP-X", "verdict": "looks good", "routed": {"owner": "team"}, "learning": {"claim": "x", "confidence": "high"}}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
        sys.stderr.write(f"not a file: {p}\n"); return 2
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
