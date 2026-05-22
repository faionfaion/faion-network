#!/usr/bin/env python3
"""validate-typescript-react-2026.py — validate an App-Router spec JSON.

Usage:
  validate-typescript-react-2026.py <spec.json>
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
    "app_name",
    "next_version",
    "react_version",
    "ts_version",
    "routes",
    "actions",
    "tsconfig_flags",
    "version",
    "last_reviewed",
)
BOUNDARIES = {"server-default", "use-client", "use-server"}
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

    for r in doc["routes"]:
        for f in r.get("files", []):
            file_name = f.get("file", "")
            boundary = f.get("boundary")
            if boundary not in BOUNDARIES:
                errors.append(f"unknown boundary {boundary!r} on {file_name!r}")
            if file_name.endswith("layout.tsx") and boundary == "use-client":
                errors.append(f"layout file marked use-client: {file_name!r}")

    for a in doc["actions"]:
        if a.get("mutates"):
            kind = (a.get("revalidate") or {}).get("kind")
            if kind not in {"path", "tag"}:
                errors.append(f"mutating action {a.get('name')!r} requires revalidate.kind in {{path, tag}}; got {kind!r}")

    flags = doc["tsconfig_flags"]
    for required_flag in ("strict", "noUncheckedIndexedAccess", "exactOptionalPropertyTypes"):
        if not flags.get(required_flag):
            errors.append(f"tsconfig_flags.{required_flag} must be true")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "app-router-spec.json"
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
        sys.stderr.write("usage: validate-typescript-react-2026.py <spec.json>\n")
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
