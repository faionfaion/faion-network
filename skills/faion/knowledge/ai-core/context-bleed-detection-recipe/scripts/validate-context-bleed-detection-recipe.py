#!/usr/bin/env python3
"""validate-context-bleed-detection-recipe.py — validate a context-bleed incident record.

Usage:
  validate-context-bleed-detection-recipe.py <incident.json>
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
    "incident_id", "owner", "bleed_type", "probe_signal",
    "session_hashes", "threshold", "kill_switch", "version", "detected_at",
)
ID_RE = re.compile(r"^cbi-[a-z0-9-]+$")
HASH_RE = re.compile(r"^[a-f0-9]{16}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?$")
BLEED = {"cross-tenant", "prior-turn", "system-drift", "clean"}
SCOPE = {"worker-pool", "prompt-cache-key", "session-range", "fleet"}
COLLAPSED = {"team", "we", "us", "engineering", "the team"}


def _check(doc: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing key: {k}")
    if errs:
        return errs
    if not ID_RE.match(str(doc["incident_id"])):
        errs.append("incident_id must match ^cbi-[a-z0-9-]+$")
    if str(doc["owner"]).strip().lower() in COLLAPSED:
        errs.append(f"owner is a collapsed plural: {doc['owner']!r}")
    if doc["bleed_type"] not in BLEED:
        errs.append(f"bleed_type must be one of {sorted(BLEED)}")
    ps = doc.get("probe_signal", {})
    if not isinstance(ps, dict):
        errs.append("probe_signal must be object")
    else:
        for k in ("canary_hit", "embedding_distance", "snapshot_diff"):
            if k not in ps:
                errs.append(f"probe_signal missing {k}")
    if doc["bleed_type"] == "cross-tenant" and not ps.get("canary_hit", False):
        errs.append("bleed_type=cross-tenant requires probe_signal.canary_hit=true")
    sh = doc.get("session_hashes", [])
    if not isinstance(sh, list) or not sh:
        errs.append("session_hashes must be non-empty list")
    for h in sh if isinstance(sh, list) else []:
        if not HASH_RE.match(str(h)):
            errs.append(f"session_hash not 16-char hex (raw user-id leaked?): {h!r}")
    t = doc.get("threshold")
    if not isinstance(t, (int, float)) or not (0.0 <= t <= 1.0):
        errs.append("threshold must be number in [0,1]")
    ks = doc.get("kill_switch", {})
    if not isinstance(ks, dict) or ks.get("scope") not in SCOPE:
        errs.append(f"kill_switch.scope must be one of {sorted(SCOPE)}")
    if ks.get("scope") == "fleet" and not ks.get("human_approval"):
        errs.append("kill_switch.scope=fleet requires human_approval=true")
    if not SEMVER_RE.match(str(doc["version"])):
        errs.append("version must be semver")
    if not TS_RE.match(str(doc["detected_at"])):
        errs.append("detected_at must be ISO-8601 timestamp")
    return errs


def _self_test() -> int:
    fixture = {
        "incident_id": "cbi-2026-05-22-001",
        "owner": "sre-oncall@acme.com",
        "bleed_type": "cross-tenant",
        "probe_signal": {"canary_hit": True, "embedding_distance": 0.08, "snapshot_diff": "none"},
        "session_hashes": ["a1b2c3d4e5f60718", "f9e8d7c6b5a40392"],
        "threshold": 0.15,
        "kill_switch": {"scope": "worker-pool", "target": "pool-3", "human_approval": False},
        "version": "1.0.0",
        "detected_at": "2026-05-22T10:32:11Z",
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
        sys.stderr.write("usage: validate-context-bleed-detection-recipe.py <incident.json>\n")
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
