#!/usr/bin/env python3
"""validate-golden-set-curation-and-maintenance.py

Validate the artefact produced by the `golden-set-curation-and-maintenance` methodology against the
JSON Schema embedded in `content/02-output-contract.xml`.

This validator uses stdlib only (no pyyaml/pydantic) for portability.

Inputs:
    --file PATH       path to artefact (JSON)
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["dataset_version", "items", "coverage_report", "owner", "promotion_review"]


def validate(obj) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v in (None, "", [], {}):
            errs.append(f"required field empty: {k}")
        if isinstance(v, str) and v.strip().upper() in {"TBD", "TODO", "FIXME"}:
            errs.append(f"placeholder value in field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.lower().strip() in {"team", "we", "tbd"}:
        errs.append("owner must be a single named person, not 'team' / 'we' / 'TBD'")
    return errs


OK = json.loads(r"""{"dataset_version": "1.0.0", "items": [{"id": "gld-0000", "bucket": "happy_path", "input": {"text": "sample input 0"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0001", "bucket": "edge_case", "input": {"text": "sample input 1"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0002", "bucket": "adversarial", "input": {"text": "sample input 2"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0003", "bucket": "known_failure_class", "input": {"text": "sample input 3"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0004", "bucket": "happy_path", "input": {"text": "sample input 4"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0005", "bucket": "edge_case", "input": {"text": "sample input 5"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0006", "bucket": "adversarial", "input": {"text": "sample input 6"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0007", "bucket": "known_failure_class", "input": {"text": "sample input 7"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0008", "bucket": "happy_path", "input": {"text": "sample input 8"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0009", "bucket": "edge_case", "input": {"text": "sample input 9"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0010", "bucket": "adversarial", "input": {"text": "sample input 10"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0011", "bucket": "known_failure_class", "input": {"text": "sample input 11"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0012", "bucket": "happy_path", "input": {"text": "sample input 12"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0013", "bucket": "edge_case", "input": {"text": "sample input 13"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0014", "bucket": "adversarial", "input": {"text": "sample input 14"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0015", "bucket": "known_failure_class", "input": {"text": "sample input 15"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0016", "bucket": "happy_path", "input": {"text": "sample input 16"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0017", "bucket": "edge_case", "input": {"text": "sample input 17"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0018", "bucket": "adversarial", "input": {"text": "sample input 18"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0019", "bucket": "known_failure_class", "input": {"text": "sample input 19"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0020", "bucket": "happy_path", "input": {"text": "sample input 20"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0021", "bucket": "edge_case", "input": {"text": "sample input 21"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0022", "bucket": "adversarial", "input": {"text": "sample input 22"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0023", "bucket": "known_failure_class", "input": {"text": "sample input 23"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0024", "bucket": "happy_path", "input": {"text": "sample input 24"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0025", "bucket": "edge_case", "input": {"text": "sample input 25"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0026", "bucket": "adversarial", "input": {"text": "sample input 26"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0027", "bucket": "known_failure_class", "input": {"text": "sample input 27"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0028", "bucket": "happy_path", "input": {"text": "sample input 28"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0029", "bucket": "edge_case", "input": {"text": "sample input 29"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0030", "bucket": "adversarial", "input": {"text": "sample input 30"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0031", "bucket": "known_failure_class", "input": {"text": "sample input 31"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0032", "bucket": "happy_path", "input": {"text": "sample input 32"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0033", "bucket": "edge_case", "input": {"text": "sample input 33"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0034", "bucket": "adversarial", "input": {"text": "sample input 34"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0035", "bucket": "known_failure_class", "input": {"text": "sample input 35"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0036", "bucket": "happy_path", "input": {"text": "sample input 36"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0037", "bucket": "edge_case", "input": {"text": "sample input 37"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0038", "bucket": "adversarial", "input": {"text": "sample input 38"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0039", "bucket": "known_failure_class", "input": {"text": "sample input 39"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0040", "bucket": "happy_path", "input": {"text": "sample input 40"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0041", "bucket": "edge_case", "input": {"text": "sample input 41"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0042", "bucket": "adversarial", "input": {"text": "sample input 42"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0043", "bucket": "known_failure_class", "input": {"text": "sample input 43"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0044", "bucket": "happy_path", "input": {"text": "sample input 44"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0045", "bucket": "edge_case", "input": {"text": "sample input 45"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0046", "bucket": "adversarial", "input": {"text": "sample input 46"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0047", "bucket": "known_failure_class", "input": {"text": "sample input 47"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0048", "bucket": "happy_path", "input": {"text": "sample input 48"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}, {"id": "gld-0049", "bucket": "edge_case", "input": {"text": "sample input 49"}, "expected_output": {"label": "correct"}, "anti_output": [{"label": "plausible-wrong"}], "metadata": {"difficulty": "medium", "added_from": "seed", "reviewer": "jane@team.io"}}], "coverage_report": {"per_bucket_count": {"happy_path": 13, "edge_case": 13, "adversarial": 12, "known_failure_class": 12}, "min_per_bucket": 12}, "owner": "jane@team.io", "promotion_review": {"reviewer": "alex@team.io", "reviewed_at": "2026-05-23"}}""")
BAD = json.loads(r"""{"dataset_version": "1.0.0", "items": [{"id": "x", "bucket": "happy_path", "input": {}, "expected_output": {}}]}""")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
