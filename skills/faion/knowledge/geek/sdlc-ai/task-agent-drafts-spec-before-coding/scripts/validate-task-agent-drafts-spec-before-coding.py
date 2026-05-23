#!/usr/bin/env python3
"""validate-task-agent-drafts-spec-before-coding.py — validate the spec artefact.

Inputs:
    --file PATH       path to artefact JSON
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

REQUIRED = ["ticket_id", "spec_comment_url", "approval_event_url", "pr_url", "approval_mode"]
APPROVAL_ENUM = {
    "linear_thumbs_up",
    "jira_slash_approve",
    "github_label_transition",
    "gitlab_label_transition",
    "auto_approve_label",
}

VALID_FIXTURE = {
    "ticket_id": "LIN-321",
    "spec_comment_url": "https://linear.app/org/issue/LIN-321/comment-12345",
    "approval_event_url": "https://linear.app/org/issue/LIN-321/reaction-67890",
    "pr_url": "https://github.com/org/repo/pull/482",
    "approval_mode": "linear_thumbs_up",
    "auto_approve_label": False,
}

INVALID_FIXTURE = {
    "ticket_id": "LIN-321",
    "spec_comment_url": "",
    "approval_event_url": "",
    "pr_url": "https://github.com/org/repo/pull/482",
    "approval_mode": "silence",
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k in ("spec_comment_url", "approval_event_url", "pr_url"):
        v = obj.get(k, "")
        if not isinstance(v, str) or len(v) < 10:
            errs.append(f"{k}: must be a non-empty URL (>=10 chars)")
    am = obj.get("approval_mode")
    if am not in APPROVAL_ENUM:
        errs.append(f"approval_mode: {am!r} not in {sorted(APPROVAL_ENUM)}")
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
