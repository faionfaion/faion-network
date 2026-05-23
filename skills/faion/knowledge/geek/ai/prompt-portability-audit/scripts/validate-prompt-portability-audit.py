#!/usr/bin/env python3
"""Validate portability-audit-report artefact.

USAGE:
    validate-prompt-portability-audit.py <input.json>
    validate-prompt-portability-audit.py --self-test
    validate-prompt-portability-audit.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEVERITIES = {"low", "medium", "high"}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "scope_paths", "findings", "followup_backlog_link", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r}")
    if not isinstance(s.get("scope_paths"), list) or len(s.get("scope_paths") or []) < 1:
        v.append("scope_paths must be non-empty (rule r1)")
    if not (s.get("followup_backlog_link") or "").strip():
        v.append("followup_backlog_link required (rule r5)")
    findings = s.get("findings")
    if not isinstance(findings, list) or len(findings) < 1:
        v.append("findings must be non-empty list")
    if isinstance(findings, list):
        for i, f in enumerate(findings):
            if not isinstance(f, dict):
                v.append(f"findings[{i}] must be object")
                continue
            for k in ("id", "criterion", "severity", "owner", "deadline", "evidence", "description"):
                if not (f.get(k) or "" if isinstance(f.get(k), str) else f.get(k)):
                    if k not in f or not f.get(k):
                        v.append(f"findings[{i}].{k} required (rules r2,r3,r4)")
            if f.get("severity") not in SEVERITIES:
                v.append(f"findings[{i}].severity must be one of {sorted(SEVERITIES)}")
            if not DATE_RE.match(f.get("deadline", "") or ""):
                v.append(f"findings[{i}].deadline must be ISO YYYY-MM-DD")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO YYYY-MM-DD")
    return v


GOOD = {
    "artefact_id": "portability-audit-support-bot-2026q2",
    "owner": "ruslan@faion.net",
    "scope_paths": ["git://faion/prompts/support-bot.yaml@a1b2c3d"],
    "findings": [{
        "id": "f1",
        "criterion": "claude-xml-thinking-tag",
        "severity": "high",
        "owner": "viktoria@faion.net",
        "deadline": "2026-07-01",
        "evidence": "git://faion/prompts/support-bot.yaml@a1b2c3d#L42",
        "description": "Uses <thinking>.",
    }],
    "followup_backlog_link": "https://github.com/faion/issues?q=label:portability",
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "scope_paths": [],
    "findings": [{"id": "f1", "description": "something"}],
    "followup_backlog_link": "",
    "version": "v1",
    "last_reviewed": "yesterday",
}


def _self_test() -> int:
    errs = validate(GOOD)
    assert errs == [], f"happy failed: {errs}"
    bad = validate(BAD)
    assert any("scope_paths" in x for x in bad)
    assert any("findings[0]" in x for x in bad)
    assert any("followup_backlog_link" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-prompt-portability-audit.py")
    p.add_argument("path", nargs="?")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
