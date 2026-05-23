#!/usr/bin/env python3
"""validate-solo-context-switch-protocol.py

Validate the daily block-log artefact against the JSON Schema in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
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

MODES = {"builder", "operator", "inbox"}
REQUIRED = ["date", "blocks", "violations_today", "urgency_overrides_today"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    blocks = obj.get("blocks")
    if isinstance(blocks, list):
        if len(blocks) < 2:
            errs.append("blocks must have >= 2 entries")
        for i, b in enumerate(blocks):
            if not isinstance(b, dict):
                errs.append(f"blocks[{i}] not object")
                continue
            if b.get("mode") not in MODES:
                errs.append(f"blocks[{i}].mode not in enum")
            hn = b.get("handoff_note") or ""
            if not isinstance(hn, str) or len(hn.strip()) < 20:
                errs.append(f"blocks[{i}].handoff_note missing or too short (need >=20 chars)")
            if b.get("mode") == "builder" and b.get("notifications") != "silenced":
                errs.append(f"blocks[{i}] builder block must have notifications=silenced")
        if blocks and blocks[0].get("mode") != "builder":
            errs.append("first block mode must be builder")
    elif "blocks" in obj:
        errs.append("blocks must be array")
    uo = obj.get("urgency_overrides_today")
    if isinstance(uo, int) and uo > 2:
        errs.append("urgency_overrides_today > 2 indicates override-list abuse")
    return errs


OK = {
    "date": "2026-05-20",
    "blocks": [
        {"mode": "builder", "window": "09:00-12:00", "notifications": "silenced", "handoff_note": "Open: checkout-retry. Next: exp vs fixed backoff. Operator: env STRIPE_RETRY_MAX=5."},
        {"mode": "operator", "window": "13:00-15:00", "notifications": "open", "handoff_note": "Closed 2 DMs + refund. Next: data-export FAQ. Builder: nothing."},
        {"mode": "inbox", "window": "15:00-16:00", "notifications": "open", "handoff_note": "Inbox zero. Next: tomorrow Builder agenda set."},
    ],
    "first_block_mode": "builder",
    "violations_today": 0,
    "urgency_overrides_today": 0,
}
BAD = {
    "date": "2026-05-20",
    "blocks": [
        {"mode": "inbox", "window": "09:00-09:30", "notifications": "open", "handoff_note": ""},
        {"mode": "builder", "window": "09:30-11:00", "notifications": "open", "handoff_note": ""},
    ],
    "first_block_mode": "inbox",
    "violations_today": 5,
    "urgency_overrides_today": 4,
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
