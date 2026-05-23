#!/usr/bin/env python3
"""validate-regression-test-first-bugfix-workflow.py — Validate a red-test-first workflow record.

Inputs:
  - <record.json>  Path to the workflow-record JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - record validates.
  1 - record violates schema / ownership / red-test-first rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TRIGGER_KINDS = {"sentry", "datadog", "customer-ticket", "log-aggregator"}
COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")
URI_RE = re.compile(r"^https?://[^\s]+$")
OWNER_RE = re.compile(r"^[a-z-]+:[a-z0-9._-]+$")
CADENCES = {"monthly", "quarterly"}

VALID_FIXTURE = {
    "trigger": {"kind": "sentry", "url": "https://sentry.io/x/issues/1/"},
    "red_test": {"path": "tests/regression/test_zero.py", "commit": "abc1234", "asserts": ["422"]},
    "fix": {"pr_url": "https://github.com/o/r/pull/1", "diff_lines": 5},
    "verification": {"ci_run_url": "https://github.com/o/r/actions/runs/1", "passed": True},
    "owner": "swe:alice",
    "review": {"cadence": "quarterly", "next_review_at": "2026-08-22"},
}
INVALID_FIXTURE = {
    "trigger": {"kind": "gut", "url": "tbd"},
    "red_test": {"path": "src/x.py", "commit": "main", "asserts": []},
    "fix": {"pr_url": "soon", "diff_lines": 0},
    "verification": {"passed": False},
    "owner": "team",
    "review": {},
}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    for k in ("trigger", "red_test", "fix", "verification", "owner", "review"):
        if k not in rec:
            out.append(f"missing required key: {k}")
    if out:
        return out
    t = rec["trigger"]
    if t.get("kind") not in TRIGGER_KINDS:
        out.append(f"trigger.kind not in {sorted(TRIGGER_KINDS)}")
    if not URI_RE.match(str(t.get("url", ""))):
        out.append("trigger.url must be http(s) URL")
    rt = rec["red_test"]
    if not str(rt.get("path", "")).startswith("tests/"):
        out.append("red_test.path must start with tests/")
    if not COMMIT_RE.match(str(rt.get("commit", ""))):
        out.append("red_test.commit must be 7-40 hex chars")
    if not isinstance(rt.get("asserts"), list) or not rt.get("asserts"):
        out.append("red_test.asserts must be non-empty list")
    f = rec["fix"]
    if not URI_RE.match(str(f.get("pr_url", ""))):
        out.append("fix.pr_url must be http(s) URL")
    if not isinstance(f.get("diff_lines"), int) or f.get("diff_lines", 0) < 1:
        out.append("fix.diff_lines must be int >= 1")
    v = rec["verification"]
    if not URI_RE.match(str(v.get("ci_run_url", ""))):
        out.append("verification.ci_run_url must be http(s) URL")
    if v.get("passed") is not True:
        out.append("verification.passed must be true")
    if not OWNER_RE.match(str(rec.get("owner", ""))):
        out.append(f"owner must match {OWNER_RE.pattern!r}")
    r = rec["review"]
    if r.get("cadence") not in CADENCES:
        out.append(f"review.cadence not in {sorted(CADENCES)}")
    if "next_review_at" not in r:
        out.append("review.next_review_at missing")
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
        rec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(rec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
