#!/usr/bin/env python3
"""Validate output contract for speech-to-text-basics config.

USAGE:
    validate-speech-to-text-basics.py <input.json>   Validate a config.
    validate-speech-to-text-basics.py --self-test    Run built-in fixture.
    validate-speech-to-text-basics.py --help         Show this help.

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

PROVIDERS = {"openai-whisper-api", "faster-whisper-local"}
FORMATS = {"verbose_json", "json", "text", "srt", "vtt"}
GRANS = {"segment", "word"}
MAX_FILE_MB = 25


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("provider", "language", "response_format", "timestamp_granularities"):
        if k not in c:
            v.append(f"missing required field: {k}")
    if c.get("provider") and c["provider"] not in PROVIDERS:
        v.append(f"provider invalid: {c['provider']!r}")
    lang = c.get("language") or ""
    if len(lang) < 2:
        v.append("language must be pinned (>=2 chars) (rule r1)")
    rf = c.get("response_format")
    if rf and rf not in FORMATS:
        v.append(f"response_format invalid: {rf!r}")
    if rf and rf != "verbose_json":
        v.append("response_format must be verbose_json for production (rule r2)")
    tg = c.get("timestamp_granularities")
    if isinstance(tg, list):
        if not tg:
            v.append("timestamp_granularities must be non-empty (rule r2)")
        for g in tg:
            if g not in GRANS:
                v.append(f"timestamp_granularities contains invalid: {g!r}")
    mfm = c.get("max_file_mb")
    if isinstance(mfm, int) and mfm > MAX_FILE_MB:
        v.append(f"max_file_mb {mfm} > {MAX_FILE_MB} hard API cap (rule r4)")
    return v


def _self_test() -> int:
    good = {
        "provider": "openai-whisper-api",
        "language": "uk",
        "response_format": "verbose_json",
        "timestamp_granularities": ["segment"],
        "max_file_mb": 25,
        "split_on_silence": True,
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = dict(good); bad.pop("language")
    assert any("language" in x for x in validate(bad)), "should require language"
    bad = dict(good); bad["response_format"] = "text"
    assert any("verbose_json" in x for x in validate(bad)), "should require verbose_json"
    bad = dict(good); bad["max_file_mb"] = 100
    assert any("max_file_mb" in x for x in validate(bad)), "should reject >25MB cap"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-speech-to-text-basics.py")
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
