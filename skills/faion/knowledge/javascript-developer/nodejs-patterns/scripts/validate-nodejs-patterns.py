#!/usr/bin/env python3
"""validate-nodejs-patterns.py — validate a scaffold-spec JSON against the methodology contract.

Inputs:
  PATH    path to a JSON file produced by the agent (positional)

Outputs:
  stdout  JSON line summarising the result
  exit 0  on pass
  exit 1  on contract violation (with violation list on stderr)
  exit 2  on usage / IO error
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED_MW = {
    "helmet",
    "cors",
    "json",
    "urlencoded",
    "compression",
    "requestLogger",
    "auth",
    "routes",
    "errorHandler",
}

REQUIRED_KEYS = (
    "artefact_id",
    "owner",
    "service_name",
    "node_version",
    "folder_tree",
    "middleware_order",
    "error_classes",
    "logger",
    "version",
    "last_reviewed",
)

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
NODE_RE = re.compile(r"^[>=^~]*\d+(\.\d+){0,2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")


def _check(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in doc:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors

    if not SLUG_RE.match(doc["artefact_id"]):
        errors.append("artefact_id must be kebab-case")

    if str(doc["owner"]).strip().lower() in {"", "team", "we", "us"}:
        errors.append("owner must be a single named accountable owner")

    if not NODE_RE.match(doc["node_version"]):
        errors.append(f"node_version not semver-shaped: {doc['node_version']!r}")

    folder = doc["folder_tree"]
    if not isinstance(folder, list) or len(folder) < 5:
        errors.append("folder_tree must list >= 5 paths")
    for entry in folder:
        if "app.listen" in str(entry):
            errors.append("folder_tree must not include 'app.listen' inside the factory")

    mw = doc["middleware_order"]
    if not isinstance(mw, list) or len(mw) < 6:
        errors.append("middleware_order must list >= 6 entries")
    bad = [m for m in mw if m not in ALLOWED_MW]
    if bad:
        errors.append(f"middleware_order has unknown tokens: {bad}")
    if mw and mw[-1] != "errorHandler":
        errors.append("middleware_order MUST end with 'errorHandler'")
    if "errorHandler" in mw and "routes" in mw and mw.index("errorHandler") < mw.index("routes"):
        errors.append("'errorHandler' must come AFTER 'routes' in middleware_order")

    classes = doc["error_classes"]
    if not isinstance(classes, list) or len(classes) < 2:
        errors.append("error_classes must contain >= 2 entries")
    for cls in classes if isinstance(classes, list) else []:
        for k in ("name", "statusCode", "code", "isOperational"):
            if k not in cls:
                errors.append(f"error_class missing field {k}: {cls}")
        sc = cls.get("statusCode")
        if not isinstance(sc, int) or not 400 <= sc <= 599:
            errors.append(f"error_class statusCode out of range: {cls}")

    logger = doc["logger"]
    if not isinstance(logger, dict) or logger.get("library") not in {"pino", "winston"}:
        errors.append("logger.library must be 'pino' or 'winston'")
    if "request_id_header" not in (logger or {}):
        errors.append("logger.request_id_header is required")

    if not SEMVER_RE.match(doc["version"]):
        errors.append(f"version not semver: {doc['version']!r}")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append(f"last_reviewed not ISO date: {doc['last_reviewed']!r}")

    return errors


def _self_test() -> int:
    fixture = json.loads(
        (Path(__file__).parent.parent / "templates" / "scaffold-spec.json").read_text()
    )
    fixture.pop("_purpose", None)
    fixture.pop("_consumes", None)
    fixture.pop("_produces", None)
    fixture.pop("_depends-on", None)
    fixture.pop("_token-budget-impact", None)
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
        sys.stderr.write("usage: validate-nodejs-patterns.py <scaffold-spec.json>\n")
        return 2
    path = Path(argv[1])
    try:
        doc = json.loads(path.read_text())
    except OSError as exc:
        sys.stderr.write(f"cannot read {path}: {exc}\n")
        return 2
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON in {path}: {exc}\n")
        return 1
    # strip optional `_meta` keys
    for k in [k for k in doc if k.startswith("_")]:
        doc.pop(k)
    errs = _check(doc)
    if errs:
        sys.stderr.write("contract violations:\n" + "\n".join(f" - {e}" for e in errs) + "\n")
        return 1
    sys.stdout.write(json.dumps({"ok": True, "path": str(path)}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
