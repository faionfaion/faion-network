#!/usr/bin/env python3
"""validate-typescript-strict-mode.py — validate a strict-mode migration spec JSON.

Usage:
  validate-typescript-strict-mode.py <spec.json>
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
    "repo",
    "ts_version",
    "current_flags",
    "target_flags",
    "migration_steps",
    "lint_backstops",
    "version",
    "last_reviewed",
)
REQ_TARGET = ("strict", "noUncheckedIndexedAccess", "exactOptionalPropertyTypes")
FORBIDDEN_TOKENS = ("TBD", "later", "TODO")
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

    tflags = doc["target_flags"]
    for f in REQ_TARGET:
        if tflags.get(f) is not True:
            errors.append(f"target_flags.{f} must be true")

    steps = doc["migration_steps"]
    flags_in_steps = {s.get("flag") for s in steps if isinstance(s, dict)}
    for f in REQ_TARGET:
        if f not in flags_in_steps:
            errors.append(f"migration_steps must include a step for flag {f!r}")
    for s in steps:
        strat = str(s.get("fix_strategy") or "")
        if len(strat) < 20:
            errors.append(f"fix_strategy too short on step {s.get('order')}")
        for tok in FORBIDDEN_TOKENS:
            if tok.lower() in strat.lower():
                errors.append(f"fix_strategy contains forbidden token {tok!r} on step {s.get('order')}")

    backs = set(doc["lint_backstops"])
    if not any("no-non-null-assertion" in b for b in backs):
        errors.append("lint_backstops must include no-non-null-assertion")
    if not any("no-explicit-any" in b for b in backs):
        errors.append("lint_backstops must include no-explicit-any")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "migration-spec.json"
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
        sys.stderr.write("usage: validate-typescript-strict-mode.py <spec.json>\n")
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
