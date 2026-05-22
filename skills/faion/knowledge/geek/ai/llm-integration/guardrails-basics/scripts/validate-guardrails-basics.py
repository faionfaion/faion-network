#!/usr/bin/env python3
"""Validate output contract for guardrails-basics spec.

USAGE:
    validate-guardrails-basics.py <input.json>   Validate a guardrails-spec.json.
    validate-guardrails-basics.py --self-test    Run built-in fixture.
    validate-guardrails-basics.py --help         Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALLOWED_LAYER_TYPES = {"regex_filter", "length_cap", "output_schema", "llm_classifier"}
ALLOWED_KINDS = {"input", "output", "both"}
MAX_BUDGET_MS = 2000


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be an object"]
    for k in ("layers", "fail_closed", "latency_budget_ms"):
        if k not in c:
            v.append(f"missing required field: {k}")
    layers = c.get("layers") or []
    if not isinstance(layers, list) or len(layers) < 4:
        v.append("layers must be an array of >=4 entries (rule r1)")
    seen_orders: list[int] = []
    classifier_order = None
    max_order = -1
    for i, layer in enumerate(layers if isinstance(layers, list) else []):
        if not isinstance(layer, dict):
            v.append(f"layers[{i}] must be object")
            continue
        for k in ("type", "kind", "order"):
            if k not in layer:
                v.append(f"layers[{i}] missing {k}")
        if layer.get("type") not in ALLOWED_LAYER_TYPES:
            v.append(f"layers[{i}].type invalid: {layer.get('type')!r}")
        if layer.get("kind") not in ALLOWED_KINDS:
            v.append(f"layers[{i}].kind invalid: {layer.get('kind')!r}")
        o = layer.get("order")
        if isinstance(o, int):
            seen_orders.append(o)
            max_order = max(max_order, o)
            if layer.get("type") == "llm_classifier":
                classifier_order = o
    if classifier_order is not None and classifier_order != max_order:
        v.append("llm_classifier must have the highest order (rule r4)")
    if c.get("fail_closed") is not True:
        v.append("fail_closed must be true (rule r5)")
    b = c.get("latency_budget_ms")
    if isinstance(b, int) and b > MAX_BUDGET_MS:
        v.append(f"latency_budget_ms must be <= {MAX_BUDGET_MS}")
    if seen_orders and len(seen_orders) != len(set(seen_orders)):
        v.append("layer orders must be unique")
    return v


def _self_test() -> int:
    good = {
        "layers": [
            {"type": "regex_filter", "kind": "input", "order": 1},
            {"type": "length_cap", "kind": "both", "order": 2},
            {"type": "output_schema", "kind": "output", "order": 3},
            {"type": "llm_classifier", "kind": "both", "order": 4},
        ],
        "fail_closed": True,
        "latency_budget_ms": 900,
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = {"layers": [{"type": "llm_classifier", "kind": "both", "order": 1}],
           "fail_closed": False, "latency_budget_ms": 5000}
    out = validate(bad)
    assert any(">=4" in x or ">= 4" in x for x in out), "should reject <4 layers"
    assert any("fail_closed" in x for x in out), "should reject fail_closed=false"
    bad2 = dict(good)
    bad2["layers"] = [{"type": "llm_classifier", "kind": "both", "order": 1}] + good["layers"][:3]
    assert any("llm_classifier" in x for x in validate(bad2)), "should reject classifier-not-last"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-guardrails-basics.py")
    p.add_argument("path", nargs="?", help="JSON spec to validate")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
