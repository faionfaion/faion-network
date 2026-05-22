#!/usr/bin/env python3
"""validate-decision-framework.py

Validate a decision-record JSON against content/02-output-contract.xml.

Inputs:
    --file PATH      path to decision-record JSON
    --self-test      run built-in fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ID_RE = re.compile(r"^dr-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
APPROACHES = {"prompt", "rag", "fine-tune", "hybrid-rag-ft"}
TIERS = {"nano", "mini", "standard", "frontier"}
SPECS = {"none", "behavioral", "factual"}
FREQ = {"never", "monthly", "weekly", "daily", "hourly"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "feature", "approach", "model_tier", "model_id", "specialization_class",
              "data_inventory", "volume_estimate", "rationale", "quarterly_review_due", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^dr-[a-z0-9-]{6,}$")
    if "approach" in obj and obj["approach"] not in APPROACHES:
        errs.append(f"approach must be one of {sorted(APPROACHES)}")
    if "model_tier" in obj and obj["model_tier"] not in TIERS:
        errs.append(f"model_tier must be one of {sorted(TIERS)}")
    if "specialization_class" in obj and obj["specialization_class"] not in SPECS:
        errs.append(f"specialization_class must be one of {sorted(SPECS)}")
    inv = obj.get("data_inventory") or {}
    if not isinstance(inv, dict):
        errs.append("data_inventory must be object")
    else:
        if not isinstance(inv.get("private"), bool):
            errs.append("data_inventory.private must be bool")
        if inv.get("change_frequency") not in FREQ:
            errs.append(f"data_inventory.change_frequency must be one of {sorted(FREQ)}")
        if not isinstance(inv.get("citations_required"), bool):
            errs.append("data_inventory.citations_required must be bool")
        cs = inv.get("corpus_size")
        if not isinstance(cs, int) or cs < 0:
            errs.append("data_inventory.corpus_size must be int >= 0")
    vol = obj.get("volume_estimate") or {}
    rpm = vol.get("requests_per_month")
    if not isinstance(rpm, int) or rpm < 0:
        errs.append("volume_estimate.requests_per_month must be int >= 0")
    rat = obj.get("rationale") or {}
    if not isinstance(rat, dict):
        errs.append("rationale must be object")
    else:
        ar = rat.get("approach_reason", "")
        if not isinstance(ar, str) or len(ar) < 30:
            errs.append("rationale.approach_reason must be string of length >= 30")
        mr = rat.get("model_reason", "")
        if not isinstance(mr, str) or len(mr) < 30:
            errs.append("rationale.model_reason must be string of length >= 30")
    # rule no-fine-tune-for-factual
    if obj.get("approach") == "fine-tune" and obj.get("specialization_class") == "factual":
        errs.append("approach=fine-tune forbidden with specialization_class=factual (rule no-fine-tune-for-factual)")
    # rule fine-tune-only-at-scale-for-behavior
    if obj.get("approach") == "fine-tune":
        if rpm is not None and isinstance(rpm, int) and rpm < 1_000_000:
            errs.append(f"approach=fine-tune requires requests_per_month >= 1000000 (got {rpm}; rule fine-tune-only-at-scale-for-behavior)")
        if not rat.get("ft_roi_calc"):
            errs.append("approach=fine-tune requires rationale.ft_roi_calc")
    # rule quarterly-review-clause
    if "quarterly_review_due" in obj:
        q = obj["quarterly_review_due"]
        if not DATE_RE.match(str(q)):
            errs.append("quarterly_review_due must be ISO date")
        else:
            try:
                qd = date.fromisoformat(q)
                today = date.today()
                if not (today + timedelta(days=1) <= qd <= today + timedelta(days=120)):
                    errs.append("quarterly_review_due must be in [today+1, today+120] (rule quarterly-review-clause)")
            except ValueError:
                errs.append("quarterly_review_due unparseable")
    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


def _today_plus(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


VALID = {
    "artefact_id": "dr-support-bot",
    "feature": "support-bot-tier1",
    "approach": "rag",
    "model_tier": "standard",
    "model_id": "claude-sonnet-4-6",
    "specialization_class": "factual",
    "data_inventory": {"private": True, "change_frequency": "weekly", "citations_required": True, "corpus_size": 4200},
    "volume_estimate": {"requests_per_month": 90000, "irreversible_error": False},
    "rationale": {
        "approach_reason": "Private corpus, weekly updates, citations are a hard product requirement.",
        "model_reason": "Standard generation; no irreversible-error; Sonnet hits SLO at half Opus cost.",
    },
    "quarterly_review_due": _today_plus(90),
    "version": "1.1.0",
    "last_reviewed": date.today().isoformat(),
}

INVALID = {
    "artefact_id": "x",
    "feature": "f",
    "approach": "fine-tune",
    "model_tier": "frontier",
    "specialization_class": "factual",
    "data_inventory": {"private": True, "change_frequency": "daily", "citations_required": True, "corpus_size": 10000},
    "volume_estimate": {"requests_per_month": 5000},
    "rationale": {"approach_reason": "want quality", "model_reason": "best model"},
    "quarterly_review_due": "2020-01-01",
    "model_id": "x",
}


def self_test() -> int:
    errs = validate(VALID)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid rejected: {errs}\n")
        return 1
    errs = validate(INVALID)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid accepted\n")
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
