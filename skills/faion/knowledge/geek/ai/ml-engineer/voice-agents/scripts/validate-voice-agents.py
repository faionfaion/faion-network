#!/usr/bin/env python3
# purpose: validate voice-agents JSON artefact against 02-output-contract schema
# consumes: JSON file passed via --file
# produces: exit-code 0 (valid) or 1 (invalid + violations on stderr)
# depends-on: stdlib only (argparse + json + re + pathlib)
# token-budget-impact: 0 (out-of-band)
"""validate-voice-agents.py — validate a voice-agents JSON artefact.

Inputs:
    --file PATH    JSON file to validate
    --self-test    run built-in valid + invalid fixtures
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

REQUIRED = ['call_id', 'agent_version', 'avg_handle_time_s', 'escalation_rate', 'p95_stt_ms', 'p95_llm_ms']

TYPE_MAP = {
    'call_id': 'string',
    'agent_version': 'string',
    'avg_handle_time_s': 'number',
    'escalation_rate': 'number',
    'p95_stt_ms': 'number',
    'p95_llm_ms': 'number',
    'p95_tts_ms': 'number',
    'transcript_url': 'string',
}

PYTHON_TYPES = {
    "string": str, "integer": int, "number": (int, float),
    "boolean": bool, "array": list, "object": dict,
}

def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        expected = PYTHON_TYPES.get(TYPE_MAP.get(k, "string"), str)
        if not isinstance(obj[k], expected):
            errs.append(f"field {k} must be {TYPE_MAP.get(k)}, got {type(obj[k]).__name__}")
    return errs

VALID_FIX = {
    'call_id': 'x',
    'agent_version': 'x',
    'avg_handle_time_s': 1.0,
    'escalation_rate': 1.0,
    'p95_stt_ms': 1.0,
    'p95_llm_ms': 1.0,
    'p95_tts_ms': 1.0,
    'transcript_url': 'x',
}
INVALID_FIX = {}

def self_test():
    if validate(VALID_FIX):
        sys.stderr.write("valid fixture rejected\n"); return 1
    if not validate(INVALID_FIX):
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"json parse: {e}\n"); return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0

if __name__ == "__main__":
    sys.exit(main())
