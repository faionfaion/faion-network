#!/usr/bin/env python3
"""validate-foreign-client-etiquette-playbook.py

Validate a Foreign Client Etiquette Playbook artefact against the output-contract schema declared in
`content/02-output-contract.xml`. Stdlib-only.

Inputs:
    --file PATH       path to artefact JSON (or front-matter-style key:value MD)
    --self-test       run built-in fixtures (ok + bad)
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["artefact_id", "owner", "decision", "rationale", "inputs_used", "version", "last_reviewed"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_PAT = re.compile(r"^[a-z][a-z0-9-]+$")
PLURAL_OWNER = re.compile(r"^(team|we|us|everyone|all)$", re.IGNORECASE)


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    if isinstance(obj.get("artefact_id"), str) and not ID_PAT.match(obj["artefact_id"]):
        errs.append("artefact_id must match ^[a-z][a-z0-9-]+$")
    if isinstance(obj.get("owner"), str) and PLURAL_OWNER.match(obj["owner"].strip()):
        errs.append("owner is plural pronoun; rule r3-named-owner requires a named human or role")
    if isinstance(obj.get("version"), str) and not SEMVER.match(obj["version"]):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if isinstance(obj.get("last_reviewed"), str) and not DATE.match(obj["last_reviewed"]):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    iu = obj.get("inputs_used")
    if isinstance(iu, list):
        if not iu:
            errs.append("inputs_used must be non-empty")
        else:
            for i, row in enumerate(iu):
                if not isinstance(row, dict):
                    errs.append(f"inputs_used[{i}] must be object")
                    continue
                if not row.get("name") or not row.get("source"):
                    errs.append(f"inputs_used[{i}] missing name or source")
    rationale = obj.get("rationale", "")
    if isinstance(rationale, str) and len(rationale) < 40:
        errs.append("rationale too short (< 40 chars); cite at least one input by name")
    return errs


OK = {
    "artefact_id": "foreign-client-etiquette-playbook-smoke-2026q2",
    "owner": "ops@example.com",
    "decision": "Apply Foreign Client Etiquette Playbook to the smoke-test scope.",
    "rationale": "Smoke-test fixture references smoke-input.yaml; serves to exercise the validator end-to-end.",
    "inputs_used": [{"name": "smoke-input", "source": "repo://fixtures/smoke-input.yaml"}],
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "status": "active",
}
BAD = {
    "artefact_id": "X",
    "owner": "team",
    "decision": "ok",
    "rationale": "obviously needed",
    "inputs_used": [],
    "version": "v1",
    "last_reviewed": "soon",
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("OK fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
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
        obj = json.loads(p.read_text(encoding="utf-8"))
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
