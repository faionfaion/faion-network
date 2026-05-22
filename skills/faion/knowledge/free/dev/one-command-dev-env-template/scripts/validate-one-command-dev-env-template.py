#!/usr/bin/env python3
"""validate-one-command-dev-env-template.py — validate a dev-env decision-record JSON.

Usage:
  validate-one-command-dev-env-template.py <record.json>
Flags: --help, --self-test
Exit: 0 ok, 1 violation, 2 usage/IO.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = (
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
)
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COLLAPSED_OWNERS = {"team", "we", "us", "engineering", "the team", "the squad", "the group"}


def _check(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errors.append(f"missing key: {k}")
    if errors:
        return errors
    if not SLUG_RE.match(doc["artefact_id"]):
        errors.append("artefact_id must be kebab-case")
    if str(doc["owner"]).strip().lower() in COLLAPSED_OWNERS:
        errors.append(f"owner is a collapsed plural; require a named human: {doc['owner']!r}")
    if len(str(doc["decision"])) < 4:
        errors.append("decision must be a non-trivial string")
    if len(str(doc["rationale"])) < 60:
        errors.append("rationale must be >= 60 chars and cite an input")

    inputs = doc["inputs_used"]
    if not isinstance(inputs, list) or not inputs:
        errors.append("inputs_used must be a non-empty array")
    for inp in inputs if isinstance(inputs, list) else []:
        if not inp.get("name") or not inp.get("source"):
            errors.append(f"inputs_used entry missing name/source: {inp}")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    fixture = {
        "artefact_id": "billing-dev-up",
        "owner": "ruslan@faion.net",
        "decision": "`make dev-up` -> docker compose up + scripts/bootstrap.sh + seed-fixtures.sh",
        "rationale": "Ticket eng-1234 logged 3-hour onboarding times because the steps were spread across three runbooks. scripts/bootstrap.sh already handles deps + migrations; wrapping in make gives one entry point.",
        "inputs_used": [
            {"name": "ticket-eng-1234", "source": "https://faion.net/tickets/eng-1234"},
            {"name": "scripts/bootstrap.sh", "source": "repo:scripts/bootstrap.sh"}
        ],
        "version": "1.0.0",
        "last_reviewed": "2026-05-22"
    }
    errs = _check(fixture)
    if errs:
        sys.stderr.write("self-test FAILED:\n" + "\n".join(errs) + "\n")
        return 1
    sys.stdout.write('{"self_test": "ok"}\n')
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-one-command-dev-env-template.py <record.json>\n")
        return 2
    try:
        doc = json.loads(Path(argv[1]).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"read/parse error: {exc}\n")
        return 2
    for k in [k for k in doc if k.startswith("_")]:
        doc.pop(k)
    errs = _check(doc)
    if errs:
        sys.stderr.write("violations:\n" + "\n".join(f" - {e}" for e in errs) + "\n")
        return 1
    sys.stdout.write(json.dumps({"ok": True}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
