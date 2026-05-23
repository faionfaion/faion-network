#!/usr/bin/env python3
"""validate-creative-brief-template.py

Validate a creative-brief JSON against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to brief JSON
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

BANNED_OWNER = re.compile(r"^(team|we|us|engineering|marketing|growth)$", re.I)
REQUIRED_TOP = ("brief_id", "campaign", "audience", "angle", "hook", "proof", "cta", "format", "owner", "version", "last_reviewed")
CAMP_TYPES = {"lead-gen", "conversion", "retargeting", "brand"}
CHANNELS = {"meta", "google", "linkedin", "tiktok", "x", "other"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing required: {k}")
    if not str(obj.get("brief_id", "")).startswith("cb-"):
        errs.append("brief_id must start with 'cb-'")
    camp = obj.get("campaign") or {}
    if camp.get("type") not in CAMP_TYPES:
        errs.append(f"campaign.type must be one of {sorted(CAMP_TYPES)}")
    if camp.get("channel") not in CHANNELS:
        errs.append(f"campaign.channel must be one of {sorted(CHANNELS)}")
    for field in ("audience", "angle", "hook"):
        sub = obj.get(field) or {}
        if not sub.get("source"):
            errs.append(f"{field}.source missing")
    proof = obj.get("proof") or []
    if not isinstance(proof, list) or not proof:
        errs.append("proof must be non-empty array")
    for i, p in enumerate(proof if isinstance(proof, list) else []):
        if "claim" not in p or "source" not in p:
            errs.append(f"proof[{i}] missing claim/source")
    owner = obj.get("owner", "")
    if not isinstance(owner, str) or len(owner) < 3:
        errs.append("owner missing or too short")
    elif BANNED_OWNER.match(owner.strip()):
        errs.append(f"owner is banned plural noun: {owner!r}")
    if not SEMVER.match(obj.get("version", "")):
        errs.append("version must be semver")
    return errs


OK = {
    "brief_id": "cb-x", "campaign": {"name": "X", "type": "lead-gen", "channel": "meta", "starts_at": "2026-06-01"},
    "audience": {"definition": "y", "source": "icp.md"}, "angle": {"text": "z", "source": "icp.md"},
    "hook": {"text": "w", "source": "i.md"}, "proof": [{"claim": "c", "source": "s"}],
    "cta": {"primary": "Book demo", "secondary": "Read case study"},
    "format": {"aspect": "1:1", "duration_or_length": "15s"}, "owner": "@alex", "version": "1.0.0", "last_reviewed": "2026-05-23",
}
BAD = {"brief_id": "cb-1", "owner": "team"}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n"); return 1
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
