#!/usr/bin/env python3
"""validate-prompt-techniques.py — Validate a PromptLibrary entry JSON record.

Inputs:
  - <entry.json>  Path to a JSON entry matching content/02-output-contract.xml schema.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - entry validates.
  1 - violates output contract.
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

SLUG_RE = re.compile(r"^[a-z0-9\-]+$")
VERSION_RE = re.compile(r"^v[0-9]+(\.[0-9]+)*$")
OWNER_RE = re.compile(r"^[a-z][a-z0-9\-]*:.+$")

VALID_FIXTURE = {
    "slug": "summary-3-bullet",
    "version": "v2",
    "model": "gpt-4o-mini",
    "prompt": "Summarise in exactly 3 bullet points, each <= 15 words.",
    "eval_score": 0.92,
    "golden_set_id": "summary-bench-2026q2",
    "created_at": "2026-05-22T12:00:00Z",
    "owner": "ml-eng:alice",
}
INVALID_FIXTURE = {
    "slug": "Summary 3 Bullet",
    "version": "2",
    "model": "gpt",
    "prompt": "Summarise",
    "owner": "team",
}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    for k in ("slug", "version", "model", "prompt", "eval_score", "golden_set_id", "created_at", "owner"):
        if k not in rec:
            out.append(f"missing field: {k}")
    if "slug" in rec and (not isinstance(rec["slug"], str) or not SLUG_RE.match(rec["slug"]) or len(rec["slug"]) < 3):
        out.append("slug must match ^[a-z0-9\\-]+$ and len >= 3")
    if "version" in rec and (not isinstance(rec["version"], str) or not VERSION_RE.match(rec["version"])):
        out.append("version must match ^v[0-9]+(\\.[0-9]+)*$")
    if "model" in rec and (not isinstance(rec["model"], str) or len(rec["model"]) < 3):
        out.append("model must be string >= 3 chars")
    if "prompt" in rec and (not isinstance(rec["prompt"], str) or len(rec["prompt"]) < 10):
        out.append("prompt must be string >= 10 chars")
    if "eval_score" in rec and (not isinstance(rec["eval_score"], (int, float)) or not 0 <= rec["eval_score"] <= 1):
        out.append("eval_score must be number in [0, 1]")
    if "owner" in rec:
        own = rec["owner"]
        if not isinstance(own, str) or not OWNER_RE.match(own):
            out.append("owner must be role:person, not team/channel")
        else:
            person_part = own.split(":", 1)[1].lower()
            if person_part in ("team", "channel", "everyone") or person_part.startswith("team") or person_part.startswith("channel"):
                out.append("owner must be role:person, not team/channel")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if any(a in ("--help", "-h") for a in argv) else 2
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
