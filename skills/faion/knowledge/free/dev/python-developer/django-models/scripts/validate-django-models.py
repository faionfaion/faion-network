#!/usr/bin/env python3
"""validate-django-models.py — validate a Django models spec JSON.

Usage:
  validate-django-models.py <spec.json>
Flags: --help, --self-test
Exit: 0 ok, 1 violation, 2 usage/IO.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = ("artefact_id", "owner", "django_version", "db_engine", "app", "models", "version", "last_reviewed")
USER_LIKE = {"User", "Customer", "Account", "Member"}
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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

    db_engine = doc["db_engine"]
    for m in doc["models"]:
        if m.get("extends") == "models.Model":
            errors.append(f"model {m.get('name')!r} extends models.Model directly; use BaseModel")
        for f in m.get("fields", []):
            if f.get("db_index") and len(str(f.get("db_index_reason") or "")) < 10:
                errors.append(f"field {f.get('name')!r}: db_index requires reason >= 10 chars")
        for fk in m.get("foreign_keys") or []:
            reason = str(fk.get("reason") or "")
            if fk.get("on_delete") == "CASCADE":
                to = str(fk.get("to") or "")
                target_model = to.split(".")[-1]
                if target_model in USER_LIKE:
                    errors.append(f"FK {fk.get('field')!r} CASCADE on user-like {to!r}; choose PROTECT or SET_NULL")
            if len(reason) < 10:
                errors.append(f"FK {fk.get('field')!r}: reason too short")
        for c in m.get("constraints", []):
            if c.get("condition") and db_engine != "postgresql":
                errors.append(f"constraint {c.get('name')!r}: partial condition requires PostgreSQL; engine is {db_engine!r}")
        if m.get("is_pii") and m.get("soft_delete"):
            errors.append(f"model {m.get('name')!r}: is_pii=true and soft_delete=true conflict (GDPR requires hard delete)")
        if not m.get("full_clean_in_service"):
            errors.append(f"model {m.get('name')!r}: full_clean_in_service must be true")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "models-spec.json"
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
        sys.stderr.write("usage: validate-django-models.py <spec.json>\n")
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
