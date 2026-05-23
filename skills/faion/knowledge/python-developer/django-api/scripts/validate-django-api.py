#!/usr/bin/env python3
"""validate-django-api.py — validate a Django REST API spec JSON against the methodology contract.

Usage:
  validate-django-api.py <spec.json>
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
    "framework",
    "django_version",
    "endpoints",
    "auth",
    "throttle",
    "version",
    "last_reviewed",
)
REQ_SCOPES = {"anon", "user", "burst", "login"}
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

    for e in doc["endpoints"]:
        if e.get("input_serializer") == e.get("output_serializer"):
            errors.append(f"endpoint {e.get('resource')!r}: input/output serializer must differ")
        if any(p.lower() == "allowany" for p in e.get("permission_classes") or []):
            errors.append(f"endpoint {e.get('resource')!r}: AllowAny forbidden as default")

    auth = doc["auth"]
    if auth.get("access_ttl_minutes", 999) > 15:
        errors.append("auth.access_ttl_minutes must be <= 15")
    if not auth.get("rotate_refresh"):
        errors.append("auth.rotate_refresh must be true")
    if not auth.get("blacklist_after_rotation"):
        errors.append("auth.blacklist_after_rotation must be true")

    scopes = set(doc["throttle"].get("scopes") or [])
    if not REQ_SCOPES.issubset(scopes):
        errors.append(f"throttle.scopes must include all of {REQ_SCOPES}; got {scopes}")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "api-spec.json"
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
        sys.stderr.write("usage: validate-django-api.py <spec.json>\n")
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
