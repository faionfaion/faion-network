#!/usr/bin/env python3
"""validate-react-hooks.py — validate a hooks-spec JSON against the methodology contract.

Inputs:
  PATH  hooks-spec JSON path
Flags:
  --help, --self-test
Exit codes: 0 ok, 1 contract violation, 2 usage/IO error
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
    "state_slices",
    "effects",
    "memoization",
    "version",
    "last_reviewed",
)
ALLOWED_OWNER_HOOK = {
    "useState",
    "useReducer",
    "useContext",
    "useRef",
    "external-store",
    "tanstack-query",
    "react-hook-form",
    "use-promise",
}
ALLOWED_MEMO_HOOK = {"useMemo", "useCallback", "React.memo"}

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EFFECT_KEYWORDS = ("subscribe", "listener", "interval", "fetch", "websocket", "ws")


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

    slices = doc["state_slices"]
    if not isinstance(slices, list) or not slices:
        errors.append("state_slices must be a non-empty array")
    for s in slices if isinstance(slices, list) else []:
        if s.get("owner_hook") not in ALLOWED_OWNER_HOOK:
            errors.append(f"state_slice.owner_hook not allowed: {s.get('owner_hook')!r}")

    effects = doc.get("effects", [])
    for e in effects if isinstance(effects, list) else []:
        name = str(e.get("name", "")).lower()
        if not e.get("cleanup_present") and any(kw in name for kw in EFFECT_KEYWORDS):
            errors.append(f"effect {name!r} requires cleanup_present=true (matches keyword)")
        for dep in e.get("deps") or []:
            d = str(dep).strip()
            if d.startswith("{") or d.startswith("["):
                errors.append(f"effect {name!r} dep is inline literal: {dep!r}")

    for m in doc.get("memoization") or []:
        if m.get("hook") not in ALLOWED_MEMO_HOOK:
            errors.append(f"memoization.hook not allowed: {m.get('hook')!r}")
        j = str(m.get("justification") or "")
        if len(j) < 10 or "just-in-case" in j.lower():
            errors.append(f"memoization.justification too thin: {j!r}")

    if not SEMVER_RE.match(doc["version"]):
        errors.append("version must be semver")
    if not DATE_RE.match(doc["last_reviewed"]):
        errors.append("last_reviewed must be ISO date")
    return errors


def _self_test() -> int:
    p = Path(__file__).parent.parent / "templates" / "hooks-spec.json"
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
        sys.stderr.write("usage: validate-react-hooks.py <hooks-spec.json>\n")
        return 2
    path = Path(argv[1])
    try:
        doc = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"read/parse error: {exc}\n")
        return 2
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
