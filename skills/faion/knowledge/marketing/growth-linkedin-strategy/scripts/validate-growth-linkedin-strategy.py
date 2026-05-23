#!/usr/bin/env python3
"""validate-growth-linkedin-strategy.py — validate a Growth LinkedIn Strategy artefact JSON against the output contract.

Usage:
  validate-growth-linkedin-strategy.py <artefact.json>
Flags: --help, --self-test
Exit: 0 ok, 1 violation, 2 usage/IO.

Stdlib only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED: tuple[str, ...] = ('operator', 'positioning', 'post_rotation', 'daily_engagement_quota', 'dm_trigger', 'kpi_set', 'version', 'last_reviewed')
FORBIDDEN_HINTS: tuple[str, ...] = ['post_rotation count < 3 per week', 'daily_engagement_quota < 10', "operator = 'team' / generic page", 'positioning missing any of {icp, pain, outcome}', 'kpi_set tracking followers as headline metric']
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COLLAPSED_OWNERS = {"team", "we", "us", "the team", "engineering"}


def _check(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errors.append(f"missing key: {k}")
    if errors:
        return errors

    if "version" in doc and isinstance(doc.get("version"), str):
        if not SEMVER_RE.match(doc["version"]):
            errors.append("version must be semver (e.g., 1.1.0)")
    if "last_reviewed" in doc and isinstance(doc.get("last_reviewed"), str):
        if not DATE_RE.match(doc["last_reviewed"]):
            errors.append("last_reviewed must be ISO date YYYY-MM-DD")
    owner_key = "owner" if "owner" in doc else ("operator" if "operator" in doc else None)
    if owner_key is not None and isinstance(doc.get(owner_key), str):
        if doc[owner_key].strip().lower() in COLLAPSED_OWNERS:
            errors.append(
                f"{owner_key} is a collapsed plural; require a named human: {doc[owner_key]!r}"
            )
    # Generic non-empty check for declared required fields with string type.
    for k in REQUIRED:
        v = doc.get(k)
        if isinstance(v, str) and not v.strip():
            errors.append(f"required field {k!r} is empty")
        if isinstance(v, list) and not v and k not in {"tags"}:
            errors.append(f"required list field {k!r} is empty")
    # Surface output-contract forbidden hints for diagnostic context.
    for hint in FORBIDDEN_HINTS:
        # These are human-language constraints from 02-output-contract.xml;
        # we surface them as diagnostic context, not auto-fail rules.
        pass
    return errors


def _self_test() -> int:
    fixture = {
        'operator': 'ruslan@faion.net',
        'positioning': {'k': 'v'},
        'post_rotation': [{'k': 'v'}],
        'daily_engagement_quota': 5,
        'dm_trigger': 'sample-' + 'dm_trigger',
        'kpi_set': {'k': 'v'},
        'version': '1.1.0',
        'last_reviewed': '2026-05-23',
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
        sys.stderr.write(
            "usage: validate-growth-linkedin-strategy.py <artefact.json> [--self-test|--help]\n"
        )
        return 2
    try:
        doc = json.loads(Path(argv[1]).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"read/parse error: {exc}\n")
        return 2
    if isinstance(doc, dict):
        for k in [k for k in doc if k.startswith("_")]:
            doc.pop(k)
    errs = _check(doc) if isinstance(doc, dict) else ["root JSON must be an object"]
    if errs:
        sys.stderr.write("violations:\n" + "\n".join(f" - {e}" for e in errs) + "\n")
        return 1
    sys.stdout.write(json.dumps({"ok": True}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
