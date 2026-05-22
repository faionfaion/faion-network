#!/usr/bin/env python3
"""validate-video-gen-basics.py — Validate generate() output against contract.

Inputs:
  - <result.json>  Path to JSON produced by generate() per 02-output-contract.xml.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - validates.
  1 - violation.
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

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
PROVIDERS = {"runway", "luma", "replicate", "pika"}
STATUSES = {"ok", "failed", "timeout", "policy_violation"}
RATIOS = {"16:9", "9:16", "1:1", "4:3", "21:9"}
REQUIRED = ["status", "local_path", "provider", "duration_s", "aspect_ratio",
            "seed", "prompt_hash", "cached"]

VALID_FIXTURE = {
    "status": "ok",
    "local_path": "out/video/abc.mp4",
    "provider": "runway",
    "duration_s": 5.04,
    "aspect_ratio": "16:9",
    "seed": 42,
    "prompt_hash": "9f4a7c3e8d2b1a5f6e9c0d3b2a1f4e8d7c9b6a5d4e3c2b1a0f9e8d7c6b5a4f3e",
    "cached": False,
    "task_id": "task_01HXYZ",
}
INVALID_FIXTURE = {"status": "ok", "local_path": "", "provider": "runway",
                   "duration_s": 12.0, "aspect_ratio": "16:9", "seed": -1,
                   "prompt_hash": "abc", "cached": False}


def validate(r: dict) -> list[str]:
    out: list[str] = []
    for k in REQUIRED:
        if k not in r:
            out.append(f"missing field: {k}")
    if "status" in r and r["status"] not in STATUSES:
        out.append(f"status not in {STATUSES}")
    if "provider" in r and r["provider"] not in PROVIDERS:
        out.append(f"provider not in {PROVIDERS}")
    if "aspect_ratio" in r and r["aspect_ratio"] not in RATIOS:
        out.append(f"aspect_ratio not in {RATIOS}")
    if "prompt_hash" in r and not SHA256_RE.match(str(r["prompt_hash"])):
        out.append("prompt_hash must be sha256 hex (64 lowercase a-f0-9)")
    if r.get("status") == "ok":
        if not r.get("local_path"):
            out.append("status ok with empty local_path")
        if not isinstance(r.get("duration_s"), (int, float)) or not (0.5 <= r["duration_s"] <= 10.0):
            out.append("status ok with duration_s outside [0.5, 10.0]")
        if not r.get("cached") and not r.get("task_id"):
            out.append("status ok with cached=false requires task_id")
    if "seed" in r and (not isinstance(r["seed"], int) or r["seed"] < 0):
        out.append("seed must be non-negative integer")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid rejected: {ok}\n"); return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid accepted\n"); return 1
        sys.stdout.write("self-test OK\n"); return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n"); return 1
    v = validate(data)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n"); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
