#!/usr/bin/env python3
"""validate-llm-hallucination-test-patterns.py

Validate the artefact produced by the `llm-hallucination-test-patterns` methodology against the
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

REQUIRED = ["suite_version", "patterns", "per_pattern_cases", "rubric_refs", "gold_authors", "results"]


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


OK = json.loads(r"""{"suite_version": "1.1.0", "patterns": ["fact_probes", "grounding_required", "refusal_correctness", "citation_verification", "contradiction_tests", "off_topic_rejection"], "per_pattern_cases": {"fact_probes": ["fact_probes-000", "fact_probes-001", "fact_probes-002", "fact_probes-003", "fact_probes-004", "fact_probes-005", "fact_probes-006", "fact_probes-007", "fact_probes-008", "fact_probes-009"], "grounding_required": ["grounding_required-000", "grounding_required-001", "grounding_required-002", "grounding_required-003", "grounding_required-004", "grounding_required-005", "grounding_required-006", "grounding_required-007", "grounding_required-008", "grounding_required-009"], "refusal_correctness": ["refusal_correctness-000", "refusal_correctness-001", "refusal_correctness-002", "refusal_correctness-003", "refusal_correctness-004", "refusal_correctness-005", "refusal_correctness-006", "refusal_correctness-007", "refusal_correctness-008", "refusal_correctness-009"], "citation_verification": ["citation_verification-000", "citation_verification-001", "citation_verification-002", "citation_verification-003", "citation_verification-004", "citation_verification-005", "citation_verification-006", "citation_verification-007", "citation_verification-008", "citation_verification-009"], "contradiction_tests": ["contradiction_tests-000", "contradiction_tests-001", "contradiction_tests-002", "contradiction_tests-003", "contradiction_tests-004", "contradiction_tests-005", "contradiction_tests-006", "contradiction_tests-007", "contradiction_tests-008", "contradiction_tests-009"], "off_topic_rejection": ["off_topic_rejection-000", "off_topic_rejection-001", "off_topic_rejection-002", "off_topic_rejection-003", "off_topic_rejection-004", "off_topic_rejection-005", "off_topic_rejection-006", "off_topic_rejection-007", "off_topic_rejection-008", "off_topic_rejection-009"]}, "rubric_refs": {"fact_probes": "templates/rubric.yaml#fact_probes", "grounding_required": "templates/rubric.yaml#grounding_required", "refusal_correctness": "templates/rubric.yaml#refusal_correctness", "citation_verification": "templates/rubric.yaml#citation_verification", "contradiction_tests": "templates/rubric.yaml#contradiction_tests", "off_topic_rejection": "templates/rubric.yaml#off_topic_rejection"}, "gold_authors": {"fact_probes-000": "jane@team.io", "grounding_required-000": "jane@team.io", "refusal_correctness-000": "jane@team.io", "citation_verification-000": "jane@team.io", "contradiction_tests-000": "jane@team.io", "off_topic_rejection-000": "jane@team.io"}, "results": {"fact_probes": {"passed": 9, "failed": 1, "n": 10}, "grounding_required": {"passed": 9, "failed": 1, "n": 10}, "refusal_correctness": {"passed": 9, "failed": 1, "n": 10}, "citation_verification": {"passed": 9, "failed": 1, "n": 10}, "contradiction_tests": {"passed": 9, "failed": 1, "n": 10}, "off_topic_rejection": {"passed": 9, "failed": 1, "n": 10}}}""")
BAD = json.loads(r"""{"suite_version": "1.0.0", "patterns": ["fact_probes"], "per_pattern_cases": {"fact_probes": ["x", "y"]}}""")


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
