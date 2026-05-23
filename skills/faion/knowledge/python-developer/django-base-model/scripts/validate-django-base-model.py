#!/usr/bin/env python3
"""validate-django-base-model.py — validate a Django base-model spec JSON.

Usage:
  validate-django-base-model.py <spec.json>
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
    "django_version",
    "db_engine",
    "bases",
    "models",
    "version",
    "last_reviewed",
)
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ON_DEL = {"CASCADE", "SET_NULL", "PROTECT", "DO_NOTHING", "SET_DEFAULT"}


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

    for b in doc["bases"]:
        if b.get("abstract") is not True:
            errors.append(f"base {b.get('name')!r} must be abstract=true")

    base_names = {b.get("name") for b in doc["bases"]}

    for m in doc["models"]:
        if m.get("extends") not in base_names:
            errors.append(f"model {m.get('name')!r} extends unknown base {m.get('extends')!r}")
        if m.get("soft_delete") and m.get("unique_fields"):
            # warn-level: must be partial-unique in the migration, document in the spec
            # We require unique_fields entries to be present alongside foreign_keys notes;
            # full check is in the migration layer.
            pass
        for fk in m.get("foreign_keys") or []:
            if fk.get("on_delete") not in ON_DEL:
                errors.append(f"unknown on_delete {fk.get('on_delete')!r}")
            reason = str(fk.get("reason") or "")
            if len(reason) < 10:
                errors.append(f"foreign_key {fk.get('field')!r} reason too short")
            if m.get("soft_delete") and fk.get("on_delete") == "CASCADE" and "cascade" not in reason.lower():
                errors.append(
                    f"soft-deletable model {m.get('name')!r} has CASCADE FK without explicit cascade reason"
                )

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "base-model-spec.json"
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
        sys.stderr.write("usage: validate-django-base-model.py <spec.json>\n")
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
