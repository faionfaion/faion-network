#!/usr/bin/env python3
"""validate-video-gen-tools.py — Validate VideoGenerationService.generate() result.

Inputs:
  - <result.json>  Path to JSON produced by service.generate() per 02-output-contract.xml.

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
STATUSES = {"ok", "failed", "all_providers_failed"}
REQUIRED = ["status", "local_path", "primary_provider", "providers_tried",
            "duration_s", "aspect_ratio", "seed", "prompt_hash"]

VALID_FIXTURE = {
    "status": "ok",
    "local_path": "out/video/abc.mp4",
    "archived_path": "s3://media-prod/videos/abc.mp4",
    "primary_provider": "runway",
    "providers_tried": [
        {"provider": "runway", "task_id": "rw_01", "status": "failed", "error": "policy"},
        {"provider": "luma", "task_id": "lm_42", "status": "ok", "duration_s": 5.04},
    ],
    "duration_s": 5.04,
    "aspect_ratio": "16:9",
    "seed": 42,
    "prompt_hash": "9f4a7c3e8d2b1a5f6e9c0d3b2a1f4e8d7c9b6a5d4e3c2b1a0f9e8d7c6b5a4f3e",
    "retries": 1,
}
INVALID_FIXTURE = {"status": "ok", "local_path": "", "primary_provider": "runway",
                   "providers_tried": [], "duration_s": 0.0, "aspect_ratio": "16:9",
                   "seed": 42, "prompt_hash": "abc"}


def validate(r: dict) -> list[str]:
    out: list[str] = []
    for k in REQUIRED:
        if k not in r:
            out.append(f"missing field: {k}")
    if "status" in r and r["status"] not in STATUSES:
        out.append(f"status not in {STATUSES}")
    if "primary_provider" in r and r["primary_provider"] not in PROVIDERS:
        out.append(f"primary_provider not in {PROVIDERS}")
    if "prompt_hash" in r and not SHA256_RE.match(str(r["prompt_hash"])):
        out.append("prompt_hash must be 64-char sha256 hex")
    if not isinstance(r.get("providers_tried"), list) or len(r.get("providers_tried", [])) < 1:
        out.append("providers_tried must be non-empty list")
    else:
        for i, p in enumerate(r["providers_tried"]):
            for k in ("provider", "task_id", "status"):
                if k not in p:
                    out.append(f"providers_tried[{i}] missing {k}")
            if p.get("provider") not in PROVIDERS:
                out.append(f"providers_tried[{i}].provider not in {PROVIDERS}")
    if r.get("status") == "ok":
        if not r.get("local_path") and not r.get("archived_path"):
            out.append("status ok requires local_path or archived_path")
        if not isinstance(r.get("duration_s"), (int, float)) or r["duration_s"] <= 0:
            out.append("status ok with duration_s <= 0")
    if r.get("status") == "all_providers_failed" and len(r.get("providers_tried", [])) == 0:
        out.append("all_providers_failed but providers_tried empty")
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
        for x in v: sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n"); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
