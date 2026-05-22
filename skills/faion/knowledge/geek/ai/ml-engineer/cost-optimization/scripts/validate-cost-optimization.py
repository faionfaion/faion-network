#!/usr/bin/env python3
"""validate-cost-optimization.py

Validate a cost-plan JSON against content/02-output-contract.xml.

Inputs:
    --file PATH      path to cost-plan JSON
    --self-test      run built-in fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^cop-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ACTION_TYPES = {"router", "prompt-cache", "response-cache", "batch", "prompt-redesign", "no-op"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "pipeline", "stages", "global_budget", "version", "last_reviewed", "measurement_baseline_days"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^cop-[a-z0-9-]{6,}$")
    if "measurement_baseline_days" in obj:
        b = obj["measurement_baseline_days"]
        if not isinstance(b, int) or b < 7:
            errs.append("measurement_baseline_days must be int >= 7 (rule measure-before-optimize)")
    stages = obj.get("stages") or []
    if not isinstance(stages, list) or not stages:
        errs.append("stages must be non-empty list")
    else:
        total_share = 0.0
        for i, st in enumerate(stages):
            if "stage" not in st:
                errs.append(f"stages[{i}].stage missing")
            cs = st.get("current_cost_share")
            if not isinstance(cs, (int, float)) or not (0 <= cs <= 1):
                errs.append(f"stages[{i}].current_cost_share must be in [0,1]")
            else:
                total_share += float(cs)
            ots = st.get("output_token_share")
            if ots is not None and (not isinstance(ots, (int, float)) or not (0 <= ots <= 1)):
                errs.append(f"stages[{i}].output_token_share must be in [0,1] when set")
            actions = st.get("actions") or []
            if not isinstance(actions, list) or not actions:
                errs.append(f"stages[{i}].actions must be non-empty")
            else:
                for j, ac in enumerate(actions):
                    if ac.get("type") not in ACTION_TYPES:
                        errs.append(f"stages[{i}].actions[{j}].type must be one of {sorted(ACTION_TYPES)}")
                    if "rule_ref" not in ac:
                        errs.append(f"stages[{i}].actions[{j}].rule_ref missing")
                    es = ac.get("expected_savings_pct")
                    if es is not None and (not isinstance(es, (int, float)) or not (0 <= es <= 0.95)):
                        errs.append(f"stages[{i}].actions[{j}].expected_savings_pct must be in [0,0.95]")
            # rule batch-the-interactive
            for ac in actions:
                if ac.get("type") == "batch" and st.get("interactive") is True:
                    errs.append(f"stages[{i}] cannot use batch on interactive stage (rule batch-the-the-interactive)")
        if total_share > 1.001:
            errs.append(f"sum of current_cost_share={total_share:.3f} exceeds 1.0")
    gb = obj.get("global_budget") or {}
    if not isinstance(gb, dict):
        errs.append("global_budget must be object")
    else:
        soft = gb.get("daily_soft_usd")
        hard = gb.get("daily_hard_usd")
        alert = gb.get("alert_at_pct")
        if not isinstance(soft, (int, float)) or soft < 0:
            errs.append("global_budget.daily_soft_usd must be number >= 0")
        if not isinstance(hard, (int, float)) or hard < 0:
            errs.append("global_budget.daily_hard_usd must be number >= 0")
        if isinstance(soft, (int, float)) and isinstance(hard, (int, float)) and soft > hard:
            errs.append("global_budget.daily_soft_usd must be <= daily_hard_usd")
        if not isinstance(alert, (int, float)) or not (0.5 <= alert <= 1):
            errs.append("global_budget.alert_at_pct must be in [0.5,1]")
    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


VALID = {
    "artefact_id": "cop-rag-pipeline",
    "pipeline": "neromedia-news-rewrite",
    "measurement_baseline_days": 14,
    "stages": [
        {"stage": "classify", "current_cost_share": 0.30, "output_token_share": 0.10,
         "actions": [{"type": "router", "rule_ref": "route-by-complexity", "expected_savings_pct": 0.65}]},
        {"stage": "rewrite", "current_cost_share": 0.55, "output_token_share": 0.70,
         "actions": [{"type": "prompt-redesign", "rule_ref": "log-output-token-share", "expected_savings_pct": 0.20}]},
        {"stage": "archive", "current_cost_share": 0.15, "output_token_share": 0.05,
         "actions": [{"type": "batch", "rule_ref": "batch-the-offline", "expected_savings_pct": 0.50}]},
    ],
    "global_budget": {"daily_soft_usd": 25, "daily_hard_usd": 50, "alert_at_pct": 0.80},
    "version": "1.1.0",
    "last_reviewed": "2026-05-22",
}

INVALID = {
    "artefact_id": "x",
    "pipeline": "rag",
    "measurement_baseline_days": 0,
    "stages": [{"stage": "all", "current_cost_share": 1.5, "actions": []}],
    "global_budget": {"daily_soft_usd": 100, "daily_hard_usd": 50, "alert_at_pct": 2},
}


def self_test() -> int:
    errs = validate(VALID)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid rejected: {errs}\n")
        return 1
    errs = validate(INVALID)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid accepted\n")
        return 1
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
