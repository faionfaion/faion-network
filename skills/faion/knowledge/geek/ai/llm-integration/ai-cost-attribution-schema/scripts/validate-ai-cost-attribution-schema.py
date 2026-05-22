#!/usr/bin/env python3
"""validate-ai-cost-attribution-schema.py — validate attribution records.

Usage:
    validate-ai-cost-attribution-schema.py --records <path-to-jsonl-or-json>
    validate-ai-cost-attribution-schema.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["request_id", "ts", "tenant_id", "feature", "route", "model", "prompt_cache_hit", "input_tokens", "output_tokens", "latency_ms", "cost_usd"]
GENERIC = re.compile(r"^(team|us|unknown|tbd|n/a)$", re.IGNORECASE)


def validate_one(r: dict, idx: int) -> list[dict]:
    v: list[dict] = []
    for k in REQUIRED:
        if k not in r:
            v.append({"rule": "r1", "field": f"records[{idx}].{k}", "msg": "missing"})
    if v:
        return v
    if GENERIC.fullmatch(str(r.get("tenant_id", ""))):
        v.append({"rule": "r3", "field": f"records[{idx}].tenant_id", "msg": "tenant_id is generic"})
    if not isinstance(r.get("prompt_cache_hit"), bool):
        v.append({"rule": "r1", "field": f"records[{idx}].prompt_cache_hit", "msg": "must be boolean"})
    if r.get("input_tokens", -1) < 0 or r.get("output_tokens", -1) < 0:
        v.append({"rule": "r1", "field": f"records[{idx}].tokens", "msg": "token counts must be >=0"})
    if not r.get("pricing_snapshot_id"):
        v.append({"rule": "r4", "field": f"records[{idx}].pricing_snapshot_id", "msg": "snapshot id required"})
    return v


def validate(records: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, r in enumerate(records):
        out.extend(validate_one(r, i))
    return out


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate([smoke]) == [], f"smoke must pass: {validate([smoke])}"
    bad = dict(smoke); bad["tenant_id"] = "unknown"
    assert any(x["rule"] == "r3" for x in validate([bad]))
    bad2 = dict(smoke); bad2["prompt_cache_hit"] = "yes"
    assert any(x["rule"] == "r1" for x in validate([bad2]))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--records", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.records:
        ap.error("--records required")
        return 2
    raw = args.records.read_text(encoding="utf-8").strip()
    if raw.startswith("["):
        recs = json.loads(raw)
    elif raw.startswith("{") and "\n" not in raw:
        recs = [json.loads(raw)]
    else:
        recs = [json.loads(line) for line in raw.splitlines() if line.strip() and not line.startswith('{"_')]
    v = validate(recs)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
