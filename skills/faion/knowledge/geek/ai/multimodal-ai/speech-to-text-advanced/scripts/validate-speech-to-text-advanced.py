#!/usr/bin/env python3
"""Validate output contract for speech-to-text-advanced config.

USAGE:
    validate-speech-to-text-advanced.py <input.json>   Validate a config.
    validate-speech-to-text-advanced.py --self-test    Run built-in fixture.
    validate-speech-to-text-advanced.py --help         Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROVIDERS = {"deepgram", "assemblyai", "openai-whisper-api", "faster-whisper-local", "azure-realtime"}
CAPABILITIES = {
    "deepgram": {"diarisation", "word_timestamps", "vocab_boost", "streaming"},
    "assemblyai": {"diarisation", "word_timestamps", "vocab_boost", "streaming"},
    "azure-realtime": {"streaming", "word_timestamps"},
    "openai-whisper-api": {"word_timestamps"},
    "faster-whisper-local": {"word_timestamps"},
}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("provider", "language", "diarisation", "word_timestamps", "post_process"):
        if k not in c:
            v.append(f"missing required field: {k}")
    prov = c.get("provider")
    if prov and prov not in PROVIDERS:
        v.append(f"provider invalid: {prov!r}")
    caps = CAPABILITIES.get(prov, set())
    if c.get("diarisation") and "diarisation" not in caps:
        v.append(f"provider {prov!r} lacks native diarisation (rule r1)")
    if c.get("word_timestamps") and "word_timestamps" not in caps:
        v.append(f"provider {prov!r} lacks word timestamps (rule r2)")
    vb = c.get("vocab_boost")
    if vb and isinstance(vb, list) and len(vb) > 0 and "vocab_boost" not in caps:
        v.append(f"provider {prov!r} lacks vocab biasing (rule r3)")
    if c.get("streaming") and "streaming" not in caps:
        v.append(f"provider {prov!r} lacks streaming (rule r4)")
    if c.get("diarisation") and not c.get("speaker_hint"):
        v.append("speaker_hint must be set when diarisation=true (rule r5)")
    pp = c.get("post_process") or {}
    if not pp.get("punctuation_restore"):
        v.append("post_process.punctuation_restore required (rule r6)")
    if "filler_removal" not in pp:
        v.append("post_process.filler_removal required (rule r6)")
    if len((c.get("language") or "")) < 2:
        v.append("language must be pinned (>=2 chars)")
    return v


def _self_test() -> int:
    good = {
        "provider": "deepgram",
        "language": "uk",
        "diarisation": True,
        "speaker_hint": 2,
        "word_timestamps": True,
        "vocab_boost": ["faion", "NERO"],
        "streaming": False,
        "post_process": {"punctuation_restore": True, "filler_removal": True, "abbreviation_expand": False},
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = {**good, "provider": "openai-whisper-api"}
    out = validate(bad)
    assert any("diarisation" in x for x in out), "should flag missing diarisation on Whisper"
    assert any("vocab" in x for x in out), "should flag missing vocab on Whisper"
    bad = {**good, "speaker_hint": None}
    bad.pop("speaker_hint")
    assert any("speaker_hint" in x for x in validate(bad)), "should require speaker_hint with diarisation"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-speech-to-text-advanced.py")
    p.add_argument("path", nargs="?", help="JSON config to validate")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
