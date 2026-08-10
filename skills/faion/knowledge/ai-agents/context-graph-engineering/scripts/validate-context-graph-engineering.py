#!/usr/bin/env python3
"""Validate a Graph Design Record against the context-graph-engineering contract.

Usage:
  validate-context-graph-engineering.py <gdr.yaml|gdr.json>
  validate-context-graph-engineering.py --self-test
  validate-context-graph-engineering.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

WARRANTS = {"m_to_n", "cross_links", "cycles", "temporal", "none"}
ALTERNATIVES = {"flat", "tree", "hybrid"}
REQUIRED_CHECKS = {"referential", "orphans", "acyclicity"}
GATE_KEYS = ("system", "warrant", "warrant_evidence", "rejected_alternative")
FULL_KEYS = (
    "cost_incumbent_tokens",
    "cost_graph_tokens",
    "edge_types",
    "supernode_cap",
    "max_hops",
    "max_fanout",
    "worst_case_nodes",
    "context_budget_tokens",
    "ranking_function",
    "integrity_checks",
    "rebuild_trigger",
)
# Conservative per-node cost used to prove the traversal budget fits (r5).
ASSUMED_TOKENS_PER_NODE = 80


def worst_case(fanout: int, hops: int) -> int:
    return sum(fanout**i for i in range(hops + 1))


def violations(gdr: dict) -> list[str]:
    errs: list[str] = []

    for key in GATE_KEYS:
        if key not in gdr:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    warrant = gdr["warrant"]
    if warrant not in WARRANTS:
        errs.append(f"warrant {warrant!r} not in {sorted(WARRANTS)} (r1-graph-warrant)")
    if len(str(gdr["warrant_evidence"]).strip()) < 40:
        errs.append("warrant_evidence must be >=40 chars of concrete evidence (r1-graph-warrant)")
    if gdr["rejected_alternative"] not in ALTERNATIVES:
        errs.append(f"rejected_alternative must be one of {sorted(ALTERNATIVES)}")

    # The gate: warrant none means the record is complete AND must not specify a graph.
    if warrant == "none":
        leaked = [k for k in FULL_KEYS if k in gdr]
        if leaked:
            errs.append(
                "warrant is 'none' so the record MUST stop; remove graph design keys: "
                + ", ".join(sorted(leaked))
                + " (r1-graph-warrant)"
            )
        return errs

    for key in FULL_KEYS:
        if key not in gdr:
            errs.append(f"missing required key for a proven warrant: {key}")
    if errs:
        return errs

    # r2 — the graph must actually pay.
    if int(gdr["cost_graph_tokens"]) >= int(gdr["cost_incumbent_tokens"]):
        errs.append(
            f"cost_graph_tokens ({gdr['cost_graph_tokens']}) >= cost_incumbent_tokens "
            f"({gdr['cost_incumbent_tokens']}): graph does not pay (r2-cheapest-structure-first)"
        )

    # r4 — closed, typed edge vocabulary; exactly one construction source each.
    edges = gdr["edge_types"]
    if not isinstance(edges, list) or not edges:
        errs.append("edge_types must be a non-empty list (r4-closed-edge-vocabulary)")
        edges = []
    banned = {"related_to", "see_also", "associated_with", "relates_to"}
    temporal_edges = False
    for i, e in enumerate(edges):
        if not isinstance(e, dict) or "name" not in e:
            errs.append(f"edge_types[{i}] must be a mapping with a name")
            continue
        name = str(e["name"])
        if name.lower() in banned:
            errs.append(f"edge type {name!r} is a catch-all; use a typed edge (r4-closed-edge-vocabulary)")
        has_derived = bool(e.get("derived_from"))
        has_extracted = bool(e.get("extracted_by"))
        if has_derived == has_extracted:
            errs.append(
                f"edge type {name!r} must declare exactly one of derived_from / extracted_by "
                "(r3-derived-edges-first)"
            )
        if e.get("temporal") is True:
            temporal_edges = True

    # r6 — temporal edges require the temporal warrant.
    if temporal_edges and gdr["warrant"] != "temporal":
        errs.append(
            "an edge type sets temporal: true but warrant is not 'temporal'; "
            "bitemporal edges need the temporal warrant or an explicit justification (r6-no-hard-delete)"
        )

    # r5 — traversal budget must be declared, arithmetically correct, and fit.
    hops, fanout = int(gdr["max_hops"]), int(gdr["max_fanout"])
    if hops > 5:
        errs.append(f"max_hops {hops} exceeds 5 (r5-declared-traversal-budget)")
    if fanout < 1:
        errs.append("max_fanout must be >= 1")
    else:
        expected = worst_case(fanout, hops)
        if int(gdr["worst_case_nodes"]) != expected:
            errs.append(
                f"worst_case_nodes is {gdr['worst_case_nodes']} but sum(k^i, i=0..h) is {expected} "
                "(r5-declared-traversal-budget)"
            )
        cost = expected * ASSUMED_TOKENS_PER_NODE
        if cost > int(gdr["context_budget_tokens"]):
            errs.append(
                f"worst-case traversal is ~{cost} tokens ({expected} nodes x {ASSUMED_TOKENS_PER_NODE}) "
                f"but context_budget_tokens is {gdr['context_budget_tokens']}: lower h or k "
                "(r5-declared-traversal-budget)"
            )
    if len(str(gdr["ranking_function"]).strip()) < 12:
        errs.append("ranking_function must name a deterministic score (r5-declared-traversal-budget)")

    # r7 — all three integrity checks wired to CI.
    checks = gdr["integrity_checks"]
    if not isinstance(checks, list):
        errs.append("integrity_checks must be a list (r7-integrity-gate-in-ci)")
    else:
        present = {str(c.get("check")) for c in checks if isinstance(c, dict)}
        for missing in sorted(REQUIRED_CHECKS - present):
            errs.append(f"integrity_checks missing {missing!r} (r7-integrity-gate-in-ci)")
        for c in checks:
            if isinstance(c, dict) and not c.get("ci_job"):
                errs.append(f"integrity check {c.get('check')!r} has no ci_job (r7-integrity-gate-in-ci)")

    if int(gdr["supernode_cap"]) < 1:
        errs.append("supernode_cap must be >= 1 (r4-closed-edge-vocabulary)")

    return errs


def load(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            print("PyYAML required for YAML records; install pyyaml or pass JSON", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(raw)
    return json.loads(raw)


def self_test() -> int:
    ok_gate = {
        "system": "methodology retrieval over a 2600-doc corpus",
        "warrant": "none",
        "warrant_evidence": "Every lookup resolves to a single domain then one slug; no doc has two parents.",
        "rejected_alternative": "tree",
    }
    bad_gate_leak = dict(ok_gate, max_hops=3)
    ok_full = {
        "system": "code navigation over a Go monorepo",
        "warrant": "cross_links",
        "warrant_evidence": "Call sites cross package boundaries; 40% of references leave their subtree.",
        "rejected_alternative": "tree",
        "cost_incumbent_tokens": 30000,
        "cost_graph_tokens": 4000,
        "edge_types": [
            {"name": "CALLS", "direction": "outbound", "meaning": "a calls b", "derived_from": "ast", "temporal": False}
        ],
        "supernode_cap": 5000,
        "max_hops": 2,
        "max_fanout": 8,
        "worst_case_nodes": 73,
        "context_budget_tokens": 20000,
        "ranking_function": "personalized pagerank seeded on anchors",
        "integrity_checks": [
            {"check": "referential", "ci_job": "graph-ci"},
            {"check": "orphans", "ci_job": "graph-ci"},
            {"check": "acyclicity", "ci_job": "graph-ci"},
        ],
        "rebuild_trigger": "any merge to main; incremental per changed package",
    }
    bad_math = dict(ok_full, worst_case_nodes=9)
    bad_pay = dict(ok_full, cost_graph_tokens=40000)
    bad_edge = dict(ok_full, edge_types=[{"name": "RELATED_TO", "derived_from": "x"}])

    cases = [
        ("gate stop, warrant none", ok_gate, 0),
        ("gate none but graph keys leaked", bad_gate_leak, 1),
        ("full valid record", ok_full, 0),
        ("worst_case_nodes arithmetic wrong", bad_math, 1),
        ("graph costs more than incumbent", bad_pay, 1),
        ("catch-all edge type", bad_edge, 1),
    ]
    failed = 0
    for name, doc, expect_errs in cases:
        errs = violations(doc)
        got = 1 if errs else 0
        status = "ok " if got == expect_errs else "FAIL"
        if got != expect_errs:
            failed += 1
        print(f"[{status}] {name}" + (f" -> {errs[0]}" if errs else ""))
    print(f"\n{len(cases) - failed}/{len(cases)} self-tests passed")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[1] == "--self-test":
        return self_test()
    path = Path(argv[1])
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    errs = violations(load(path))
    if not errs:
        print(f"OK  {path}")
        return 0
    print(f"FAIL  {path}", file=sys.stderr)
    for e in errs:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
