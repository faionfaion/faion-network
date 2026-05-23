#!/usr/bin/env python3
"""validate-go-layout-agentic-workflow.py — validate a Go Standard Layout — Agentic Workflow and Prompts artefact JSON.

Usage:
  validate-go-layout-agentic-workflow.py <artefact.json>
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
    "artefact_id", "owner", "decision", "rationale",
    "inputs_used", "version", "last_reviewed",
)
ID_RE = re.compile(r"^golaw\-[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COLLAPSED = {"team", "we", "us", "engineering", "the team"}


def _check(doc: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing key: {k}")
    if errs:
        return errs
    if not ID_RE.match(str(doc["artefact_id"])):
        errs.append(f"artefact_id must match ^golaw\-[a-z0-9-]+$, got {doc['artefact_id']!r}")
    if str(doc["owner"]).strip().lower() in COLLAPSED:
        errs.append(f"owner is a collapsed plural: {doc['owner']!r}")
    if len(str(doc["decision"])) < 4:
        errs.append("decision must be a non-trivial string")
    if len(str(doc["rationale"])) < 60:
        errs.append("rationale must be >= 60 chars and cite an input")
    inputs = doc["inputs_used"]
    if not isinstance(inputs, list) or not inputs:
        errs.append("inputs_used must be a non-empty array")
    for inp in inputs if isinstance(inputs, list) else []:
        if not isinstance(inp, dict) or not inp.get("name") or not inp.get("source"):
            errs.append(f"inputs_used entry missing name/source: {inp}")
    if not SEMVER_RE.match(str(doc["version"])):
        errs.append("version must be semver")
    if not DATE_RE.match(str(doc["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


def _self_test() -> int:
    fixture = {
        "artefact_id": "golaw-self-test-001",
        "owner": "alex@acme.com",
        "decision": "decision shape consistent with templates/go-layout-agentic-workflow.md example",
        "rationale": "Self-test fixture cites input A and input B; both are pinned in inputs_used with verifiable sources. Rationale exceeds 60 chars to satisfy the contract.",
        "inputs_used": [
            {"name": "A", "source": "https://example.com/A"},
            {"name": "B", "source": "repo:path/B"}
        ],
        "version": "1.0.0",
        "last_reviewed": "2026-05-23",
    }
    errs = _check(fixture)
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
        sys.stderr.write("usage: validate-go-layout-agentic-workflow.py <artefact.json>\n")
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
