#!/usr/bin/env python3
"""validate-company-prompt-library-pattern.py — validate a company prompt-library spec JSON.

Usage:
  validate-company-prompt-library-pattern.py <spec.json>
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
    "spec_id", "owner", "namespace_map", "override_layers",
    "eval_gate", "role_packs", "version", "last_reviewed",
)
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NS_RE = re.compile(r"^prompts/(role|task)/[a-z0-9-]+/$")
LAYERS = ["faion-defaults", "role-pack", "company-override", "repo-override"]
COLLAPSED = {"team", "we", "us", "engineering", "the team"}


def _check(doc: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing key: {k}")
    if errs:
        return errs
    if not SLUG_RE.match(str(doc["spec_id"])):
        errs.append("spec_id must be kebab-case")
    if str(doc["owner"]).strip().lower() in COLLAPSED:
        errs.append(f"owner is a collapsed plural: {doc['owner']!r}")
    ns = doc.get("namespace_map", {})
    if not isinstance(ns, dict) or not ns:
        errs.append("namespace_map must be non-empty object")
    for k in ns if isinstance(ns, dict) else []:
        if not NS_RE.match(k):
            errs.append(f"namespace key out of shape: {k!r}")
    layers = doc.get("override_layers", [])
    if layers != LAYERS:
        errs.append(f"override_layers must be exactly {LAYERS}, got {layers}")
    gate = doc.get("eval_gate", {})
    if not isinstance(gate, dict) or not gate.get("scorers"):
        errs.append("eval_gate.scorers must be non-empty list")
    if not gate.get("block_on_fail"):
        errs.append("eval_gate.block_on_fail must be true")
    for pack in doc.get("role_packs", []) if isinstance(doc.get("role_packs"), list) else []:
        if not pack.get("owner") or str(pack["owner"]).strip().lower() in COLLAPSED:
            errs.append(f"role_pack {pack.get('name')!r} missing/collapsed owner")
    if not SEMVER_RE.match(str(doc["version"])):
        errs.append("version must be semver")
    if not DATE_RE.match(str(doc["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


def _self_test() -> int:
    fixture = {
        "spec_id": "acme-prompt-library",
        "owner": "alex@acme.com",
        "namespace_map": {
            "prompts/role/pm/": "PM agents",
            "prompts/role/dev/": "dev agents",
        },
        "override_layers": LAYERS,
        "eval_gate": {"scorers": ["rubric-judge"], "threshold": 0.85, "block_on_fail": True},
        "role_packs": [{"name": "pm", "owner": "alex@acme.com", "count": 12}],
        "version": "1.0.0",
        "last_reviewed": "2026-05-22",
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
        sys.stderr.write("usage: validate-company-prompt-library-pattern.py <spec.json>\n")
        return 2
    try:
        doc = json.loads(Path(argv[1]).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"read/parse error: {exc}\n")
        return 2
    errs = _check(doc)
    if errs:
        sys.stderr.write("violations:\n" + "\n".join(f" - {e}" for e in errs) + "\n")
        return 1
    sys.stdout.write(json.dumps({"ok": True}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
