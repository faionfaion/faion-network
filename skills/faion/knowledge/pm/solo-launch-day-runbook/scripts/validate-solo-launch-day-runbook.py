#!/usr/bin/env python3
"""validate-solo-launch-day-runbook.py

Validate the per-launch execution log against the JSON Schema in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to log JSON
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
import sys
from pathlib import Path

REQUIRED = ["launch_id", "product", "announce_at", "founder_name", "pre_checks", "checkpoints", "closeout"]
PRE_REQUIRED = ["smoke_t_minus_24h", "smoke_t_minus_2h", "stripe_live_swap_at", "fallback_content_ready", "rollback_dry_run_at"]
CHECKPOINT_REQUIRED = ["at", "label", "errors_count", "signups_count", "paid_count"]
CLOSEOUT_REQUIRED = ["paid_signups", "total_signups", "errors", "top_3_learnings"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    pre = obj.get("pre_checks")
    if isinstance(pre, dict):
        for k in PRE_REQUIRED:
            if k not in pre:
                errs.append("pre_checks missing: " + k)
        if pre.get("smoke_t_minus_2h") in (None, ""):
            errs.append("pre_checks.smoke_t_minus_2h must be filled before announce")
        if pre.get("fallback_content_ready") is not True:
            errs.append("pre_checks.fallback_content_ready must be true")
    elif "pre_checks" in obj:
        errs.append("pre_checks must be object")
    cps = obj.get("checkpoints")
    if isinstance(cps, list):
        if len(cps) < 5:
            errs.append("checkpoints must have ≥5 entries (T+15m, T+1h, T+4h, T+12h, T+24h)")
        for i, cp in enumerate(cps):
            if not isinstance(cp, dict):
                errs.append(f"checkpoints[{i}] not object")
                continue
            for k in CHECKPOINT_REQUIRED:
                if k not in cp:
                    errs.append(f"checkpoints[{i}] missing: " + k)
    elif "checkpoints" in obj:
        errs.append("checkpoints must be array")
    rb = obj.get("rollback_log")
    if isinstance(rb, list):
        for i, r in enumerate(rb):
            if not isinstance(r, dict) or "reverted_at" not in r:
                errs.append(f"rollback_log[{i}] missing reverted_at")
    co = obj.get("closeout")
    if isinstance(co, dict):
        for k in CLOSEOUT_REQUIRED:
            if k not in co:
                errs.append("closeout missing: " + k)
        learn = co.get("top_3_learnings")
        if not isinstance(learn, list) or len(learn) != 3:
            errs.append("closeout.top_3_learnings must be a 3-item list")
    elif "closeout" in obj:
        errs.append("closeout must be object")
    return errs


OK = {
    "launch_id": "launch-2026-05-23",
    "product": "Faion Pro",
    "announce_at": "2026-05-23T15:00:00Z",
    "founder_name": "Ruslan",
    "pre_checks": {
        "smoke_t_minus_24h": "2026-05-22T15:00:00Z",
        "smoke_t_minus_2h": "2026-05-23T13:00:00Z",
        "stripe_live_swap_at": "2026-05-23T12:50:00Z",
        "stripe_verify_charge_id": "ch_3OabcXYZ",
        "fallback_content_ready": True,
        "rollback_dry_run_at": "2026-05-22T16:00:00Z",
    },
    "checkpoints": [
        {"at": "2026-05-23T15:15:00Z", "label": "T+15m", "errors_count": 0, "signups_count": 12, "paid_count": 3},
        {"at": "2026-05-23T16:00:00Z", "label": "T+1h", "errors_count": 1, "signups_count": 47, "paid_count": 9},
        {"at": "2026-05-23T19:00:00Z", "label": "T+4h", "errors_count": 1, "signups_count": 120, "paid_count": 21},
        {"at": "2026-05-24T03:00:00Z", "label": "T+12h", "errors_count": 2, "signups_count": 180, "paid_count": 31},
        {"at": "2026-05-24T15:00:00Z", "label": "T+24h", "errors_count": 2, "signups_count": 210, "paid_count": 38},
    ],
    "rollback_log": [],
    "closeout": {
        "paid_signups": 38,
        "total_signups": 210,
        "errors": 2,
        "top_3_learnings": ["a", "b", "c"],
        "runbook_updates": [],
    },
}
BAD = {
    "launch_id": "x",
    "product": "X",
    "announce_at": "2026-05-23T15:00:00Z",
    "pre_checks": {"smoke_t_minus_2h": None, "fallback_content_ready": False},
    "checkpoints": [],
}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
