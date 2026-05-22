#!/usr/bin/env python3
"""validate-qa-edge-case-spec-template.py — Validate a filled QA edge-case spec.

Inputs:
  - <spec.json>  Path to the spec JSON (or extracted YAML frontmatter + body as JSON).

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
URI_RE = re.compile(r"^https?://[^\s]+$")
STALE_DAYS = 183

VALID_FIXTURE = {
    "header": {
        "version": "1.0.0",
        "owner": "qa-eng:alice",
        "last_reviewed": dt.date.today().isoformat(),
        "incident_url": "https://sentry.io/x/issues/1/",
    },
    "given": "User locale tr_TR submits checkout amount 0.0.",
    "when": "POST /api/v1/checkout fires with body amount 0.",
    "then": "Server returns 422; no Order row created.",
    "evidence": ["https://sentry.io/x/issues/1/"],
    "decisions": {"next_actions": ["pin pytest regression"], "next_review": "2026-11-22"},
}
INVALID_FIXTURE = {"header": {"owner": "qa team"}, "given": "", "when": "", "then": "", "evidence": [], "decisions": {}}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    if "header" not in spec or not isinstance(spec["header"], dict):
        out.append("missing or non-object header")
        return out
    h = spec["header"]
    for k in ("version", "owner", "last_reviewed", "incident_url"):
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
    if "incident_url" in h and not URI_RE.match(str(h["incident_url"])):
        out.append("header.incident_url must be http(s) URL")
    for k in ("given", "when", "then"):
        v = spec.get(k, "")
        if not isinstance(v, str) or len(v) < 10:
            out.append(f"{k} must be string of >= 10 chars")
    ev = spec.get("evidence", [])
    if not isinstance(ev, list) or not ev:
        out.append("evidence must be non-empty list of URLs")
    else:
        for i, u in enumerate(ev):
            if not URI_RE.match(str(u)):
                out.append(f"evidence[{i}] not a URL")
    dec = spec.get("decisions", {})
    if not isinstance(dec, dict) or not dec.get("next_actions") or not dec.get("next_review"):
        out.append("decisions must include next_actions[] and next_review")
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
