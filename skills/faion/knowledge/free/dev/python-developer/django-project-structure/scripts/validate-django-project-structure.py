#!/usr/bin/env python3
"""validate-django-project-structure.py — validate a Django layout spec JSON.

Usage:
  validate-django-project-structure.py <spec.json>
Flags: --help, --self-test
Exit: 0 ok, 1 violation, 2 usage/IO.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = ("artefact_id", "owner", "project", "django_version", "apps", "core_modules", "config_modules", "test_root", "version", "last_reviewed")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
APP_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
REQ_APP_FILES = ("services.py", "selectors.py", "apis.py", "models.py", "constants.py", "admin.py")
REQ_CONFIG = ("base.py", "dev.py", "prod.py", "urls.py")


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

    for a in doc["apps"]:
        if not APP_NAME_RE.match(a.get("name", "")):
            errors.append(f"app name not snake_case: {a.get('name')!r}")
        files = a.get("files") or []
        for req in REQ_APP_FILES:
            if not any(req in f for f in files):
                errors.append(f"app {a.get('name')!r} missing required file {req}")

    cms = doc["config_modules"]
    for req in REQ_CONFIG:
        if not any(req in c for c in cms):
            errors.append(f"config_modules missing {req}")

    for cm in doc["core_modules"]:
        if cm.startswith("apps.") or "apps/" in cm:
            errors.append(f"core_modules entry references apps/: {cm!r}")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "layout-spec.json"
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
        sys.stderr.write("usage: validate-django-project-structure.py <spec.json>\n")
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
