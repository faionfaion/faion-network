#!/usr/bin/env python3
"""validate-design-ops-foundations.py

Validate an artefact produced by the design-ops-foundations methodology against the schema
declared in content/02-output-contract.xml (mirrored in templates/design-ops-foundations.schema.json).

Inputs:
    --file PATH       path to artefact (JSON or Markdown-with-table)
    --schema PATH     path to JSON schema (default: templates/design-ops-foundations.schema.json)
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["artefact_id", "owner", "decision", "version", "last_reviewed", "inputs_used"]

FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", "the team", "the squad", "the group"}


def parse_markdown_table(text: str) -> dict:
    """Pull a 'Field | Value' table from a Markdown artefact, and also scan
    heading-style sections (## field-name) for required field values."""
    out: dict = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*([a-zA-Z_]+)\s*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            key, value = m.group(1).strip(), m.group(2).strip()
            if key.lower() in ("field", "key") and value.lower() in ("value",):
                continue
            out[key] = value
    # Heading-style: ## <field>\n\n<value>
    for m in re.finditer(r"^##\s+([a-zA-Z_]+)\s*\n+([^\n][^\n]*)", text, flags=re.MULTILINE):
        key = m.group(1).strip()
        val = m.group(2).strip()
        if key not in out and val and not val.startswith("-") and not val.startswith("1."):
            out[key] = val
    return out


def coerce_obj(path: Path) -> dict:
    text = path.read_text()
    if path.suffix == ".json":
        return json.loads(text)
    obj = parse_markdown_table(text)
    # inputs_used: scan list items after a heading containing 'inputs'
    inputs: list[str] = []
    in_inputs = False
    for line in text.splitlines():
        if re.match(r"#+\s+inputs(\s+used)?", line, flags=re.IGNORECASE):
            in_inputs = True
            continue
        if in_inputs and line.startswith("#"):
            break
        if in_inputs and line.startswith("- "):
            inputs.append(line[2:].strip())
    if inputs:
        obj["inputs_used"] = inputs
    # decision: first paragraph under a 'Decision' heading
    m = re.search(r"#+\s+decision[^\n]*\n+(.+?)(?:\n#+\s|$)", text, flags=re.IGNORECASE | re.DOTALL)
    if m and "decision" not in obj:
        obj["decision"] = m.group(1).strip().split("\n")[0]
    return obj


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object/table"]
    for k in REQUIRED:
        if k not in obj or not obj[k]:
            errs.append(f"missing required field: {k}")
    owner = (obj.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS or not owner:
        errs.append(f"owner is forbidden value: {owner!r}")
    version = obj.get("version") or ""
    if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", str(version)):
        errs.append(f"version not semver: {version!r}")
    last_rev = str(obj.get("last_reviewed") or "")
    if not re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", last_rev):
        errs.append(f"last_reviewed not ISO date: {last_rev!r}")
    inputs = obj.get("inputs_used") or []
    if not isinstance(inputs, list) or len(inputs) < 1:
        errs.append("inputs_used must be a non-empty list")
    return errs


OK = {
    "artefact_id": "smoke-design-ops-foundations",
    "owner": "Maria Lopes",
    "decision": "raise floor rate from $125 to $140",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
    "inputs_used": ["toggl-export-q1.csv"],
}

BAD = {
    "artefact_id": "no-owner",
    "owner": "team",
    "decision": "",
    "version": "1.0",
    "last_reviewed": "tomorrow",
    "inputs_used": [],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected: " + repr(validate(OK)) + "\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--schema", type=str, default=None)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = coerce_obj(p)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"parse error: {exc}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
