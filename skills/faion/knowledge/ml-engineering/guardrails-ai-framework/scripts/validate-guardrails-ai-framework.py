#!/usr/bin/env python3
"""validate-guardrails-ai-framework.py — Validate output artifact for `guardrails-ai-framework` methodology.

Inputs:
  - <artifact.json>  Path to the JSON artifact produced by this methodology.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - artifact validates.
  1 - artifact violates schema.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in valid + invalid fixtures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = ['pipeline_name', 'schema_path', 'validators', 'on_fail_default', 'max_reasks']
ENUMS = json.loads('{"on_fail_default": ["reask", "fix", "refrain", "filter", "noop"]}')

VALID_FIXTURE = json.loads('{"pipeline_name": "support-reply", "schema_path": "schemas/support_reply.py", "validators": [{"id": "hub:DetectPII@0.0.3", "on_fail": "filter"}, {"id": "hub:ToxicLanguage@0.0.5", "on_fail": "refrain"}], "on_fail_default": "reask", "max_reasks": 3}')
INVALID_FIXTURE = json.loads('{"pipeline_name": "", "schema_path": "", "validators": [], "on_fail_default": "yolo", "max_reasks": 999}')


def validate(obj: dict) -> list[str]:
    out: list[str] = []
    if not isinstance(obj, dict):
        out.append("top-level must be an object")
        return out
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", [], {}):
            out.append(f"required key missing or empty: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            out.append(f"{k}={obj[k]!r} not in {allowed}")
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(obj)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
