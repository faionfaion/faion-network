#!/usr/bin/env python3
"""validate-qa-ac-to-assertion-mapping.py

Validate an ac-mapping artefact produced by the qa-ac-to-assertion-mapping
methodology against the JSON Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = json.loads('{"$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://faion.net/schemas/qa-ac-to-assertion-mapping.json", "type": "object", "required": ["story", "acceptance_criteria", "orphan_tests", "orphan_acs", "mapping_committed_at"], "properties": {"story": {"type": "object", "required": ["id", "url"]}, "acceptance_criteria": {"type": "array", "minItems": 1}, "orphan_tests": {"type": "array"}, "orphan_acs": {"type": "array", "maxItems": 0}, "mapping_committed_at": {"type": "string"}}}')
ASSERTION_CLASS = {"state", "output", "side_effect", "negative"}
STRUCTURAL_TOKENS = [
    r"\bwas called\b",
    r"\bhas been called\b",
    r"\btoHaveBeenCalled\b",
    r"\bno exception\b",
    r"\bdid not throw\b",
    r"^status 200$",
    r"\bspy called\b",
    r"^called$",
]


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in SCHEMA["required"]:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if isinstance(obj.get("story"), dict):
        for k in ("id", "url"):
            if k not in obj["story"]:
                errs.append(f"story.{k} missing")
    elif "story" in obj:
        errs.append("story must be object")
    acs = obj.get("acceptance_criteria")
    if not isinstance(acs, list) or len(acs) < 1:
        errs.append("acceptance_criteria must be a non-empty array")
    else:
        for i, ac in enumerate(acs):
            if not isinstance(ac, dict):
                errs.append(f"acceptance_criteria[{i}] not an object")
                continue
            for k in ("ac_id", "description", "tests"):
                if k not in ac:
                    errs.append(f"acceptance_criteria[{i}].{k} missing")
            tests = ac.get("tests")
            if not isinstance(tests, list) or len(tests) < 1:
                errs.append(f"acceptance_criteria[{i}].tests must be non-empty array")
                continue
            for j, t in enumerate(tests):
                if not isinstance(t, dict):
                    errs.append(f"acceptance_criteria[{i}].tests[{j}] not an object")
                    continue
                for k in ("file_path", "test_name", "asserted_behavior", "assertion_class"):
                    if k not in t:
                        errs.append(f"acceptance_criteria[{i}].tests[{j}].{k} missing")
                ab = t.get("asserted_behavior", "")
                if isinstance(ab, str):
                    if len(ab) < 20:
                        errs.append(f"acceptance_criteria[{i}].tests[{j}].asserted_behavior too short (<20 chars)")
                    for pat in STRUCTURAL_TOKENS:
                        if re.search(pat, ab, re.IGNORECASE):
                            errs.append(f"acceptance_criteria[{i}].tests[{j}].asserted_behavior matches structural token: {pat}")
                            break
                cls = t.get("assertion_class")
                if cls is not None and cls not in ASSERTION_CLASS:
                    errs.append(f"acceptance_criteria[{i}].tests[{j}].assertion_class not in {sorted(ASSERTION_CLASS)}")
    if "orphan_acs" in obj:
        if not isinstance(obj["orphan_acs"], list):
            errs.append("orphan_acs must be array")
        elif len(obj["orphan_acs"]) > 0:
            errs.append("orphan_acs must be empty (every AC must be mapped)")
    if "orphan_tests" in obj and not isinstance(obj["orphan_tests"], list):
        errs.append("orphan_tests must be array")
    if "mapping_committed_at" in obj and not isinstance(obj["mapping_committed_at"], str):
        errs.append("mapping_committed_at must be string")
    return errs


def self_test() -> int:
    good = {
        "story": {"id": "STORY-1", "url": "https://issues.example.com/STORY-1"},
        "acceptance_criteria": [
            {
                "ac_id": "AC-1",
                "description": "user can submit valid form",
                "tests": [
                    {
                        "file_path": "tests/signup.spec.ts",
                        "test_name": "submits valid form and persists user",
                        "asserted_behavior": "response status 201 AND db.users row exists with expected email",
                        "assertion_class": "state",
                    }
                ],
            }
        ],
        "orphan_tests": [],
        "orphan_acs": [],
        "mapping_committed_at": "2026-05-23T10:00:00Z",
    }
    errs = validate(good)
    if errs:
        sys.stderr.write("self-test: good fixture rejected: " + json.dumps(errs) + "\n")
        return 1
    bad = {
        "story": {"id": "STORY-1"},
        "acceptance_criteria": [
            {
                "ac_id": "AC-1",
                "description": "x",
                "tests": [
                    {
                        "file_path": "t.ts",
                        "test_name": "calls api",
                        "asserted_behavior": "spy called",
                        "assertion_class": "called",
                    }
                ],
            }
        ],
        "orphan_acs": ["AC-2"],
    }
    if not validate(bad):
        sys.stderr.write("self-test: bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
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
