#!/usr/bin/env python3
"""validate-team-charter-working-agreement.py — Validate a filled team charter.

Inputs:
  - <charter.json>  Path to the charter JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - charter validates.
  1 - charter violates schema / ownership / staleness rules.
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
OWNER_RE = re.compile(r"^[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+$")
ARTEFACT_RE = re.compile(r"^[a-z0-9-]+$")
STALE_DAYS = 90
REQUIRED_SECTIONS = ("mission", "decision_rights", "working_hours", "ai_tool_policy", "code_review_sla", "on_call_rotation")

VALID_FIXTURE = {
    "artefact_id": "team-a-charter",
    "owner": "tech-lead:alice",
    "decision": "Adopt async-first working hours with 4h overlap window.",
    "rationale": "Q2-2026 retro flagged 3 timezones causing meeting overload; survey of 12 team members preferred async.",
    "inputs_used": [{"name": "Q2-2026 retro", "source": "https://repo/retro.md"}],
    "version": "1.0.0",
    "last_reviewed": dt.date.today().isoformat(),
    "sections": {k: "filled" for k in REQUIRED_SECTIONS},
}
INVALID_FIXTURE = {"owner": "team"}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    for k in ("artefact_id", "owner", "decision", "rationale", "inputs_used", "version", "last_reviewed"):
        if k not in spec:
            out.append(f"{k} missing")
    if "artefact_id" in spec and not ARTEFACT_RE.match(str(spec["artefact_id"])):
        out.append("artefact_id must be kebab-case slug")
    if "owner" in spec:
        owner = str(spec["owner"])
        if not OWNER_RE.match(owner) or owner.lower().startswith(("team", "we", "us", "engineering", "the-team", "the-squad")):
            out.append("owner must be role:person, not team")
    if "version" in spec and not SEMVER_RE.match(str(spec["version"])):
        out.append("version must be semver")
    if "last_reviewed" in spec:
        try:
            d = dt.date.fromisoformat(str(spec["last_reviewed"]))
            age = (dt.date.today() - d).days
            if age > STALE_DAYS:
                out.append(f"last_reviewed stale ({age} days; max {STALE_DAYS})")
        except ValueError:
            out.append("last_reviewed not ISO date")
    inputs = spec.get("inputs_used", [])
    if not isinstance(inputs, list) or not inputs:
        out.append("inputs_used must be non-empty list")
    else:
        for i, it in enumerate(inputs):
            if not isinstance(it, dict) or "name" not in it or "source" not in it:
                out.append(f"inputs_used[{i}] must include name and source")
    rationale = spec.get("rationale", "")
    if len(str(rationale)) < 30:
        out.append("rationale must be at least 30 chars and cite an input")
    sections = spec.get("sections", {})
    for k in REQUIRED_SECTIONS:
        if not sections.get(k):
            out.append(f"sections.{k} missing or empty")
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
