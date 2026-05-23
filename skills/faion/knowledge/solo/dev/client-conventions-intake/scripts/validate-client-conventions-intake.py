#!/usr/bin/env python3
"""validate-client-conventions-intake.py

Validate a client-conventions intake report JSON against the schema + rule consistency.

Inputs:
    --file PATH      path to report JSON
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

ID_RE = re.compile(r"^cci-[a-z0-9-]{6,}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
TEAM_ALIASES = {"engineering", "dev", "ops", "team", "platform", "qa", "support"}
DIMENSIONS = ("branching", "commit_style", "code_review", "naming", "ci_gates", "security", "documentation", "communication")
VERDICTS = {"commit-record", "block-missing-dimensions", "block-no-signoff", "block-stated-observed-mismatch"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "client", "engagement_start", "contact_email", "dimensions", "mismatches", "signoff", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^cci-[a-z0-9-]{6,}$")
    if "engagement_start" in obj and not DATE_RE.match(str(obj["engagement_start"])):
        errs.append("engagement_start must be ISO date")

    em = str(obj.get("contact_email", ""))
    if em and not EMAIL_RE.match(em):
        errs.append("contact_email must be valid email")
    if em.split("@", 1)[0].lower() in TEAM_ALIASES:
        errs.append(f"contact_email is a team alias")

    dims = obj.get("dimensions") or {}
    if not isinstance(dims, dict):
        errs.append("dimensions must be an object")
    else:
        for d in DIMENSIONS:
            block = dims.get(d)
            if not isinstance(block, dict):
                errs.append(f"dimensions.{d} missing or not object")
                continue
            for sub in ("stated", "source"):
                if sub not in block or not str(block[sub]).strip():
                    errs.append(f"dimensions.{d}.{sub} missing or empty")

    mm = obj.get("mismatches") or []
    if isinstance(mm, list):
        for i, item in enumerate(mm):
            for sub in ("dimension", "stated", "observed", "resolution"):
                if sub not in item or not str(item.get(sub, "")).strip():
                    errs.append(f"mismatches[{i}].{sub} missing or empty")

    signoff = obj.get("signoff") or {}
    if not isinstance(signoff, dict) or not signoff:
        errs.append("signoff missing")
    else:
        sby = str(signoff.get("signed_by", ""))
        if sby and not EMAIL_RE.match(sby):
            errs.append("signoff.signed_by must be valid email")
        if sby.split("@", 1)[0].lower() in TEAM_ALIASES:
            errs.append("signoff.signed_by is a team alias")
        if "signed_at" not in signoff or not DATE_RE.match(str(signoff["signed_at"])):
            errs.append("signoff.signed_at must be ISO date")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


def _dim(s, src):
    return {"stated": s, "source": src}


VALID_FIXTURE = {
    "artefact_id": "cci-acme-2026-05",
    "client": "ACME",
    "engagement_start": "2026-05-23",
    "contact_email": "lead@acme.com",
    "dimensions": {d: _dim(f"stated {d}", f"source {d}") for d in DIMENSIONS},
    "mismatches": [],
    "signoff": {"signed_by": "lead@acme.com", "signed_at": "2026-05-23"},
    "verdict": "commit-record",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "intake",
    "client": "ACME",
    "engagement_start": "today",
    "contact_email": "team@acme.com",
    "dimensions": {"branching": {"stated": "trunk"}},
    "mismatches": [{"dimension": "commit_style", "stated": "squash", "observed": "merges", "resolution": ""}],
    "signoff": {},
    "verdict": "commit-record",
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
    ap.add_argument("--file", type=str, help="path to report JSON")
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
