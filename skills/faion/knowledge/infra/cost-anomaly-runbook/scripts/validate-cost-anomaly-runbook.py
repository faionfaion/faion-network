#!/usr/bin/env python3
"""validate-cost-anomaly-runbook.py — validate artefact produced by the cost-anomaly-runbook methodology.

Validates against the schema declared in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON (or YAML if PyYAML present)
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage error / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
]

OWNER_FORBIDDEN_PATTERNS = [
    r"^team$",
    r"^we$",
    r"^us$",
    r"^everyone$",
    r"^engineering$",
    r"^\s*$",
]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED_FIELDS:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v is None or (isinstance(v, str) and not v.strip()):
            errs.append(f"empty value for required field: {k}")
    if "owner" in obj and isinstance(obj["owner"], str):
        for pat in OWNER_FORBIDDEN_PATTERNS:
            if re.match(pat, obj["owner"].strip(), re.IGNORECASE):
                errs.append("owner is plural / generic — single named handle required")
                break
    if "version" in obj and isinstance(obj["version"], str):
        if not re.match(r"^\d+\.\d+\.\d+$", obj["version"]):
            errs.append("version is not semver (X.Y.Z)")
    if "last_reviewed" in obj and isinstance(obj["last_reviewed"], str):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", obj["last_reviewed"]):
            errs.append("last_reviewed must be ISO-8601 date YYYY-MM-DD")
    if "inputs_used" in obj:
        if not isinstance(obj["inputs_used"], list):
            errs.append("inputs_used must be a list")
        elif not obj["inputs_used"] and obj.get("decision") not in (None, "no-op"):
            errs.append("inputs_used is empty AND decision is not 'no-op'")
    if "rationale" in obj and isinstance(obj["rationale"], str):
        if len(obj["rationale"].split()) < 8:
            errs.append("rationale is shorter than 2 sentences (heuristic: < 8 words)")
    return errs


OK_FIXTURE = {
    "artefact_id": "cost-anomaly-runbook-2026-05-23-001",
    "owner": "ruslan@faion.net",
    "decision": "apply",
    "rationale": "The input artefact `inputs/spec.md` matches the Applies-If preconditions and the named owner is accountable.",
    "inputs_used": ["inputs/spec.md"],
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

BAD_FIXTURE = {
    "artefact_id": "cost-anomaly-runbook-bad",
    "owner": "team",
    "decision": "apply",
    "rationale": "obvious",
    "inputs_used": [],
    "version": "1",
    "last_reviewed": "yesterday",
}


def self_test() -> int:
    ok_errs = validate(OK_FIXTURE)
    if ok_errs:
        sys.stderr.write(f"OK fixture rejected: {ok_errs}\n")
        return 1
    bad_errs = validate(BAD_FIXTURE)
    if not bad_errs:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write(f"self-test OK ({len(bad_errs)} violations on bad fixture)\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate Cost Anomaly Runbook artefact",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON file")
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
        sys.stderr.write(f"JSON parse error: {e}\n")
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
