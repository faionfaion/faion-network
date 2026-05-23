#!/usr/bin/env python3
"""validate-finetune-kickoff-checklist.py — validate a kickoff checklist.

Usage:
    validate-finetune-kickoff-checklist.py --checklist file.json
    validate-finetune-kickoff-checklist.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(d: dict) -> list[dict]:
    v: list[dict] = []
    req = ["workload", "owner", "created_at", "decision_record_ref",
           "baseline", "dataset", "holdout", "training_plan", "rollback", "budget_cap_usd"]
    for k in req:
        if k not in d:
            v.append({"rule": "schema", "message": f"missing: {k}"})
    if v:
        return v
    if not d["decision_record_ref"]:
        v.append({"rule": "rule:r1", "message": "decision_record_ref empty"})
    if d["owner"] in ("team", "TBD", ""):
        v.append({"rule": "rule:r1", "message": "owner not named"})
    if d["dataset"].get("total_examples", 0) < 1000:
        v.append({"rule": "rule:r1", "message": "dataset < 1000 examples"})
    if not d["dataset"].get("pii_audit_pass"):
        v.append({"rule": "rule:r5", "message": "pii_audit_pass must be true"})
    ho = d["holdout"]
    if ho.get("fraction", 0) < 0.10:
        v.append({"rule": "rule:r3", "message": f"holdout.fraction {ho.get('fraction')} < 0.10"})
    if not ho.get("disjoint_from_train"):
        v.append({"rule": "rule:r3", "message": "holdout not disjoint from train"})
    if not ho.get("stratified"):
        v.append({"rule": "rule:r3", "message": "holdout not stratified"})
    rb = d["rollback"]
    if not rb.get("plan") or len(rb["plan"]) < 50:
        v.append({"rule": "rule:r7", "message": "rollback.plan < 50 chars"})
    if not rb.get("dry_run_passed"):
        v.append({"rule": "rule:r7", "message": "rollback dry_run_passed not true"})
    if d["training_plan"].get("eval_cadence") not in ("per-epoch", "every-n-steps"):
        v.append({"rule": "rule:r6", "message": "eval_cadence not declared"})
    return v


def self_test() -> int:
    good = {
        "workload": "support-classifier", "owner": "ml-eng@example.com",
        "created_at": "2026-05-22", "decision_record_ref": "rfc/x.json",
        "budget_cap_usd": 1000,
        "baseline": {"score": 0.78, "eval_harness_commit": "a1b2c3d"},
        "dataset": {"total_examples": 6500, "dedup_dropped": 420, "pii_audit_pass": True},
        "holdout": {"fraction": 0.10, "disjoint_from_train": True, "stratified": True},
        "training_plan": {"eval_cadence": "per-epoch", "max_epochs": 3},
        "rollback": {"plan": "x" * 60, "canary_metric": "m", "dry_run_passed": True},
    }
    assert validate(good) == [], validate(good)
    bad = dict(good, owner="team",
               dataset={"total_examples": 200, "dedup_dropped": 0, "pii_audit_pass": False},
               holdout={"fraction": 0.02, "disjoint_from_train": False, "stratified": False},
               rollback={"plan": "TBD", "canary_metric": "x", "dry_run_passed": False})
    out = validate(bad)
    assert any(x["rule"] == "rule:r3" for x in out), out
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checklist", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.checklist:
        ap.error("--checklist required")
        return 2
    out = validate(json.loads(args.checklist.read_text(encoding="utf-8")))
    sys.stdout.write(json.dumps({"ok": not out, "violations": out}, indent=2) + "\n")
    return 0 if not out else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
