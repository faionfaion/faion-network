#!/usr/bin/env python3
"""validate-openai-function-calling.py — Validate an OpenAI function-calling / parse record.

Inputs:
  - <record.json>  Path to a record matching content/02-output-contract.xml schema.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - record validates.
  1 - record violates schema.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in valid + invalid fixtures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KINDS = {"tool_calls", "parsed", "content"}

VALID_FIXTURE = {
    "model": "gpt-4o",
    "kind": "parsed",
    "refusal": None,
    "parsed": {"name": "John Doe", "age": 30, "email": "john@example.com"},
    "tool_calls": None,
    "content": None,
    "latency_ms": 712,
    "request_id": "req_xyz1",
}
INVALID_FIXTURE = {
    "model": "gpt-4o",
    "kind": "parsed",
    "refusal": None,
    "parsed": None,
}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    for k in ("model", "kind", "refusal", "latency_ms", "request_id"):
        if k not in rec:
            out.append(f"missing field: {k}")
    if "model" in rec and (not isinstance(rec["model"], str) or len(rec["model"]) < 3):
        out.append("model must be string >= 3 chars")
    if rec.get("kind") not in KINDS:
        out.append(f"kind must be one of {sorted(KINDS)}")
    if "latency_ms" in rec and (not isinstance(rec["latency_ms"], int) or rec["latency_ms"] < 0):
        out.append("latency_ms must be int >= 0")
    if "request_id" in rec and (not isinstance(rec["request_id"], str) or len(rec["request_id"]) < 4):
        out.append("request_id must be string >= 4 chars")
    k = rec.get("kind")
    if k == "parsed":
        if rec.get("parsed") is None and rec.get("refusal") is None:
            out.append("kind=parsed but both parsed and refusal are null")
    if k == "tool_calls":
        tc = rec.get("tool_calls")
        if not isinstance(tc, list) or not tc:
            out.append("kind=tool_calls requires non-empty tool_calls list")
        else:
            for i, t in enumerate(tc):
                if not isinstance(t, dict):
                    out.append(f"tool_calls[{i}] not object")
                    continue
                for f in ("id", "name", "arguments"):
                    if f not in t:
                        out.append(f"tool_calls[{i}].{f} missing")
                if "id" in t and (not isinstance(t["id"], str) or not t["id"]):
                    out.append(f"tool_calls[{i}].id must be non-empty string")
    if k == "content":
        if not isinstance(rec.get("content"), str) or not rec["content"]:
            out.append("kind=content requires non-empty content string")
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
