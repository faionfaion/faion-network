#!/usr/bin/env python3
"""validate-changelog-automation-conventional-commits.py

Validate a changelog-update artefact JSON against schema + semver rule.

Inputs:
    --file PATH      path to changelog-update JSON
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

ID_RE = re.compile(r"^chg-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REL_VER_RE = re.compile(r"^v?\d+\.\d+\.\d+(-[a-z0-9.-]+)?$")
BUMPS = {"major", "minor", "patch"}
VERDICTS = {"emit-changelog", "block-non-conventional", "block-missing-version-bump", "block-merge-noise"}
SECTIONS_OPTIONAL = ("chore", "refactor", "docs", "perf", "test", "build", "ci", "style", "deviations")
MERGE_RE = re.compile(r"^Merge (branch|pull request) ", re.IGNORECASE)


def compute_bump(sections: dict) -> str:
    if sections.get("breaking"):
        return "major"
    if sections.get("feat"):
        return "minor"
    return "patch"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "range_from", "range_to", "release_version", "release_date", "sections", "semver_bump", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^chg-[a-z0-9-]{6,}$")
    if "release_version" in obj and not REL_VER_RE.match(str(obj["release_version"])):
        errs.append("release_version must be semver (v?MAJOR.MINOR.PATCH[-pre])")
    if "release_date" in obj and not DATE_RE.match(str(obj["release_date"])):
        errs.append("release_date must be ISO date YYYY-MM-DD")

    sec = obj.get("sections") or {}
    if not isinstance(sec, dict):
        errs.append("sections must be an object")
    else:
        for required_sec in ("breaking", "feat", "fix"):
            if required_sec not in sec or not isinstance(sec[required_sec], list):
                errs.append(f"sections.{required_sec} must be a list (possibly empty)")
        # Merge noise check.
        all_lines: list[str] = []
        for k in ("breaking", "feat", "fix", *SECTIONS_OPTIONAL):
            lst = sec.get(k) or []
            if isinstance(lst, list):
                all_lines.extend(lst)
        merge_hits = [ln for ln in all_lines if MERGE_RE.match(str(ln).strip())]
        if merge_hits:
            errs.append(f"merge-shaped lines present: {merge_hits[:3]} ... (r4 violation)")

    bump = obj.get("semver_bump")
    if bump not in BUMPS:
        errs.append(f"semver_bump must be one of {sorted(BUMPS)}")
    elif isinstance(sec, dict):
        computed = compute_bump(sec)
        if computed != bump:
            errs.append(f"semver_bump={bump} but computed={computed} from sections (r5 violation)")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    if verdict == "emit-changelog":
        devs = sec.get("deviations") if isinstance(sec, dict) else []
        if devs:
            errs.append("verdict=emit-changelog forbidden when sections.deviations non-empty")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "chg-v1-4-0",
    "range_from": "v1.3.0",
    "range_to": "HEAD",
    "release_version": "v1.4.0",
    "release_date": "2026-05-23",
    "semver_bump": "minor",
    "sections": {
        "breaking": [],
        "feat": ["(api) add /v2/quote endpoint"],
        "fix": ["(billing) FX rounding mismatch on EUR-PT"],
        "chore": ["bump deps"],
        "deviations": [],
    },
    "verdict": "emit-changelog",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "log",
    "range_from": "v1.3.0",
    "range_to": "HEAD",
    "release_version": "1.4",
    "release_date": "today",
    "semver_bump": "patch",
    "sections": {"breaking": ["drop /v1"], "feat": ["add /v2"], "fix": ["Merge branch foo"], "deviations": []},
    "verdict": "emit-changelog",
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
    ap.add_argument("--file", type=str, help="path to changelog-update JSON")
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
