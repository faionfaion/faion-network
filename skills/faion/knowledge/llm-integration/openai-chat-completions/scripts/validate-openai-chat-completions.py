#!/usr/bin/env python3
"""validate-openai-chat-completions.py — Validate a logged Chat Completions call record.

Inputs:
  - <record.json>  Path to a JSON record matching content/02-output-contract.xml schema.

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
import re
import sys
from pathlib import Path

FINISH_REASONS = {"stop", "length", "tool_calls", "content_filter", "function_call"}
HASH_RE = re.compile(r"^[a-f0-9]{16,64}$")

VALID_FIXTURE = {
    "model": "gpt-4o-mini",
    "messages_hash": "a1b2c3d4e5f60718",
    "params": {"temperature": 0.2, "max_tokens": 1024, "response_format": "json_object", "seed": 42},
    "usage": {"prompt_tokens": 312, "completion_tokens": 187, "total_tokens": 499},
    "finish_reason": "stop",
    "content": '{"answer": "ok"}',
    "latency_ms": 612,
    "request_id": "req_abc123def456",
}
INVALID_FIXTURE = {
    "model": "gpt-4",
    "params": {"temperature": None, "max_tokens": 2048},
    "usage": {},
    "finish_reason": "length",
    "content": '{"answer": "partial...',
}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    for k in ("model", "messages_hash", "params", "usage", "finish_reason", "latency_ms", "request_id"):
        if k not in rec:
            out.append(f"missing field: {k}")
    if "model" in rec and (not isinstance(rec["model"], str) or len(rec["model"]) < 3):
        out.append("model must be string >= 3 chars")
    if "messages_hash" in rec and not HASH_RE.match(str(rec["messages_hash"])):
        out.append("messages_hash must be hex 16-64 chars")
    p = rec.get("params", {})
    if not isinstance(p, dict):
        out.append("params must be object")
    else:
        if "temperature" not in p or p["temperature"] is None:
            out.append("params.temperature missing or null (explicit value required)")
        elif not isinstance(p["temperature"], (int, float)) or not 0 <= p["temperature"] <= 2:
            out.append("params.temperature must be number in [0, 2]")
        if "max_tokens" not in p or not isinstance(p["max_tokens"], int) or p["max_tokens"] < 1:
            out.append("params.max_tokens must be int >= 1")
    u = rec.get("usage", {})
    if not isinstance(u, dict):
        out.append("usage must be object")
    else:
        for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
            if k not in u:
                out.append(f"usage.{k} missing")
            elif not isinstance(u[k], int) or u[k] < 0:
                out.append(f"usage.{k} must be int >= 0")
    fr = rec.get("finish_reason")
    if fr not in FINISH_REASONS:
        out.append(f"finish_reason must be one of {sorted(FINISH_REASONS)}")
    if fr == "length" and rec.get("content"):
        out.append("finish_reason=length with non-null content is invalid (truncated)")
    if "latency_ms" in rec and (not isinstance(rec["latency_ms"], int) or rec["latency_ms"] < 0):
        out.append("latency_ms must be int >= 0")
    if "request_id" in rec and (not isinstance(rec["request_id"], str) or len(rec["request_id"]) < 4):
        out.append("request_id must be string >= 4 chars")
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
