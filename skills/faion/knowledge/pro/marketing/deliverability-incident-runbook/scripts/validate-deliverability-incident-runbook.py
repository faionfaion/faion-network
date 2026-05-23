#!/usr/bin/env python3
"""validate-deliverability-incident-runbook.py

Validate the incident report JSON against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to incident report JSON
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

BANNED_OWNER = re.compile(r"^(team|we|us)$", re.I)
INC_ID = re.compile(r"^inc-\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
ACTIONS = {"throttle", "pause-segment", "suppress-list", "escalate", "no-op"}
CHECKS = {"spf", "dkim", "dmarc", "esp_reputation", "blocklist_lookup", "complaint_sample"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("incident_id", "detected_at", "owner", "metrics", "diagnostics", "containment", "postmortem", "version"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    if not INC_ID.match(obj.get("incident_id", "")):
        errs.append("incident_id must match inc-YYYY-MM-DD-<slug>")
    if not SEMVER.match(obj.get("version", "")):
        errs.append("version must be semver")
    owner = obj.get("owner", "")
    if not isinstance(owner, str) or len(owner) < 3:
        errs.append("owner missing or too short")
    elif BANNED_OWNER.match(owner.strip()):
        errs.append(f"owner is banned plural noun: {owner!r}")
    metrics = obj.get("metrics") or {}
    for k in ("complaint_rate_pct", "bounce_rate_pct", "unsub_rate_pct", "segment"):
        if k not in metrics:
            errs.append(f"metrics.{k} missing")
    diags = obj.get("diagnostics") or []
    if not isinstance(diags, list) or not diags:
        errs.append("diagnostics must be non-empty array")
    for i, d in enumerate(diags if isinstance(diags, list) else []):
        for k in ("check", "result", "source"):
            if k not in d:
                errs.append(f"diagnostics[{i}].{k} missing")
        if d.get("check") not in CHECKS:
            errs.append(f"diagnostics[{i}].check invalid: {d.get('check')!r}")
    cont = obj.get("containment") or {}
    if cont.get("action") not in ACTIONS:
        errs.append(f"containment.action invalid: {cont.get('action')!r}")
    if cont.get("action") in {"throttle", "pause-segment"} and not cont.get("auto_resume_at"):
        errs.append("containment requires auto_resume_at (rule reversible-throttle)")
    pm = obj.get("postmortem") or ""
    if not isinstance(pm, str) or len(pm) < 100:
        errs.append("postmortem must be >= 100 chars")
    return errs


OK = {
    "incident_id": "inc-2026-05-23-x",
    "detected_at": "2026-05-23T09:42:00Z",
    "owner": "@alex-email",
    "metrics": {"complaint_rate_pct": 0.18, "bounce_rate_pct": 2.4, "unsub_rate_pct": 1.6, "segment": "seg-b"},
    "diagnostics": [{"check": "dkim", "result": "pass", "source": "https://x.test"}],
    "containment": {"action": "pause-segment", "auto_resume_at": "2026-05-24T09:00:00Z"},
    "postmortem": "x" * 120,
    "version": "1.0.0",
}
BAD = {"incident_id": "inc-1", "owner": "team"}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
