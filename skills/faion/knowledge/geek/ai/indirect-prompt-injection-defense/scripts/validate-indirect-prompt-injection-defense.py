#!/usr/bin/env python3
"""validate-indirect-prompt-injection-defense.py — validate a defense-spec.json against the output contract.

Usage:
    validate-indirect-prompt-injection-defense.py --spec <path-to-defense-spec.json>
    validate-indirect-prompt-injection-defense.py --self-test

Inputs: a JSON file matching templates/defense-spec.schema.json.
Outputs: stdout JSON {ok: bool, violations: [...]}
Exit codes: 0 = pass, 1 = violations found, 2 = bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_TOP = ["agent_name", "boundaries", "untrusted_sources", "taint_rules", "tool_scopes", "canary", "eval_set"]
CHANNELS = {"system", "user", "tool", "memory", "rag"}
TRUST = {"untrusted", "partially_trusted", "trusted"}
SPLIT = {"single_llm", "dual_llm_planner_reader", "n_llm_pipeline"}
OUTBOUND = {"abort_on_match", "log_on_match"}


def validate(spec: dict) -> list[dict]:
    v: list[dict] = []
    for k in REQUIRED_TOP:
        if k not in spec:
            v.append({"rule": "schema", "field": k, "msg": "missing required field"})
    if v:
        return v
    if not isinstance(spec["boundaries"], list) or len(spec["boundaries"]) < 3:
        v.append({"rule": "r1", "field": "boundaries", "msg": "need >=3 trust boundaries"})
    for i, b in enumerate(spec.get("boundaries", [])):
        if b.get("channel") not in CHANNELS:
            v.append({"rule": "schema", "field": f"boundaries[{i}].channel", "msg": f"channel must be one of {CHANNELS}"})
    sources = spec.get("untrusted_sources", [])
    if not sources:
        v.append({"rule": "r1", "field": "untrusted_sources", "msg": "declare at least one untrusted source"})
    for i, s in enumerate(sources):
        if s.get("trust_level") not in TRUST:
            v.append({"rule": "schema", "field": f"untrusted_sources[{i}].trust_level", "msg": "invalid trust_level"})
    taint = spec.get("taint_rules", [])
    if not taint:
        v.append({"rule": "r2", "field": "taint_rules", "msg": "no taint_rules but untrusted_sources present"})
    for i, s in enumerate(sources):
        pat = s.get("source", "")
        matched = any(re.fullmatch(t.get("source_pattern", ""), pat) or re.search(t.get("source_pattern", "^$"), pat) for t in taint)
        if not matched:
            v.append({"rule": "r2", "field": f"untrusted_sources[{i}].source", "msg": f"no taint_rule matches source '{pat}'"})
    split = spec.get("split_pattern")
    if split not in SPLIT:
        v.append({"rule": "schema", "field": "split_pattern", "msg": f"split_pattern must be one of {SPLIT}"})
    canary = spec.get("canary") or {}
    if not canary.get("token_format"):
        v.append({"rule": "r5", "field": "canary.token_format", "msg": "canary token_format required"})
    if canary.get("outbound_check") not in OUTBOUND:
        v.append({"rule": "r5", "field": "canary.outbound_check", "msg": f"outbound_check must be one of {OUTBOUND}"})
    eset = spec.get("eval_set") or {}
    if eset.get("min_categories", 0) < 10:
        v.append({"rule": "r7", "field": "eval_set.min_categories", "msg": "need >=10 adversarial categories"})
    if eset.get("min_cases", 0) < 20:
        v.append({"rule": "r7", "field": "eval_set.min_cases", "msg": "need >=20 eval cases total"})
    for i, t in enumerate(spec.get("tool_scopes", [])):
        if "allowed_paths" not in t or "allowed_hosts" not in t:
            v.append({"rule": "r4", "field": f"tool_scopes[{i}]", "msg": "tool scope must declare allowed_paths AND allowed_hosts"})
    return v


def self_test() -> int:
    valid = {
        "agent_name": "rss-summariser",
        "boundaries": [
            {"id": "b1", "label": "dev", "channel": "system"},
            {"id": "b2", "label": "user", "channel": "user"},
            {"id": "b3", "label": "rss", "channel": "tool"},
        ],
        "untrusted_sources": [{"source": "rss_item_body", "trust_level": "untrusted", "max_size_kb": 16, "content_type": "text/html"}],
        "taint_rules": [{"source_pattern": "rss_.*", "wrap_with": "<u>{}</u>", "max_quote_chars": 8000}],
        "split_pattern": "single_llm",
        "tool_scopes": [{"tool": "fetch_rss", "allowed_paths": [], "allowed_hosts": ["feeds.example.com"]}],
        "canary": {"token_format": "CANARY-{uuid}", "outbound_check": "abort_on_match"},
        "eval_set": {"path": "evals/ipi/", "min_categories": 10, "min_cases": 20},
    }
    assert validate(valid) == [], f"valid spec should pass: {validate(valid)}"
    bad = dict(valid)
    bad["boundaries"] = [valid["boundaries"][0]]
    assert any(x["rule"] == "r1" for x in validate(bad)), "should flag missing boundaries"
    bad2 = dict(valid)
    bad2["canary"] = {"token_format": "", "outbound_check": "abort_on_match"}
    assert any(x["rule"] == "r5" for x in validate(bad2)), "should flag missing canary token"
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", type=Path, help="Path to defense-spec.json")
    ap.add_argument("--self-test", action="store_true", help="Run built-in fixture")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.spec:
        ap.error("--spec required")
        return 2
    data = json.loads(args.spec.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
