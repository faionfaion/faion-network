#!/usr/bin/env python3
"""validate-qa-changed-lines-coverage-dashboard.py

Validate a diff-coverage artefact produced by the
qa-changed-lines-coverage-dashboard methodology against the JSON Schema in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in ("policy", "pr_comment", "dashboard"):
        if k not in obj:
            errs.append(f"missing required top-level field: {k}")
    policy = obj.get("policy")
    if isinstance(policy, dict):
        for k in ("default_threshold", "overrides", "report_full_repo_trend"):
            if k not in policy:
                errs.append(f"policy.{k} missing")
        dt = policy.get("default_threshold")
        if isinstance(dt, int):
            if dt < 1 or dt > 100:
                errs.append("policy.default_threshold must be 1..100 (0 disables the gate)")
        elif "default_threshold" in policy:
            errs.append("policy.default_threshold must be integer")
        overrides = policy.get("overrides", [])
        if not isinstance(overrides, list):
            errs.append("policy.overrides must be array")
        else:
            for i, o in enumerate(overrides):
                if not isinstance(o, dict):
                    errs.append(f"policy.overrides[{i}] not an object")
                    continue
                for k in ("paths", "threshold", "reason"):
                    if k not in o:
                        errs.append(f"policy.overrides[{i}].{k} missing")
                reason = o.get("reason", "")
                if isinstance(reason, str) and len(reason) < 10:
                    errs.append(f"policy.overrides[{i}].reason must be at least 10 characters")
                th = o.get("threshold")
                if isinstance(th, int) and (th < 0 or th > 100):
                    errs.append(f"policy.overrides[{i}].threshold must be 0..100")
        if "report_full_repo_trend" in policy and not isinstance(policy["report_full_repo_trend"], bool):
            errs.append("policy.report_full_repo_trend must be boolean")
    pr = obj.get("pr_comment")
    if isinstance(pr, dict):
        for k in ("headline_metric", "per_file", "merge_gate_verdict"):
            if k not in pr:
                errs.append(f"pr_comment.{k} missing")
        if pr.get("headline_metric") not in (None, "diff_coverage_percent"):
            errs.append("pr_comment.headline_metric must be diff_coverage_percent")
        verdict = pr.get("merge_gate_verdict")
        if verdict not in (None, "pass", "fail"):
            errs.append("pr_comment.merge_gate_verdict must be pass|fail")
        per_file = pr.get("per_file", [])
        if not isinstance(per_file, list):
            errs.append("pr_comment.per_file must be array")
        else:
            any_fail = False
            for i, row in enumerate(per_file):
                if not isinstance(row, dict):
                    errs.append(f"pr_comment.per_file[{i}] not an object")
                    continue
                for k in ("path", "percent", "gate_pass"):
                    if k not in row:
                        errs.append(f"pr_comment.per_file[{i}].{k} missing")
                pct = row.get("percent")
                if isinstance(pct, int) and (pct < 0 or pct > 100):
                    errs.append(f"pr_comment.per_file[{i}].percent must be 0..100")
                if row.get("gate_pass") is False:
                    any_fail = True
            if any_fail and verdict == "pass":
                errs.append("pr_comment.merge_gate_verdict=pass while some per_file row gate_pass=false (aggregate masking)")
    db = obj.get("dashboard")
    if isinstance(db, dict):
        for k in ("timestamp", "median_diff_coverage_7d", "median_diff_coverage_30d", "low_coverage_files", "exclusion_list_size"):
            if k not in db:
                errs.append(f"dashboard.{k} missing")
        if "exclusion_list_size" in db and not isinstance(db["exclusion_list_size"], int):
            errs.append("dashboard.exclusion_list_size must be integer")
        if "low_coverage_files" in db and not isinstance(db["low_coverage_files"], list):
            errs.append("dashboard.low_coverage_files must be array")
    return errs


def self_test() -> int:
    good = {
        "policy": {
            "default_threshold": 80,
            "overrides": [
                {"paths": ["billing/**"], "threshold": 90, "reason": "money-touching code needs higher floor"}
            ],
            "report_full_repo_trend": True,
        },
        "pr_comment": {
            "headline_metric": "diff_coverage_percent",
            "per_file": [{"path": "src/signup.py", "percent": 92, "gate_pass": True}],
            "full_repo_trend_line": "trend: 78.4% (-0.1pp)",
            "merge_gate_verdict": "pass",
        },
        "dashboard": {
            "timestamp": "2026-05-23T10:00:00Z",
            "median_diff_coverage_7d": 84.2,
            "median_diff_coverage_30d": 82.7,
            "low_coverage_files": ["src/legacy/forms.py"],
            "exclusion_list_size": 4,
        },
    }
    errs = validate(good)
    if errs:
        sys.stderr.write("self-test: good fixture rejected: " + json.dumps(errs) + "\n")
        return 1
    bad = {
        "policy": {
            "default_threshold": 0,
            "overrides": [{"paths": ["billing/**"], "threshold": 90}],
            "report_full_repo_trend": True,
        },
        "pr_comment": {
            "headline_metric": "whole_repo_coverage_percent",
            "merge_gate_verdict": "pass",
        },
    }
    if not validate(bad):
        sys.stderr.write("self-test: bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
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
