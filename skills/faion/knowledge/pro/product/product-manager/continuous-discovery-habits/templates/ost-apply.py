#!/usr/bin/env python3
"""
ost-apply.py — apply OST diffs emitted by agents.
Usage: python ost-apply.py <ost.yaml> <diff.yaml>
The diff format is the schema defined in ost.yaml under 'diffs:'.
PM reviews the diff file before running this script.
Operations: add (new opportunity), update (patch fields), park (set status=parked),
            archive (remove from active tree).
"""
import sys, yaml, copy
from pathlib import Path


def apply_diff(ost: dict, diff: dict) -> dict:
    out = copy.deepcopy(ost)
    by_id = {o["id"]: o for o in out.get("opportunities", [])}

    for op in diff.get("add", []):
        if op["id"] in by_id:
            raise SystemExit(f"add: id already exists: {op['id']}")
        out["opportunities"].append(op)
        by_id[op["id"]] = op

    for op in diff.get("update", []):
        if op["id"] not in by_id:
            raise SystemExit(f"update: missing opportunity: {op['id']}")
        by_id[op["id"]].update(op)

    for op_id in diff.get("park", []):
        if op_id not in by_id:
            raise SystemExit(f"park: missing opportunity: {op_id}")
        by_id[op_id]["status"] = "parked"

    for op_id in diff.get("archive", []):
        out["opportunities"] = [
            o for o in out["opportunities"] if o["id"] != op_id
        ]

    return out


if __name__ == "__main__":
    ost_path = Path(sys.argv[1])
    diff_path = Path(sys.argv[2])
    ost = yaml.safe_load(ost_path.read_text())
    diff = yaml.safe_load(diff_path.read_text())
    result = apply_diff(ost, diff.get("diffs", diff))
    ost_path.write_text(yaml.safe_dump(result, sort_keys=False, allow_unicode=True))
    print(f"Applied diff from {diff_path} to {ost_path}")
