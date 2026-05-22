#!/usr/bin/env python3
"""validate-django-quality-linting.py — validate a Django quality stack spec JSON."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = (
    "artefact_id",
    "owner",
    "django_version",
    "python_version",
    "ruff",
    "mypy",
    "pre_commit_hooks",
    "ci_gates",
    "coverage_threshold",
    "version",
    "last_reviewed",
)
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQ_CI = ("ruff", "mypy", "manage.py check --deploy", "coverage")


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

    if not doc["ruff"].get("exclude_migrations"):
        errors.append("ruff.exclude_migrations must be true")

    if not doc["mypy"].get("django_settings_module"):
        errors.append("mypy.django_settings_module must be non-empty")

    for h in doc["pre_commit_hooks"]:
        if h.get("stage") == "commit" and not h.get("fast"):
            errors.append(f"pre-commit hook {h.get('name')!r}: stage=commit requires fast=true")

    ci_text = " ".join(doc["ci_gates"]).lower()
    for req in REQ_CI:
        if req.lower() not in ci_text:
            errors.append(f"ci_gates must include something containing {req!r}")

    if int(doc.get("coverage_threshold", 0)) < 80:
        errors.append("coverage_threshold must be >= 80")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "quality-spec.json"
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
        sys.stderr.write("usage: validate-django-quality-linting.py <spec.json>\n")
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
