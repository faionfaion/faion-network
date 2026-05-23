#!/usr/bin/env python3
"""validate-video-generation-async-api.py — validate VideoJob / provider-config.

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

REQUIRED = ["provider", "idempotency_key", "poll_backoff_seconds", "total_wait_cap_seconds", "artefact_storage", "fallback"]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    key = obj.get("idempotency_key", "")
    if not key or len(key) < 16:
        errs.append("idempotency_key required, >=16 chars (r1-idempotency-key)")
    backoff = obj.get("poll_backoff_seconds", [])
    if isinstance(backoff, list) and backoff and backoff[0] < 1:
        errs.append("poll_backoff_seconds[0] must be >= 1 (r2-exp-backoff-polling)")
    cap = obj.get("total_wait_cap_seconds", 0)
    if cap < 60 or cap > 900:
        errs.append("total_wait_cap_seconds must be in [60, 900] (r3-total-wait-cap)")
    fb = obj.get("fallback", {})
    if isinstance(fb, dict) and fb.get("provider") == obj.get("provider"):
        errs.append("fallback.provider must differ from primary (r5-provider-fallback)")
    return errs


FIXTURE_VALID = """
provider: runway
idempotency_key: "8f2a000000000000"
poll_backoff_seconds: [1, 2, 4, 8, 16, 30]
total_wait_cap_seconds: 600
artefact_storage: {bucket: x, key_prefix: y}
fallback: {provider: luma, trigger: timeout}
"""

FIXTURE_INVALID = """
provider: runway
idempotency_key: ""
poll_backoff_seconds: [0.1, 0.2]
total_wait_cap_seconds: 5000
artefact_storage: {bucket: x, key_prefix: y}
fallback: {provider: runway, trigger: x}
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
    ap = argparse.ArgumentParser(prog="validate-video-generation-async-api", description=__doc__,
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
