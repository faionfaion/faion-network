#!/usr/bin/env python3
"""validate-terraform-modules-versioning.py — enforce the output contract for Terraform Modules — Versioning.

Stdlib-only. Implements minimal JSON Schema draft-07 checks tailored to this
methodology's contract (see ../content/02-output-contract.xml). Exit codes:

  0  artefact valid
  1  artefact invalid (violations listed on stdout)
  2  usage error / file not found

CLI:

  python validate-terraform-modules-versioning.py <artefact.json>      validate an artefact file
  python validate-terraform-modules-versioning.py --help               print help
  python validate-terraform-modules-versioning.py --self-test          run built-in fixture
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

SLUG = "terraform-modules-versioning"
EXPECTED_PRODUCES = "spec"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
KEBAB = re.compile(r"^[a-z][a-z0-9-]+$")
FORBIDDEN_OWNERS = {"team", "we", "us", ""}


def _required_keys(obj: dict) -> list[str]:
    required = [
        "artefact_id",
        "produces",
        "owner",
        "version",
        "last_reviewed",
        "inputs_used",
        "decision",
        "rationale",
        "trace_refs",
    ]
    return [k for k in required if k not in obj]


def validate(obj: dict) -> list[str]:
    """Return a list of human-readable violations. Empty list = valid."""
    violations: list[str] = []

    missing = _required_keys(obj)
    if missing:
        violations.append(f"missing required keys: {missing}")
        return violations

    if not isinstance(obj.get("artefact_id"), str) or not KEBAB.match(obj["artefact_id"]):
        violations.append("artefact_id must be kebab-case string")

    if obj.get("produces") != EXPECTED_PRODUCES:
        violations.append(
            f"produces must be {EXPECTED_PRODUCES!r}, got {obj.get('produces')!r}"
        )

    owner = obj.get("owner")
    if not isinstance(owner, str) or owner.strip().lower() in FORBIDDEN_OWNERS:
        violations.append("owner must be a named string (not 'team' / 'we' / 'us' / blank)")

    version = obj.get("version", "")
    if not isinstance(version, str) or not SEMVER.match(version):
        violations.append("version must match semver pattern X.Y.Z")

    last = obj.get("last_reviewed")
    try:
        last_date = datetime.strptime(last, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        violations.append("last_reviewed must be ISO date YYYY-MM-DD")
        last_date = None

    inputs = obj.get("inputs_used")
    if not isinstance(inputs, list) or not inputs:
        violations.append("inputs_used must be a non-empty list")
    else:
        for i, item in enumerate(inputs):
            if not isinstance(item, dict):
                violations.append(f"inputs_used[{i}] must be an object")
                continue
            if not item.get("name") or not item.get("source"):
                violations.append(f"inputs_used[{i}] must have name + source")

    decision = obj.get("decision")
    if not isinstance(decision, str) or not decision.strip():
        violations.append("decision must be non-empty string")

    rationale = obj.get("rationale", "")
    if not isinstance(rationale, str) or len(rationale) < 40:
        violations.append("rationale must be >=40 chars")
    else:
        names = []
        if isinstance(inputs, list):
            names = [i.get("name", "") for i in inputs if isinstance(i, dict)]
        if names and not any(n and n in rationale for n in names):
            violations.append("rationale must cite at least one inputs_used.name (rule r5)")

    refs = obj.get("trace_refs")
    if not isinstance(refs, list) or not refs:
        violations.append("trace_refs must be a non-empty list of strings")

    return violations


def _self_test() -> int:
    good = {
        "artefact_id": f"{SLUG}-smoke-test",
        "produces": EXPECTED_PRODUCES,
        "owner": "ruslan@faion.net",
        "version": "1.0.0",
        "last_reviewed": date.today().isoformat(),
        "inputs_used": [{"name": "smoke-input", "source": "file://./smoke-input"}],
        "decision": "Smoke-test fixture decision.",
        "rationale": (
            "Fixture exercises typed inputs, named owner, and traceable decision; "
            "cites smoke-input."
        ),
        "trace_refs": ["smoke-input"],
        "status": "draft",
    }
    bad = {
        "artefact_id": "X",
        "produces": "wrong-shape",
        "owner": "team",
        "version": "v1",
        "last_reviewed": "yesterday",
        "inputs_used": [],
        "decision": "",
        "rationale": "short",
        "trace_refs": [],
    }

    good_violations = validate(good)
    if good_violations:
        sys.stdout.write("self-test FAILED: good fixture rejected\n")
        for v in good_violations:
            sys.stdout.write(f"  - {v}\n")
        return 1

    bad_violations = validate(bad)
    if not bad_violations:
        sys.stdout.write("self-test FAILED: bad fixture accepted\n")
        return 1

    sys.stdout.write(
        f"self-test OK: good fixture passes; bad fixture has {len(bad_violations)} violations\n"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog=f"validate-{SLUG}.py",
        description=f"Validate {SLUG} output artefact against content/02-output-contract.xml.",
    )
    parser.add_argument("artefact", nargs="?", help="Path to JSON artefact to validate.")
    parser.add_argument(
        "--self-test", action="store_true", help="Run built-in fixture and exit."
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    if not args.artefact:
        parser.print_help()
        return 2

    path = Path(args.artefact)
    if not path.exists():
        sys.stdout.write(f"ERROR: file not found: {path}\n")
        return 2

    try:
        obj = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        sys.stdout.write(f"ERROR: invalid JSON: {exc}\n")
        return 1

    violations = validate(obj)
    if violations:
        sys.stdout.write(f"FAIL: {len(violations)} violation(s):\n")
        for v in violations:
            sys.stdout.write(f"  - {v}\n")
        return 1

    sys.stdout.write("OK: artefact valid (schema + forbidden-pattern checks pass)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
