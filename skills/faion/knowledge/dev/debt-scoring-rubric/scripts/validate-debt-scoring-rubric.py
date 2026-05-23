#!/usr/bin/env python3
"""validate-debt-scoring-rubric.py

Validate a debt-register JSON against schema + formula rule.

Inputs:
    --file PATH      path to register JSON
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

ID_RE = re.compile(r"^dsr-[a-z0-9-]{6,}$")
ITEM_ID_RE = re.compile(r"^debt-[a-z0-9-]{4,}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
CATEGORIES = {"architecture", "code", "test", "design", "infra", "dependency", "documentation"}
CONFIDENCE = {"high", "medium", "low"}
VERDICTS = {"publish-register", "block-missing-anchors", "block-formula-mismatch", "block-no-evidence"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "anchors_signed_off_by", "items", "threshold", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^dsr-[a-z0-9-]{6,}$")
    em = str(obj.get("anchors_signed_off_by", ""))
    if em and not EMAIL_RE.match(em):
        errs.append("anchors_signed_off_by must be valid email")

    items = obj.get("items") or []
    if not isinstance(items, list) or len(items) < 5:
        errs.append("items must be a list of at least 5 entries")
    else:
        for i, it in enumerate(items):
            if not ITEM_ID_RE.match(str(it.get("item_id", ""))):
                errs.append(f"items[{i}].item_id must match ^debt-[a-z0-9-]{{4,}}$")
            if it.get("category") not in CATEGORIES:
                errs.append(f"items[{i}].category must be one of {sorted(CATEGORIES)}")
            factors = it.get("factors") or {}
            for f in ("user_impact", "change_frequency", "fragility", "blast_radius", "fix_cost"):
                v = factors.get(f)
                if not isinstance(v, int) or not (1 <= v <= 5):
                    errs.append(f"items[{i}].factors.{f} must be int in [1,5]")
            if it.get("confidence") not in CONFIDENCE:
                errs.append(f"items[{i}].confidence must be one of {sorted(CONFIDENCE)}")
            ev = it.get("evidence") or {}
            for src in ("change_freq_source", "fragility_source", "blast_source"):
                if not str(ev.get(src, "")).strip():
                    errs.append(f"items[{i}].evidence.{src} missing or empty")
            wci = it.get("what_changes_if_paid")
            if not isinstance(wci, str) or len(wci) < 10:
                errs.append(f"items[{i}].what_changes_if_paid must be string of length >= 10")
            # Formula check.
            if all(isinstance(factors.get(f), int) for f in ("user_impact", "change_frequency", "fragility", "blast_radius", "fix_cost")):
                computed = (factors["user_impact"] * factors["change_frequency"] * factors["fragility"] * factors["blast_radius"]) / factors["fix_cost"]
                score = it.get("score")
                if not isinstance(score, (int, float)) or abs(score - computed) > 0.01:
                    errs.append(f"items[{i}].score={score} does not match computed={computed} (formula mismatch)")

    th = obj.get("threshold")
    if not isinstance(th, (int, float)) or th < 0:
        errs.append("threshold must be non-negative number")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


def _item(idx):
    factors = {"user_impact": 4, "change_frequency": 5, "fragility": 4, "blast_radius": 3, "fix_cost": 3}
    score = (factors["user_impact"] * factors["change_frequency"] * factors["fragility"] * factors["blast_radius"]) / factors["fix_cost"]
    return {
        "item_id": f"debt-item{idx:03d}",
        "title": f"Debt item {idx}",
        "category": "architecture",
        "factors": factors,
        "score": score,
        "confidence": "medium",
        "evidence": {"change_freq_source": "git log", "fragility_source": "tracker", "blast_source": "service map"},
        "what_changes_if_paid": "Significantly reduces churn pain.",
    }


VALID_FIXTURE = {
    "artefact_id": "dsr-q2-2026",
    "anchors_signed_off_by": "pm@acme.com",
    "anchors_signed_off_at": "2026-05-20",
    "items": [_item(i) for i in range(5)],
    "threshold": 30,
    "verdict": "publish-register",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "debt",
    "anchors_signed_off_by": "team@",
    "items": [{"item_id": "x", "title": "fix", "category": "stuff", "factors": {"user_impact": 9}, "score": 999, "confidence": "very-high"}],
    "threshold": -5,
    "verdict": "publish-register",
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
    ap.add_argument("--file", type=str, help="path to debt-register JSON")
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
