#!/usr/bin/env python3
"""validate-trunk-based-feature-flags.py

Validate a per-flag spec JSON against the schema and rule consistency.

Inputs:
    --file PATH      path to flag-spec JSON
    --self-test      run built-in valid + invalid fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TYPES = {"release", "experiment", "ops", "permission"}
ID_RE = re.compile(r"^ff-[a-z0-9-]{6,}$")
FLAG_ID_RE = re.compile(r"^[a-z][a-z0-9_.]{3,63}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
TEAM_ALIASES = {"engineering", "dev", "ops", "team", "platform", "qa", "support"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "flag_id", "owner_email", "type", "ramp_plan", "kill_switch_tested", "cleanup_ticket_id", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^ff-[a-z0-9-]{6,}$")

    if "flag_id" in obj and not FLAG_ID_RE.match(str(obj["flag_id"])):
        errs.append("flag_id must match ^[a-z][a-z0-9_.]{3,63}$")

    em = str(obj.get("owner_email", ""))
    if em and not EMAIL_RE.match(em):
        errs.append("owner_email must be a valid email")
    local = em.split("@", 1)[0].lower() if "@" in em else em.lower()
    if local in TEAM_ALIASES:
        errs.append(f"owner_email is a team alias ({local}); use a named human")

    typ = obj.get("type")
    if typ and typ not in TYPES:
        errs.append(f"type must be one of {sorted(TYPES)}")

    rp = obj.get("ramp_plan")
    if not isinstance(rp, list) or len(rp) < 1:
        errs.append("ramp_plan must be a non-empty list")
    else:
        for i, stage in enumerate(rp):
            for sub in ("pct", "gate"):
                if sub not in stage:
                    errs.append(f"ramp_plan[{i}] missing {sub}")
            pct = stage.get("pct")
            if not isinstance(pct, int) or not (0 <= pct <= 100):
                errs.append(f"ramp_plan[{i}].pct must be int in [0,100]")
            gate = stage.get("gate")
            if not isinstance(gate, str) or not gate.strip():
                errs.append(f"ramp_plan[{i}].gate must be a non-empty string")
        # Single-step 0→100 only allowed for type=ops.
        if typ != "ops":
            pcts = [s.get("pct", 0) for s in rp if isinstance(s, dict)]
            if pcts == [100] or (len(pcts) == 2 and pcts[0] == 0 and pcts[1] == 100):
                errs.append("ramp_plan single-step 0→100 only allowed for type=ops")

    if obj.get("kill_switch_tested") is True and not obj.get("kill_switch_test_run_id"):
        errs.append("kill_switch_tested=true requires kill_switch_test_run_id")

    ct = obj.get("cleanup_ticket_id")
    if not isinstance(ct, str) or not ct.strip():
        errs.append("cleanup_ticket_id must be a non-empty string")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    if "cleanup_sla_date" in obj and obj["cleanup_sla_date"] and not DATE_RE.match(str(obj["cleanup_sla_date"])):
        errs.append("cleanup_sla_date must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "ff-f066-shadow-router",
    "flag_id": "quote_shadow_go_pct",
    "owner_email": "ruslan@faion.net",
    "type": "release",
    "ramp_plan": [
        {"pct": 1, "gate": "diff_rate < 0.5"},
        {"pct": 10, "gate": "diff_rate < 0.5 AND error_rate baseline"},
        {"pct": 50, "gate": "clusters classified"},
        {"pct": 100, "gate": "sign-off"},
    ],
    "kill_switch_tested": True,
    "kill_switch_test_run_id": "CI-9982",
    "cleanup_ticket_id": "TICKET-4421",
    "cleanup_sla_date": "2026-07-23",
    "dark_launch": True,
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "shadow",
    "flag_id": "X",
    "owner_email": "engineering@faion.net",
    "type": "misc",
    "ramp_plan": [],
    "kill_switch_tested": True,
    "cleanup_ticket_id": "",
    "version": "1.0",
    "last_reviewed": "soon",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to flag-spec JSON")
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
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
