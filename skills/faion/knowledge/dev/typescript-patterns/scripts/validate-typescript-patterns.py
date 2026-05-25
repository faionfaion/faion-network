#!/usr/bin/env python3
"""validate-typescript-patterns.py — validate a typed-shapes spec JSON.

Usage:
  validate-typescript-patterns.py <spec.json>
Flags: --help, --self-test
Exit: 0 ok, 1 violation, 2 usage/IO.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = ("artefact_id", "owner", "scope", "ts_version", "types", "version", "last_reviewed")
KINDS = {"external-input", "internal", "id-brand", "result", "config"}
REPRS = {"interface", "zod-schema", "discriminated-union", "branded-string", "branded-number"}
VALIDS = {"zod-parse", "zod-safe-parse", "type-guard", "assertion-fn", "none"}
EXT_VALID = {"zod-parse", "zod-safe-parse"}

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")


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
    types = doc["types"]
    if not isinstance(types, list) or not types:
        errors.append("types must be a non-empty array")
    for t in types if isinstance(types, list) else []:
        if not NAME_RE.match(t.get("name", "")):
            errors.append(f"type name must be PascalCase: {t.get('name')!r}")
        if t.get("kind") not in KINDS:
            errors.append(f"unknown kind: {t.get('kind')!r}")
        if t.get("representation") not in REPRS:
            errors.append(f"unknown representation: {t.get('representation')!r}")
        v = t.get("validation")
        if v is not None and v not in VALIDS:
            errors.append(f"unknown validation: {v!r}")
        if t.get("kind") == "external-input" and (v not in EXT_VALID):
            errors.append(f"external-input {t['name']!r} requires validation in {EXT_VALID}; got {v!r}")
        if t.get("representation") == "discriminated-union" and not t.get("discriminator"):
            errors.append(f"discriminated-union {t['name']!r} missing discriminator")
    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "typed-shapes-spec.json"
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
        sys.stderr.write("usage: validate-typescript-patterns.py <spec.json>\n")
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
