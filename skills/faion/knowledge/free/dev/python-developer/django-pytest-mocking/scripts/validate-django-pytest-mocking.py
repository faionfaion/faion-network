#!/usr/bin/env python3
"""validate-django-pytest-mocking.py — validate a mocking spec JSON."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = ("artefact_id", "owner", "boundaries", "anti_mocks", "version", "last_reviewed")
REQ_ANTI = {"django-orm", "time-sleep"}
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ASSERT_KEYWORDS = ("assert_called", "responses.calls", "is_valid", "len(responses")


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

    for b in doc["boundaries"]:
        tech = b.get("technique")
        if tech == "unittest-mock-patch":
            tgt = str(b.get("patch_target") or "")
            if not tgt.startswith("apps."):
                errors.append(f"boundary {b.get('name')!r}: unittest-mock-patch target must be at consumer's apps.* import path; got {tgt!r}")
        asserts = b.get("asserts") or []
        if not any(any(kw in a for kw in ASSERT_KEYWORDS) for a in asserts):
            errors.append(f"boundary {b.get('name')!r}: asserts must verify the call happened (assert_called* / responses.calls), not only return value")

    anti = set(doc["anti_mocks"] or [])
    if not REQ_ANTI.issubset(anti):
        errors.append(f"anti_mocks must include {REQ_ANTI}; got {anti}")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "mocking-spec.json"
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
        sys.stderr.write("usage: validate-django-pytest-mocking.py <spec.json>\n")
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
