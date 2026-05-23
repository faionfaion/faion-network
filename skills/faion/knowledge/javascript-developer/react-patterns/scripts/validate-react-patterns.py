#!/usr/bin/env python3
"""validate-react-patterns.py — validate a feature-spec JSON against the methodology contract.

Inputs:
  PATH  feature-spec JSON path
Flags:
  --help, --self-test
Exit codes: 0 ok, 1 contract violation, 2 usage/IO error.
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
    "feature_name",
    "react_version",
    "folder_tree",
    "components",
    "context",
    "state_routing",
    "version",
    "last_reviewed",
)
LAYERS = {"server", "form", "global-ui", "local", "shared-context"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
FEATURE_RE = re.compile(r"^[a-z][a-z0-9-]*$")
COMP_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
PROPS_RE = re.compile(r"^[A-Z][A-Za-z0-9]*Props$")


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
    if not FEATURE_RE.match(doc["feature_name"]):
        errors.append("feature_name must be lowercase-kebab")

    tree = doc["folder_tree"]
    if not isinstance(tree, list) or len(tree) < 4:
        errors.append("folder_tree must list >= 4 paths")

    comps = doc["components"]
    if not isinstance(comps, list) or not comps:
        errors.append("components must be a non-empty array")
    for c in comps if isinstance(comps, list) else []:
        if not COMP_RE.match(c.get("name", "")):
            errors.append(f"component name must be PascalCase: {c.get('name')!r}")
        if not PROPS_RE.match(c.get("props_interface", "")):
            errors.append(f"props_interface must end with Props: {c.get('props_interface')!r}")
        if c.get("declaration") not in {"function-declaration", "named-const-arrow"}:
            errors.append(f"unknown declaration: {c.get('declaration')!r}")

    ctx = doc["context"]
    if ctx is not None:
        if not ctx.get("null_sentinel"):
            errors.append("context.null_sentinel must be true")
        if not ctx.get("value_memoized"):
            errors.append("context.value_memoized must be true")

    routing = doc["state_routing"]
    if not isinstance(routing, list) or not routing:
        errors.append("state_routing must be a non-empty array")
    seen: set[str] = set()
    for r in routing if isinstance(routing, list) else []:
        slc = r.get("slice")
        if slc in seen:
            errors.append(f"duplicate state_routing slice: {slc!r}")
        seen.add(slc)
        if r.get("layer") not in LAYERS:
            errors.append(f"layer not allowed: {r.get('layer')!r}")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "feature-spec.json"
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
        sys.stderr.write("usage: validate-react-patterns.py <feature-spec.json>\n")
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
