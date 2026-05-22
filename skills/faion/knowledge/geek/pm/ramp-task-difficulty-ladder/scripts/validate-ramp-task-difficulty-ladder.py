#!/usr/bin/env python3
"""validate-ramp-task-difficulty-ladder.py — Validate a filled ramp-task ladder spec.

Inputs:
  - <spec.json>  Path to the ladder JSON (header + ladder rows + owner + outcome review).

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - spec validates.
  1 - spec violates schema / staleness / ownership rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
STALE_DAYS = 183
ALLOWED_TRIGGERS_PREFIX = ("hire", "start-date", "ticket", "calendar", "threshold", "event")
ALLOWED_CADENCE = {"monthly", "quarterly"}
MIN_RUNGS = 3

VALID_FIXTURE = {
    "header": {
        "version": "1.0.0",
        "owner": "tech-lead:alice",
        "last_reviewed": dt.date.today().isoformat(),
        "trigger": "hire-signed",
        "evidence_root": "onboarding/",
        "review_cadence": "quarterly",
    },
    "ladder": [
        {"rung": 1, "pattern": "docs", "duration_days": 1, "evidence": "https://github.com/x/pulls/1"},
        {"rung": 2, "pattern": "rename", "duration_days": 2, "evidence": "https://github.com/x/pulls/2"},
        {"rung": 3, "pattern": "endpoint", "duration_days": 3, "evidence": "https://github.com/x/pulls/3"},
    ],
    "outcome_review": {
        "last_run": dt.date.today().isoformat(),
        "next_due": (dt.date.today() + dt.timedelta(days=90)).isoformat(),
        "outcomes": ["time-to-first-PR"],
    },
}
INVALID_FIXTURE = {"header": {"owner": "team"}, "ladder": [], "outcome_review": {}}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    h = spec.get("header")
    if not isinstance(h, dict):
        out.append("missing or non-object header")
        return out
    for k in ("version", "owner", "last_reviewed", "trigger", "review_cadence"):
        if k not in h:
            out.append(f"header.{k} missing")
    if "version" in h and not SEMVER_RE.match(str(h["version"])):
        out.append("header.version must be semver")
    if "owner" in h:
        owner = str(h["owner"])
        if ":" not in owner or owner.lower().endswith(("team", "channel", "everyone")):
            out.append("header.owner must be person (role:person), not team")
    if "last_reviewed" in h:
        try:
            d = dt.date.fromisoformat(str(h["last_reviewed"]))
            age = (dt.date.today() - d).days
            if age > STALE_DAYS:
                out.append(f"header.last_reviewed stale ({age} days; max {STALE_DAYS})")
        except ValueError:
            out.append("header.last_reviewed not ISO date")
    if "trigger" in h:
        trig = str(h["trigger"]).strip().lower()
        if not trig or not any(trig.startswith(p) for p in ALLOWED_TRIGGERS_PREFIX):
            out.append("header.trigger must be a named observable event prefix")
    if "review_cadence" in h and str(h["review_cadence"]) not in ALLOWED_CADENCE:
        out.append(f"header.review_cadence must be one of {sorted(ALLOWED_CADENCE)}")
    ladder = spec.get("ladder", [])
    if not isinstance(ladder, list) or len(ladder) < MIN_RUNGS:
        out.append(f"ladder must be a list of >= {MIN_RUNGS} rungs")
    else:
        for i, r in enumerate(ladder):
            if not isinstance(r, dict):
                out.append(f"ladder[{i}] not object")
                continue
            for k in ("rung", "pattern", "duration_days", "evidence"):
                if k not in r:
                    out.append(f"ladder[{i}].{k} missing")
    rev = spec.get("outcome_review", {})
    if not isinstance(rev, dict) or not rev.get("last_run") or not rev.get("next_due"):
        out.append("outcome_review must include last_run and next_due ISO dates")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(spec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
