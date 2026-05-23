#!/usr/bin/env python3
"""validate-ai-llm-workload-architecture.py — Validate a `ai-llm-workload-architecture` artefact against the output-contract schema.

Inputs:
  - <artefact.json>  Path to the artefact JSON file.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - artefact validates.
  1 - artefact violates schema / cross-field rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in valid + invalid fixtures.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

OWNER_RE = re.compile(r"^[a-z-]+:[a-z0-9._-]+$")
URI_RE = re.compile(r"^https?://[^\s]+$")
CADENCES = {"monthly", "quarterly"}
BAD_TRIGGER_KINDS = {"tbd", "soon", "when needed", ""}

VALID_FIXTURE = {
    "trigger": {"kind": "weekly-review", "url": "https://example.com/t/1"},
    "owner": "swe:alice",
    "inputs": [{"name": "scope", "value": "billing"}],
    "decision": "Adopt variant A behind feature flag.",
    "evidence": ["https://example.com/pr/1"],
    "review": {"cadence": "quarterly", "next_review_at": "2026-08-22"},
}
INVALID_FIXTURE = {
    "trigger": {"kind": "soon", "url": "tbd"},
    "owner": "team",
    "inputs": [],
    "decision": "",
    "evidence": [],
    "review": {},
}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    for k in ("trigger", "owner", "inputs", "decision", "evidence", "review"):
        if k not in rec:
            out.append(f"missing required key: {k}")
    if out:
        return out
    t = rec["trigger"]
    if not isinstance(t, dict) or t.get("kind", "").lower() in BAD_TRIGGER_KINDS:
        out.append("trigger.kind must be a concrete event/threshold/schedule")
    if not URI_RE.match(str(t.get("url", ""))):
        out.append("trigger.url must be an http(s) URL")
    if not OWNER_RE.match(str(rec.get("owner", ""))):
        out.append("owner must match `role:handle` (lowercase, : separator)")
    inputs = rec.get("inputs", [])
    if not isinstance(inputs, list) or not inputs:
        out.append("inputs must be a non-empty list")
    else:
        for i, item in enumerate(inputs):
            if not isinstance(item, dict) or "name" not in item or "value" not in item:
                out.append(f"inputs[{i}] must have name + value")
    if not str(rec.get("decision", "")).strip():
        out.append("decision must be a non-empty sentence")
    ev = rec.get("evidence", [])
    if not isinstance(ev, list) or not ev:
        out.append("evidence must be a non-empty list of URLs")
    else:
        for i, u in enumerate(ev):
            if not URI_RE.match(str(u)):
                out.append(f"evidence[{i}] must be an http(s) URL")
    r = rec.get("review", {})
    if r.get("cadence") not in CADENCES:
        out.append("review.cadence must be 'monthly' or 'quarterly'")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(r.get("next_review_at", ""))):
        out.append("review.next_review_at must be YYYY-MM-DD")
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
