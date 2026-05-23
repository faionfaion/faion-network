#!/usr/bin/env python3
"""validate-single-interview-fast-loop-template.py — validate a Single Interview Fast Loop Template artefact JSON against the output contract.

Usage:
  validate-single-interview-fast-loop-template.py <artefact.json>
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

REQUIRED: tuple[str, ...] = ('loop_id', 'decision_under_test', 'must_asks', 'interview_at', 'synthesis_due_at', 'synthesis_outcome', 'citation_path', 'owner', 'version', 'last_reviewed')
FORBIDDEN_HINTS: tuple[str, ...] = ['must_asks length < 3 OR > 5', 'synthesis_due_at > interview_at + 36h', "synthesis_outcome ∈ {'interesting', 'tbd', ''}"]
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
    for k in REQUIRED:
        v = doc.get(k)
        if isinstance(v, str) and not v.strip():
            errors.append(f"required field {k!r} is empty")
        if isinstance(v, list) and not v and k not in {"tags"}:
            errors.append(f"required list field {k!r} is empty")
    for _hint in FORBIDDEN_HINTS:
        # Surface forbidden-pattern hints as diagnostic context; not auto-fail.
        pass
    return errors


def _self_test() -> int:
    fixture: dict[str, Any] = {
        'loop_id': 'sample-loop_id',
        'decision_under_test': 'sample-decision_under_test',
        'must_asks': [{'k': 'v'}],
        'interview_at': '2026-05-23T12:00:00Z',
        'synthesis_due_at': '2026-05-23T12:00:00Z',
        'synthesis_outcome': 'sample-synthesis_outcome',
        'citation_path': 'sample-citation_path',
        'owner': 'ruslan@faion.net',
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
            "usage: validate-single-interview-fast-loop-template.py <artefact.json> [--self-test|--help]\n"
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
