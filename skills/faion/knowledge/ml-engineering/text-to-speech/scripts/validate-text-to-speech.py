#!/usr/bin/env python3
"""validate-text-to-speech.py — validate text-to-speech config.

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

REQUIRED = ['provider', 'model', 'voice', 'cache', 'fallback']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    if obj.get("provider") not in {"openai", "elevenlabs", "google", "azure", "deepgram", "local-coqui"}:
        errs.append('provider must be in {openai, elevenlabs, google, azure, deepgram, local-coqui}')
    if not isinstance(obj.get("cache"), dict) or not obj["cache"].get("enabled"):
        errs.append('cache.enabled must be true (r3-cache-by-text-hash)')
    if isinstance(obj.get("fallback"), dict) and obj["fallback"].get("provider") == obj.get("provider"):
        errs.append('fallback.provider must differ from primary (r5-fallback-mandatory)')
    if obj.get("voice", {}).get("clone_consent") is False:
        errs.append('voice cloning requires explicit consent record (r4-consent-for-cloning)')
    return errs


FIXTURE_VALID = '\nprovider: elevenlabs\nmodel: eleven_turbo_v2\nvoice: {id: rachel, clone_consent: true}\ncache: {enabled: true, ttl_days: 30}\nfallback: {provider: openai, model: tts-1}\n'
FIXTURE_INVALID = '\nprovider: foo\nmodel: x\nvoice: {id: x, clone_consent: false}\ncache: {enabled: false}\nfallback: {provider: foo}\n'


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
    ap = argparse.ArgumentParser(prog="validate-text-to-speech", description=__doc__,
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
