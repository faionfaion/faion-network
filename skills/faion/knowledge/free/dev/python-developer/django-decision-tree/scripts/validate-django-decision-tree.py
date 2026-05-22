#!/usr/bin/env python3
"""validate-django-decision-tree.py — validate a Django architecture decision-record JSON.

Usage:
  validate-django-decision-tree.py <record.json>
Flags: --help, --self-test
Exit: 0 ok, 1 violation, 2 usage/IO.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = ("artefact_id", "owner", "project", "signals", "decisions", "dependencies", "version", "last_reviewed")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DECISION_KEYS = ("framework", "api_stack", "layering", "db", "deployment")


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

    s = doc["signals"]
    d = doc["decisions"]
    rats = (d.get("rationales") or {})

    if d.get("framework") == "fastapi" and s.get("needs_admin"):
        errors.append("framework=fastapi forbidden when needs_admin=true")
    if d.get("layering") == "clean-arch" and s.get("model_count", 0) < 10:
        errors.append("layering=clean-arch forbidden for model_count < 10")
    if d.get("layering") == "simple" and s.get("model_count", 0) >= 50:
        errors.append("layering=simple forbidden for model_count >= 50")

    for k in DECISION_KEYS:
        if not d.get(k):
            errors.append(f"decisions.{k} missing")
        if len(str(rats.get(k) or "")) < 20:
            errors.append(f"decisions.rationales.{k} too short")

    for dep in doc["dependencies"]:
        a = dep.get("audit") or {}
        if dep.get("verdict") == "adopt":
            if not a.get("recent_commits") or not a.get("no_known_cves") or not a.get("django_compat") or not a.get("license_ok"):
                errors.append(f"dependency {dep.get('name')!r} verdict=adopt with failing audit signals")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "arch-decision-record.json"
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
        sys.stderr.write("usage: validate-django-decision-tree.py <record.json>\n")
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
