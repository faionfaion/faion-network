#!/usr/bin/env python3
"""validate-tts-implementation.py — Validate TTSService.synthesize() output.

Inputs:
  - <result.json>  Path to JSON produced by TTSService per 02-output-contract.xml.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - result validates.
  1 - result violates schema.
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

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
PROVIDERS = {"openai", "elevenlabs", "google", "azure"}
STATUSES = {"ok", "error"}
REQUIRED = ["status", "path", "duration_s", "provider", "voice", "model",
            "cache_key", "cached", "chunks"]

VALID_FIXTURE = {
    "status": "ok",
    "path": "out/audio/cache/abc/assembled.mp3",
    "duration_s": 126.6,
    "provider": "openai",
    "voice": "onyx",
    "model": "tts-1-hd",
    "speed": 1.0,
    "cache_key": "9f4a7c3e8d2b1a5f6e9c0d3b2a1f4e8d7c9b6a5d4e3c2b1a0f9e8d7c6b5a4f3e",
    "cached": False,
    "chunks": [
        {"index": 0, "path": "out/audio/cache/abc/c0.mp3", "duration_s": 62.1,
         "char_count": 3950, "cached": False},
        {"index": 1, "path": "out/audio/cache/abc/c1.mp3", "duration_s": 64.5,
         "char_count": 3990, "cached": False},
    ],
}
INVALID_FIXTURE = {
    "status": "ok",
    "path": "out/audio/clone-42.mp3",
    "duration_s": 25.0,
    "provider": "elevenlabs",
    "voice": "cloned-speaker-alice",
    "model": "eleven_multilingual_v2",
    "cache_key": "shortkey",
    "cached": False,
    "chunks": [],
}


def validate(result: dict) -> list[str]:
    out: list[str] = []
    for k in REQUIRED:
        if k not in result:
            out.append(f"missing field: {k}")
    if "status" in result and result["status"] not in STATUSES:
        out.append(f"status not in {STATUSES}")
    if "provider" in result and result["provider"] not in PROVIDERS:
        out.append(f"provider not in {PROVIDERS}")
    if "cache_key" in result and not SHA256_RE.match(str(result["cache_key"])):
        out.append("cache_key must be 64-char sha256 hex")
    if result.get("status") == "ok":
        if not result.get("path"):
            out.append("status ok with empty path")
        if not isinstance(result.get("duration_s"), (int, float)) or result["duration_s"] <= 0.0:
            out.append("status ok with duration_s <= 0.0")
    if isinstance(result.get("chunks"), list):
        if result.get("duration_s", 0) > 60.0 and len(result["chunks"]) < 2:
            out.append("duration_s > 60s requires >=2 chunks")
        for i, c in enumerate(result["chunks"]):
            for k in ("index", "path", "duration_s", "char_count", "cached"):
                if k not in c:
                    out.append(f"chunks[{i}] missing {k}")
        if result["chunks"]:
            total = sum(c.get("duration_s", 0) for c in result["chunks"])
            if abs(total - result.get("duration_s", 0)) > 1.0:
                out.append(f"chunks duration sum {total:.1f} differs from total {result.get('duration_s', 0):.1f} by >1.0s")
    if (result.get("provider") == "elevenlabs"
            and str(result.get("voice", "")).startswith(("cloned-", "clone-"))
            and not result.get("consent_id")):
        out.append("cloned voice without consent_id (r6-clone-consent-gate)")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(data)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
