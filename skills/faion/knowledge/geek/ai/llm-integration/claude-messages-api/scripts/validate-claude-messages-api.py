#!/usr/bin/env python3
"""validate-claude-messages-api.py — validate output JSON against the methodology output contract.

Inputs:
  - path to a JSON file produced by the methodology

Outputs:
  - stdout: human-readable violation list (empty on pass)
  - exit 0 on pass, 1 on schema violations, 2 on usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["stop_reason_centralised", "max_tokens_explicit", "multimodal_image_first", "pdf_preflight_check", "metadata_user_id", "streaming_delta_aware", "model_id", "forbidden_seen"]


def validate(doc: dict) -> list:
    errs = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    if not doc.get('stop_reason_centralised'):
        errs.append('stop_reason_centralised' + ' must be true')
    if not doc.get('max_tokens_explicit'):
        errs.append('max_tokens_explicit' + ' must be true')
    if not doc.get('multimodal_image_first'):
        errs.append('multimodal_image_first' + ' must be true')
    if not doc.get('pdf_preflight_check'):
        errs.append('pdf_preflight_check' + ' must be true')
    if not doc.get('metadata_user_id'):
        errs.append('metadata_user_id' + ' must be true')
    if not doc.get('streaming_delta_aware'):
        errs.append('streaming_delta_aware' + ' must be true')
    fs = doc.get("forbidden_seen")
    if not isinstance(fs, list):
        errs.append("forbidden_seen must be an array")
    elif fs:
        errs.append(f"forbidden_seen non-empty: {fs}")
    return errs


SMOKE = {'stop_reason_centralised': True, 'max_tokens_explicit': True, 'multimodal_image_first': True, 'pdf_preflight_check': True, 'metadata_user_id': True, 'streaming_delta_aware': True, 'model_id': 'claude-sonnet-4-20250514', 'forbidden_seen': []}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate claude-messages-api output JSON.")
    parser.add_argument("path", nargs="?", help="Path to JSON output to validate.")
    parser.add_argument("--self-test", action="store_true", help="Run an in-process smoke test.")
    args = parser.parse_args()

    if args.self_test:
        errs = validate(SMOKE)
        if errs:
            sys.stderr.write(f"self-test failed: {errs}\n")
            return 1
        sys.stdout.write("self-test ok\n")
        return 0

    if not args.path:
        parser.print_help()
        return 2

    p = Path(args.path)
    if not p.exists():
        sys.stderr.write(f"file not found: {p}\n")
        return 2

    try:
        doc = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError) as e:
        sys.stderr.write(f"json parse error: {e}\n")
        return 1

    errs = validate(doc)
    if errs:
        for e in errs:
            sys.stdout.write(e + "\n")
        return 1
    sys.stdout.write("ok\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
