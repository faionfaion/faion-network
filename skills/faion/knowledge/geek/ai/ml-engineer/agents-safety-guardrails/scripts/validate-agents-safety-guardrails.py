#!/usr/bin/env python3
"""validate-agents-safety-guardrails.py — Validate an output artefact for the `agents-safety-guardrails` methodology.

Inputs:
  <artefact.json>  Path to the artefact JSON file.

Outputs:
  stdout: PASS / FAIL with one violation per line.

Exit codes:
  0 - artefact validates.
  1 - artefact violates schema.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in fixtures.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

SLUG = "agents-safety-guardrails"
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
OWNER_RE = re.compile(r"^[a-z-]+:[a-z0-9._-]+$")
URI_RE = re.compile(r"^https?://[^\s]+$")
CADENCES = {"weekly", "monthly", "quarterly"}
PRODUCES = "config"

VALID_FIXTURE = {
    "slug": SLUG,
    "version": "1.1.0",
    "owner": "ml-eng:alice",
    "produced_at": "2026-05-22T11:30:00Z",
    "produces": PRODUCES,
    "scope": {"title": "Smoke-test agents-safety-guardrails", "context_link": "https://github.com/org/repo/issues/0"},
    "approver": "tl:bob",
    "review": {"cadence": "quarterly", "next_review_at": "2026-08-22"},
}

INVALID_FIXTURE = {
    "slug": "wrong",
    "version": "0.1",
    "owner": "team",
    "produced_at": "soon",
    "produces": "vibes",
    "scope": {"title": "tbd"},
    "approver": "",
    "review": {},
}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    for k in ("slug", "version", "owner", "produced_at", "produces", "scope", "approver", "review"):
        if k not in rec:
            out.append(f"missing required key: {k}")
    if out:
        return out
    if rec.get("slug") != SLUG:
        out.append(f"slug must equal {SLUG!r}")
    if not SEMVER_RE.match(str(rec.get("version", ""))):
        out.append("version must be semver")
    if not OWNER_RE.match(str(rec.get("owner", ""))):
        out.append("owner must match role:person")
    if not OWNER_RE.match(str(rec.get("approver", ""))):
        out.append("approver must match role:person")
    try:
        datetime.fromisoformat(str(rec.get("produced_at", "")).replace("Z", "+00:00"))
    except ValueError:
        out.append("produced_at must be ISO date-time")
    if rec.get("produces") != PRODUCES:
        out.append(f"produces must equal {PRODUCES!r}")
    scope = rec.get("scope", {})
    if not isinstance(scope, dict):
        out.append("scope must be object")
    else:
        if len(str(scope.get("title", ""))) < 5:
            out.append("scope.title must be >= 5 chars")
        if not URI_RE.match(str(scope.get("context_link", ""))):
            out.append("scope.context_link must be http(s) URL")
    review = rec.get("review", {})
    if not isinstance(review, dict):
        out.append("review must be object")
    else:
        if review.get("cadence") not in CADENCES:
            out.append(f"review.cadence not in {sorted(CADENCES)}")
        try:
            date.fromisoformat(str(review.get("next_review_at", "")))
        except ValueError:
            out.append("review.next_review_at must be ISO date")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv or "-h" in argv else 2
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
