#!/usr/bin/env python3
"""validate-ai-coding-of-qualitative-data-protocol.py

Validate the artefact produced by the ai-coding-of-qualitative-data-protocol methodology against the
JSON Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in valid + invalid fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['codebook_version', 'coded_segments', 'kappa', 'coders']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'codebook_version': 'v1.2.0', 'coded_segments': [{'segment_id': 's000', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's001', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's002', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's003', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's004', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's005', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's006', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's007', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's008', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's009', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's010', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's011', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's012', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's013', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's014', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's015', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's016', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's017', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's018', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}, {'segment_id': 's019', 'code_ids': ['pain.auth'], 'coder': 'ai-claude-sonnet', 'timestamp': '2026-05-20T10:00:00Z'}], 'kappa': 0.78, 'coders': ['ai-claude-sonnet', 'ruslan@faion.net']}
BAD = {'codebook_version': '1', 'coded_segments': []}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: valid example rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: invalid example accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except Exception as exc:
        sys.stderr.write(f"unreadable JSON: {exc}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
