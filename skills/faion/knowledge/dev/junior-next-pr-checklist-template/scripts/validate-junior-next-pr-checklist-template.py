#!/usr/bin/env python3
"""validate-junior-next-pr-checklist-template.py — validate junior-next-pr-checklist-template output against the 02-output-contract schema.

Flags:
  --help        Print usage and exit (provided by argparse).
  --self-test   Run an internal fixture-based smoke test and exit.

Exit codes:
  0 — input passes the schema and forbidden-pattern checks.
  1 — input fails; violations printed to stderr.
  2 — usage / file error.

Inputs:
  - Positional: path to JSON file to validate, OR `--self-test`.

Outputs:
  - stdout: "ok" on pass.
  - stderr: one violation per line on fail.

Dependencies: stdlib only.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["artefact_id", "owner", "problem", "decision", "rationale", "inputs_used", "version", "last_reviewed"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
ID_RE = re.compile(r"^[a-z][a-z0-9-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(doc: dict) -> list[str]:
    violations: list[str] = []
    if not isinstance(doc, dict):
        return ["root must be a JSON object"]
    for key in REQUIRED:
        if key not in doc:
            violations.append(f"missing required key: {key}")
    owner = (doc.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        violations.append(f"forbidden owner value: {owner!r} (must be named human or role-with-rotation)")
    artefact_id = doc.get("artefact_id", "")
    if artefact_id and not ID_RE.match(artefact_id):
        violations.append(f"artefact_id does not match pattern ^[a-z][a-z0-9-]+$: {artefact_id!r}")
    version = doc.get("version", "")
    if version and not SEMVER.match(version):
        violations.append(f"version not semver: {version!r}")
    last_reviewed = doc.get("last_reviewed", "")
    if last_reviewed and not DATE_RE.match(last_reviewed):
        violations.append(f"last_reviewed not ISO date: {last_reviewed!r}")
    return violations


def self_test() -> int:
    good = {
        "artefact_id": "sample-2026-q2",
        "owner": "ruslan@faion.net",
        "version": "1.0.0",
        "last_reviewed": "2026-05-23",
    }
    for key in REQUIRED:
        good.setdefault(key, "x")
    v = validate(good)
    if v:
        print(f"self-test FAIL on valid doc: {v}", file=sys.stderr)
        return 1
    bad = {"artefact_id": "BAD ID", "owner": "team", "version": "draft"}
    v = validate(bad)
    if not v:
        print("self-test FAIL: invalid doc passed", file=sys.stderr)
        return 1
    print("self-test ok")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        prog="validate-junior-next-pr-checklist-template.py",
        description="Validate junior-next-pr-checklist-template output against 02-output-contract schema. Exit 0 on pass, 1 on fail, 2 on usage error.",
    )
    p.add_argument("path", nargs="?", help="Path to JSON file to validate")
    p.add_argument("--self-test", action="store_true", help="Run an internal fixture-based smoke test and exit")
    args = p.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.path:
        p.print_help(sys.stderr)
        return 2
    try:
        doc = json.loads(Path(args.path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"file not found: {args.path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"json parse error: {e}", file=sys.stderr)
        return 1
    violations = validate(doc)
    if violations:
        for v in violations:
            print(v, file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
