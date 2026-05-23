#!/usr/bin/env python3
"""validate-spatial-computing-overview.py

Validate a spatial-computing platform-selection decision-record JSON against
the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to decision-record JSON
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

VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
USE_CASES = {"productivity", "entertainment", "training", "industrial", "social"}
AUDIENCES = {"consumer", "prosumer", "enterprise"}
CONTENT_TYPES = {"floating-windows", "cinematic-video", "dialogue-agent", "interactive-simulation",
                 "3d-model-inspection", "active-gaming", "spatial-overlay"}
PLATFORMS = {"visionos", "quest", "psvr2", "hololens", "android-xr", "webxr"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__")
    else:
        if hdr.get("methodology") != "spatial-computing-overview":
            errs.append("header methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("header version not semver")
        if hdr.get("produces") != "decision-record":
            errs.append("header produces mismatch")
    if "decision_date" not in obj or not DATE_RE.match(str(obj["decision_date"])):
        errs.append("decision_date missing or not ISO")
    if obj.get("use_case") not in USE_CASES:
        errs.append("use_case invalid")
    if obj.get("audience") not in AUDIENCES:
        errs.append("audience invalid")
    cts = obj.get("content_types") or []
    if not isinstance(cts, list) or not cts:
        errs.append("content_types must be non-empty list")
    else:
        for c in cts:
            if c not in CONTENT_TYPES:
                errs.append(f"content_types invalid: {c}")
    scoring = obj.get("scoring") or []
    if not isinstance(scoring, list) or len(scoring) < 2:
        errs.append("scoring must contain >=2 platforms")
    else:
        for i, s in enumerate(scoring):
            if s.get("platform") not in PLATFORMS:
                errs.append(f"scoring[{i}].platform invalid")
            for k in ("install_base", "sdk_maturity", "audience_fit", "content_type_fit", "store_constraints"):
                v = s.get(k)
                if not isinstance(v, int) or not (0 <= v <= 5):
                    errs.append(f"scoring[{i}].{k} must be int 0-5")
            ev = s.get("evidence_sources") or []
            if not isinstance(ev, list) or not ev:
                errs.append(f"scoring[{i}].evidence_sources missing")
    rec = obj.get("recommendation") or {}
    if rec.get("primary") not in PLATFORMS:
        errs.append("recommendation.primary invalid")
    fb = rec.get("fallback") or []
    if not isinstance(fb, list) or not fb:
        errs.append("recommendation.fallback must be non-empty list")
    if len(str(rec.get("rationale", ""))) < 40:
        errs.append("recommendation.rationale must be >=40 chars")
    risk = rec.get("risk_notes") or []
    if not isinstance(risk, list) or not risk:
        errs.append("recommendation.risk_notes must be non-empty list")
    return errs


OK = {
    "__faion_header__": {"methodology": "spatial-computing-overview", "version": "1.1.0", "produces": "decision-record"},
    "decision_date": "2026-05-23",
    "use_case": "productivity",
    "audience": "prosumer",
    "content_types": ["floating-windows"],
    "scoring": [
        {"platform": "visionos", "install_base": 3, "sdk_maturity": 4, "audience_fit": 5, "content_type_fit": 5, "store_constraints": 3, "evidence_sources": ["IDC 2025"]},
        {"platform": "webxr", "install_base": 4, "sdk_maturity": 3, "audience_fit": 3, "content_type_fit": 3, "store_constraints": 5, "evidence_sources": ["caniuse 2026"]},
    ],
    "recommendation": {"primary": "visionos", "fallback": ["webxr"], "rationale": "Best fit for prosumer + content; fallback for reach", "risk_notes": ["small install base"]},
}
BAD = {"use_case": "productivity", "scoring": [{"platform": "visionos"}], "recommendation": {"primary": "visionos"}}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
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
