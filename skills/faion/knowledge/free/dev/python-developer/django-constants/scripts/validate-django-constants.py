#!/usr/bin/env python3
"""validate-django-constants.py — validate a per-app constants spec JSON.

Usage:
  validate-django-constants.py <spec.json>
Flags: --help, --self-test
Exit: 0 ok, 1 violation, 2 usage/IO.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = ("artefact_id", "owner", "app", "django_version", "enums", "limits", "version", "last_reviewed")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PASCAL_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
UPPER_SNAKE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def _check(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errors.append(f"missing key: {k}")
    if errors:
        return errors
    if not SLUG_RE.match(doc["artefact_id"]):
        errors.append("artefact_id must be kebab-case")
    if str(doc["owner"]).strip().lower() in {"", "team", "we", "us"}:
        errors.append("owner must be a single named person")

    for e in doc["enums"]:
        if not PASCAL_RE.match(e.get("name", "")):
            errors.append(f"enum name must be PascalCase: {e.get('name')!r}")
        if e.get("kind") not in {"TextChoices", "IntegerChoices"}:
            errors.append(f"unknown enum kind: {e.get('kind')!r}")
        members = e.get("members") or []
        if len(members) < 2:
            errors.append(f"enum {e.get('name')!r} must have at least 2 members")
        for m in members:
            if not UPPER_SNAKE_RE.match(m.get("name", "")):
                errors.append(f"member name not UPPER_SNAKE: {m.get('name')!r}")

    for li in doc["limits"]:
        if not UPPER_SNAKE_RE.match(li.get("name", "")):
            errors.append(f"limit name not UPPER_SNAKE: {li.get('name')!r}")
        if len(str(li.get("rationale") or "")) < 10:
            errors.append(f"limit {li.get('name')!r} rationale too short")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "constants-spec.json"
    doc = json.loads(p.read_text())
    for k in [k for k in doc if k.startswith("_")]:
        doc.pop(k)
    errs = _check(doc)
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
        sys.stderr.write("usage: validate-django-constants.py <spec.json>\n")
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
