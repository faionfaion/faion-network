#!/usr/bin/env python3
"""validate-structured-tool-errors.py — validate a ToolError envelope JSON body.

Inputs:
  - <error.json>  Path to a JSON file matching the templates/error_envelope.json schema.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - body validates.
  1 - body violates schema or self-check rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in fixtures.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]+$")
HINTS = {"RETRY_LATER", "CHECK_INPUT", "TRY_ALTERNATIVE", "REPORT_TO_USER", "NEEDS_AUTH"}

VALID_FIXTURE = {
    "error": {
        "code": "UPSTREAM_RATE_LIMITED",
        "message": "GitHub API returned 429.",
        "recoveryHint": "RETRY_LATER",
        "retry_after_seconds": 60,
        "traceId": "01HX9V7Q2XQF9P0M4Z",
    }
}

INVALID_FIXTURE = {
    "error": {
        "code": "429",
        "message": "TypeError: NoneType has no attribute 'json' at /app/tools/github.py:42",
        "recoveryHint": "RETRY_NOW",
        "traceId": "x",
    }
}


def validate(body: dict) -> list[str]:
    v: list[str] = []
    if "error" not in body:
        return ["missing required key: error"]
    err = body["error"]
    if not isinstance(err, dict):
        return ["error must be an object"]
    for k in ("code", "message", "recoveryHint", "traceId"):
        if k not in err:
            v.append(f"error.{k} missing")
    if v:
        return v
    if not CODE_RE.match(str(err["code"])):
        v.append(f"error.code must match ^[A-Z][A-Z0-9_]+$ (got {err['code']!r})")
    if not isinstance(err["message"], str) or not (1 <= len(err["message"]) <= 240):
        v.append("error.message must be string 1..240 chars")
    if err["recoveryHint"] not in HINTS:
        v.append(f"error.recoveryHint not in closed enum (got {err['recoveryHint']!r})")
    if not isinstance(err["traceId"], str) or len(err["traceId"]) < 8:
        v.append("error.traceId must be string >= 8 chars")
    if "retry_after_seconds" in err:
        ras = err["retry_after_seconds"]
        if not isinstance(ras, int) or not (0 <= ras <= 3600):
            v.append("error.retry_after_seconds must be int 0..3600")
    # Heuristic stack-trace detection
    if "  File " in err.get("message", "") or "Traceback" in err.get("message", ""):
        v.append("error.message must not contain stack frames")
    return v


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
        body = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    violations = validate(body)
    if violations:
        sys.stdout.write("FAIL\n")
        for x in violations:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
