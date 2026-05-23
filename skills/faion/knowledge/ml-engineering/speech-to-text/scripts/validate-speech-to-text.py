#!/usr/bin/env python3
"""validate-speech-to-text.py — validate stt-config.yaml.

Inputs: --file PATH | --self-test | --help
Exit:   0 valid, 1 invalid, 2 usage
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["provider", "model", "mode", "max_chunk_seconds", "overlap_seconds", "fallback"]
VALID_PROVIDERS = {"openai-whisper", "openai-gpt4o", "assemblyai", "deepgram", "elevenlabs-scribe", "faster-whisper-local"}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    p, mode = obj.get("provider"), obj.get("mode")
    if p not in VALID_PROVIDERS:
        errs.append(f"provider must be one of {sorted(VALID_PROVIDERS)}")
    if p == "openai-whisper" and mode == "streaming":
        errs.append("openai-whisper does not support streaming (fm-01)")
    chunk = obj.get("max_chunk_seconds", 0)
    overlap = obj.get("overlap_seconds", 0)
    if chunk > 300 and overlap < 3:
        errs.append("chunk > 300s with overlap < 3s loses boundary words (r4-chunking-with-overlap)")
    fb = obj.get("fallback", {})
    if not isinstance(fb, dict) or "provider" not in fb:
        errs.append("fallback.provider required (r5-mandatory-fallback)")
    elif fb.get("provider") == p:
        errs.append("fallback.provider must differ from primary (r5-mandatory-fallback)")
    if p == "openai-gpt4o" and obj.get("custom_vocab"):
        errs.append("openai-gpt4o ignores custom_vocab; use deepgram instead (fm-02)")
    return errs


FIXTURE_VALID = """
provider: deepgram
model: nova-2
mode: streaming
max_chunk_seconds: 300
overlap_seconds: 5
fallback: {provider: faster-whisper-local, trigger: {consecutive_5xx: 3}}
"""

FIXTURE_INVALID = """
provider: openai-whisper
model: whisper-1
mode: streaming
max_chunk_seconds: 600
overlap_seconds: 0
fallback: {provider: openai-whisper, trigger: {}}
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n"); return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n"); return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(prog="validate-speech-to-text", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n"); return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
