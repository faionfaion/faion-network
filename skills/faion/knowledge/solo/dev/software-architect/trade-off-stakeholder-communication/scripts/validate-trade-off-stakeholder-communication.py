#!/usr/bin/env python3
"""validate-trade-off-stakeholder-communication.py

Validate a stakeholder briefing bundle against the schema declared in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to bundle JSON
    --self-test       run built-in fixtures (OK + BAD)
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

ARTEFACT_KEYS = ("exec_summary", "pm_brief", "engineer_note", "ops_delta")
DECISION_ID_RE = re.compile(r"^ADR-[0-9]{3,5}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("decision_id", "decision_title", "reversibility", "key_risk", "artefacts"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "decision_id" in obj and not DECISION_ID_RE.match(str(obj["decision_id"])):
        errs.append(f"decision_id must match ^ADR-[0-9]{{3,5}}$: got {obj['decision_id']!r}")
    if obj.get("reversibility") not in ("type-1", "type-2"):
        errs.append(f"reversibility must be type-1|type-2: got {obj.get('reversibility')!r}")
    kr = obj.get("key_risk", "")
    if not (24 <= len(kr) <= 320):
        errs.append(f"key_risk length must be 24..320 chars: got {len(kr)}")

    artefacts = obj.get("artefacts") or {}
    for k in ARTEFACT_KEYS:
        if k not in artefacts:
            errs.append(f"artefacts missing {k}")

    exec_s = artefacts.get("exec_summary") or {}
    wc = exec_s.get("word_count")
    if isinstance(wc, int) and wc > 120:
        errs.append(f"exec_summary.word_count > 120: {wc}")

    eng = artefacts.get("engineer_note") or {}
    sac = eng.get("sacrificed")
    if not (isinstance(sac, list) and len(sac) >= 1):
        errs.append("engineer_note.sacrificed must have >=1 entry")

    # risk-preservation: verbatim key_risk in every artefact body
    bodies = {}
    for k in ARTEFACT_KEYS:
        a = artefacts.get(k) or {}
        body = a.get("body", "")
        bodies[k] = body
        if kr and kr not in body:
            errs.append(f"artefacts.{k}.body must contain key_risk verbatim")
        if a.get("embeds_key_risk") is not True:
            errs.append(f"artefacts.{k}.embeds_key_risk must be true")

    # role-fit: no two artefacts share identical body text
    seen: dict[str, str] = {}
    for k, b in bodies.items():
        if b and b in seen:
            errs.append(f"artefacts.{k}.body identical to artefacts.{seen[b]}.body (role-fit violation)")
        elif b:
            seen[b] = k

    # convergence-check gate for type-1
    if obj.get("reversibility") == "type-1" and obj.get("convergence_check_passed") is not True:
        errs.append("convergence_check_passed must be true for type-1 decisions")

    return errs


OK = {
    "decision_id": "ADR-0023",
    "decision_title": "Adopt Postgres-only persistence; defer Redis cache to Phase 2",
    "reversibility": "type-1",
    "key_risk": "Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
    "artefacts": {
        "exec_summary": {
            "body": "We are standardising on Postgres. Key risk: Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
            "word_count": 40,
            "embeds_key_risk": True,
        },
        "pm_brief": {
            "body": "Phase 2 cache becomes P0. Key risk: Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
            "roadmap_impact": "Phase 2 adds 4 weeks",
            "dependency_changes": ["cache layer P0"],
            "embeds_key_risk": True,
        },
        "engineer_note": {
            "body": "Postgres-only. Key risk: Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
            "sacrificed": ["Sub-ms p99 reads", "Independent cache scaling"],
            "embeds_key_risk": True,
        },
        "ops_delta": {
            "body": "Single oncall. Key risk: Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
            "runbook_changes": ["pool saturation"],
            "alert_changes": ["p95 250ms"],
            "embeds_key_risk": True,
        },
    },
    "convergence_check_passed": True,
}

BAD = {
    "decision_id": "ADR-99",
    "decision_title": "x",
    "reversibility": "type-1",
    "key_risk": "vague",
    "artefacts": {
        "exec_summary": {"body": "no", "word_count": 200, "embeds_key_risk": False},
        "pm_brief": {"body": "no", "roadmap_impact": "", "dependency_changes": [], "embeds_key_risk": False},
        "engineer_note": {"body": "no", "sacrificed": [], "embeds_key_risk": False},
        "ops_delta": {"body": "no", "runbook_changes": [], "alert_changes": [], "embeds_key_risk": False},
    },
}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"OK fixture rejected: {errs_ok}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to bundle JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    except Exception as e:
        sys.stderr.write(f"cannot parse JSON: {e}\n")
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
