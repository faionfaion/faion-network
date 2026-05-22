#!/usr/bin/env python3
"""validate-structured-output.py — validate structured-output config.

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

REQUIRED = ["provider", "mode", "model_name", "schema_ref", "repair_strategy", "log_raw_on_failure"]
VALID_PROVIDERS = {"openai", "anthropic", "gemini", "mistral", "cohere"}
VALID_MODES = {"response_format", "tool_use_json", "schema_response", "function_call"}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    if obj.get("provider") not in VALID_PROVIDERS:
        errs.append(f"provider must be in {sorted(VALID_PROVIDERS)}")
    if obj.get("mode") not in VALID_MODES:
        errs.append(f"mode must be in {sorted(VALID_MODES)}")
    if obj.get("repair_strategy") not in ("once", "none"):
        errs.append("repair_strategy must be once|none (r3-repair-once)")
    if obj.get("log_raw_on_failure") is not True:
        errs.append("log_raw_on_failure must be true (r4-log-raw-on-failure)")
    # capability matching
    matches = {
        "openai": "response_format",
        "anthropic": "tool_use_json",
        "gemini": "schema_response",
        "mistral": "function_call",
    }
    p, m = obj.get("provider"), obj.get("mode")
    if p in matches and m and m != matches[p]:
        errs.append(f"provider {p} expects mode {matches[p]}, got {m}")
    return errs


FIXTURE_VALID = """
provider: openai
mode: response_format
model_name: gpt-4o-2024-08-06
schema_ref: schemas/SupportTicket.json
repair_strategy: once
log_raw_on_failure: true
"""

FIXTURE_INVALID = """
provider: foo
mode: manual_prompt
model_name: x
schema_ref: x
repair_strategy: infinite
log_raw_on_failure: false
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
    ap = argparse.ArgumentParser(prog="validate-structured-output", description=__doc__,
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
