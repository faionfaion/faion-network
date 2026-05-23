#!/usr/bin/env python3
"""validate-tech-debt-management.py

Validate a tech-debt-management plan JSON against schema + rule consistency.

Inputs:
    --file PATH      path to plan JSON
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

ID_RE = re.compile(r"^tdm-[a-z0-9-]{6,}$")
ITEM_ID_RE = re.compile(r"^debt-[a-z0-9-]{4,}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
TEAM_ALIASES = {"engineering", "dev", "ops", "team", "platform", "qa", "support"}
STRATEGIES = {"boy-scout", "feature-attached", "dedicated-sprint", "strangler-fig"}
GATE_KINDS = {"ruff", "eslint", "regex", "ast-visitor", "test-name", "loc-cap", "complexity-cap", "custom"}
NON_MECHANICAL = {"checklist", "review", "documentation"}
VERDICTS = {"adopt-plan", "block-no-gate", "block-no-exit-criteria", "block-low-score-skip"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
UNOBSERVABLE = re.compile(r"^(ongoing|continuous|as needed|when ready|later)\.?$", re.I)


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "register_ref", "items", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^tdm-[a-z0-9-]{6,}$")
    if not str(obj.get("register_ref", "")).strip():
        errs.append("register_ref must be non-empty")

    items = obj.get("items") or []
    if not isinstance(items, list) or len(items) < 1:
        errs.append("items must be a non-empty list")
    else:
        for i, it in enumerate(items):
            if not ITEM_ID_RE.match(str(it.get("debt_item_id", ""))):
                errs.append(f"items[{i}].debt_item_id must match ^debt-[a-z0-9-]{{4,}}$")
            if it.get("strategy") not in STRATEGIES:
                errs.append(f"items[{i}].strategy must be one of {sorted(STRATEGIES)}")
            ex = str(it.get("exit_criterion", "")).strip()
            if len(ex) < 10:
                errs.append(f"items[{i}].exit_criterion must be string of length >= 10")
            if UNOBSERVABLE.match(ex):
                errs.append(f"items[{i}].exit_criterion is unobservable ({ex})")
            gate = it.get("gate") or {}
            if gate.get("kind") not in GATE_KINDS:
                errs.append(f"items[{i}].gate.kind must be one of {sorted(GATE_KINDS)}")
            if gate.get("kind") in NON_MECHANICAL:
                errs.append(f"items[{i}].gate.kind is non-mechanical (r3 violation)")
            if not str(gate.get("definition", "")).strip():
                errs.append(f"items[{i}].gate.definition must be non-empty")
            em = str(it.get("owner_email", ""))
            if em and not EMAIL_RE.match(em):
                errs.append(f"items[{i}].owner_email must be valid email")
            if em.split("@", 1)[0].lower() in TEAM_ALIASES:
                errs.append(f"items[{i}].owner_email is a team alias")
            if it.get("strategy") == "dedicated-sprint" and not it.get("target_sprint"):
                errs.append(f"items[{i}].strategy=dedicated-sprint requires target_sprint")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "tdm-q2-2026",
    "register_ref": "dsr-q2-2026",
    "items": [{
        "debt_item_id": "debt-order-mono",
        "strategy": "strangler-fig",
        "exit_criterion": "100% traffic switched to new order service for 2 weeks",
        "gate": {"kind": "loc-cap", "definition": "src/orders/views.py <= 200 LoC"},
        "owner_email": "ruslan@faion.net",
        "target_sprint": "26",
    }],
    "verdict": "adopt-plan",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "tdm",
    "register_ref": "",
    "items": [{
        "debt_item_id": "x",
        "strategy": "best-practices",
        "exit_criterion": "later",
        "gate": {"kind": "checklist", "definition": "be careful"},
        "owner_email": "team@faion.net",
    }],
    "verdict": "adopt-plan",
    "version": "1.0",
    "last_reviewed": "today",
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
    ap.add_argument("--file", type=str, help="path to plan JSON")
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
