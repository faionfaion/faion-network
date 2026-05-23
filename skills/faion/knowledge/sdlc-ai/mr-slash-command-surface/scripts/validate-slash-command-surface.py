#!/usr/bin/env python3
"""validate-slash-command-surface.py — validate the bot-config artefact.

Inputs:
    --file PATH       path to artefact (JSON; workflow YAML can be parsed via yq first)
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["bot", "events", "auto_describe", "auto_review", "auto_improve", "sender_filter"]
BOT_ENUM = {"qodo-merge", "coderabbit", "sourcery", "pr-agent-selfhosted"}

VALID_FIXTURE = {
    "bot": "qodo-merge",
    "events": ["pull_request", "issue_comment"],
    "auto_describe": True,
    "auto_review": True,
    "auto_improve": False,
    "sender_filter": "sender.type != 'Bot'",
    "describe_block_markers": {"start": "AUTO-DESCRIBE-START", "end": "AUTO-DESCRIBE-END"},
}

INVALID_FIXTURE = {
    "bot": "qodo-merge",
    "events": ["pull_request"],
    "auto_describe": True,
    "auto_review": False,
    "auto_improve": True,
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("bot") not in BOT_ENUM and "bot" in obj:
        errs.append(f"bot: not in {sorted(BOT_ENUM)}")
    evs = obj.get("events", [])
    if not isinstance(evs, list) or len(evs) < 2:
        errs.append("events: must be array with minItems 2")
    elif "issue_comment" not in evs:
        errs.append("events: must contain 'issue_comment' (slash dispatch)")
    if obj.get("auto_describe") is not True:
        errs.append("auto_describe: must be true")
    if obj.get("auto_review") is not True:
        errs.append("auto_review: must be true")
    if obj.get("auto_improve") is not False:
        errs.append("auto_improve: must be false")
    if "sender_filter" not in obj or not obj["sender_filter"]:
        errs.append("sender_filter: must be present and non-empty")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
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
