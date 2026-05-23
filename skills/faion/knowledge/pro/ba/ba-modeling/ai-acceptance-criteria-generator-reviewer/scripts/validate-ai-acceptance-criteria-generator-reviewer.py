#!/usr/bin/env python3
"""validate-ai-acceptance-criteria-generator-reviewer.py

Validate a reviewer-rubric artefact against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to rubric JSON
    --self-test       run built-in fixtures (OK + BAD)
    --help            this message

Outputs:
    stdout = "OK" on pass; stderr = "VIOLATION: ..." lines on fail.

Exit codes:
    0 = valid
    1 = invalid (violations printed)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_TOP = ("dimensions", "instance_scores", "rater_count", "weighted_total", "weights_locked_at")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    dims = obj.get("dimensions", [])
    if not isinstance(dims, list) or len(dims) < 3:
        errs.append("dimensions must be array with >= 3 items")
    else:
        for i, d in enumerate(dims):
            if not isinstance(d, dict):
                errs.append(f"dimensions[{i}] must be object")
                continue
            if "anchors_1_3_5" not in d:
                errs.append(f"dimensions[{i}] missing anchors_1_3_5 (rule r1)")
            else:
                a = d["anchors_1_3_5"]
                if not all(k in a for k in ("1", "3", "5")):
                    errs.append(f"dimensions[{i}].anchors_1_3_5 missing 1/3/5 (rule r1)")
            if "weight" not in d:
                errs.append(f"dimensions[{i}] missing weight")
    scores = obj.get("instance_scores", [])
    if not isinstance(scores, list) or len(scores) < 1:
        errs.append("instance_scores must have >= 1 entry")
    else:
        for i, inst in enumerate(scores):
            for j, ds in enumerate(inst.get("dimension_scores", [])):
                if not ds.get("evidence_refs"):
                    errs.append(
                        f"instance_scores[{i}].dimension_scores[{j}] missing evidence_refs (rule r2)"
                    )
    rc = obj.get("rater_count", 0)
    dvu = obj.get("decision_value_usd", 0)
    if isinstance(rc, int) and isinstance(dvu, (int, float)) and dvu >= 10000 and rc < 2:
        errs.append("single-rater on decision_value_usd >= 10000 (rule r3)")
    return errs


OK_FIXTURE = {
    "dimensions": [
        {"name": "happy", "anchors_1_3_5": {"1": "no", "3": "one", "5": "all"}, "weight": 0.5},
        {"name": "neg", "anchors_1_3_5": {"1": "no", "3": "some", "5": "all"}, "weight": 0.3},
        {"name": "edge", "anchors_1_3_5": {"1": "no", "3": "b", "5": "b+null"}, "weight": 0.2},
    ],
    "instance_scores": [
        {
            "instance_id": "AC-1",
            "dimension_scores": [
                {"dimension": "happy", "score": 5, "evidence_refs": ["d.md#L1"]},
                {"dimension": "neg", "score": 3, "evidence_refs": ["d.md#L2"]},
                {"dimension": "edge", "score": 4, "evidence_refs": ["d.md#L3"]},
            ],
        }
    ],
    "rater_count": 2,
    "weighted_total": 78.0,
    "weights_locked_at": "2026-05-23T09:00:00Z",
}
BAD_FIXTURE = {
    "dimensions": [
        {"name": "happy", "anchors_1_3_5": {"1": "x", "3": "y", "5": "z"}, "weight": 1.0}
    ],
    "instance_scores": [
        {
            "instance_id": "AC-1",
            "dimension_scores": [{"dimension": "happy", "score": 5, "evidence_refs": []}],
        }
    ],
    "rater_count": 1,
    "weighted_total": 100.0,
    "weights_locked_at": "2026-05-23T09:00:00Z",
    "decision_value_usd": 50000,
}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK fixture rejected\n")
        return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
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
