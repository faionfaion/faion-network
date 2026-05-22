#!/usr/bin/env python3
"""validate-agent-builder-community-rituals.py — Validate a ritual session log.

Inputs:
  - <log.json>  Path to a single-session JSON log (ritual_id, host, artefact_link, retention).

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - log validates.
  1 - log violates cadence / host / artefact / retention rules.
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

OWNER_RE = re.compile(r"^[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+$")
URL_RE = re.compile(r"^https?://[^\s]+$")
ALLOWED_RITUALS = {"office-hours", "eval-sharing", "prompt-swap"}
HOST_ROTATION_MAX = 6
RETENTION_ALARM_PCT = 30

VALID_FIXTURE = {
    "ritual_id": "office-hours",
    "session_date": dt.date.today().isoformat(),
    "host": "host:alice",
    "organiser": "organiser:bob",
    "attendees": ["@a", "@b", "@c"],
    "artefact_link": "https://example.com/qa-log/1",
    "session_index": 3,
    "host_session_count": 2,
    "retention_90d_pct": 42,
}
INVALID_FIXTURE = {"ritual_id": "random", "host": "team"}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    for k in ("ritual_id", "session_date", "host", "organiser", "artefact_link", "retention_90d_pct"):
        if k not in spec:
            out.append(f"{k} missing")
    if "ritual_id" in spec and spec["ritual_id"] not in ALLOWED_RITUALS:
        out.append(f"ritual_id must be one of {sorted(ALLOWED_RITUALS)}")
    if "session_date" in spec:
        try:
            dt.date.fromisoformat(str(spec["session_date"]))
        except ValueError:
            out.append("session_date not ISO date")
    for k in ("host", "organiser"):
        if k in spec and not OWNER_RE.match(str(spec[k])):
            out.append(f"{k} must be role:person")
    if "artefact_link" in spec and not URL_RE.match(str(spec["artefact_link"])):
        out.append("artefact_link must be http(s) URL (rule r2-artefact-per-ritual)")
    hc = spec.get("host_session_count", 0)
    if isinstance(hc, int) and hc > HOST_ROTATION_MAX:
        out.append(f"host_session_count {hc} exceeds rotation max {HOST_ROTATION_MAX} (rule r4-rotating-host)")
    r = spec.get("retention_90d_pct")
    if isinstance(r, (int, float)) and r < RETENTION_ALARM_PCT:
        out.append(f"retention_90d_pct {r} below alarm threshold {RETENTION_ALARM_PCT} — design review required")
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
