#!/usr/bin/env python3
"""Validate an Index Budget Record against the hierarchical-index-compression contract.

The checks are arithmetic: does the fan-out reach the corpus, does every level fit
the ceiling, and does the cold walk cost less than the body it delivers.

Usage:
  validate-hierarchical-index-compression.py <record.yaml|record.json>
  validate-hierarchical-index-compression.py --self-test
  validate-hierarchical-index-compression.py --help

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

BUILD_PATTERNS = {"shard", "recursive_summary", "hybrid"}
MAX_DEPTH = 3
MAX_DISCRIMINATOR_CHARS = 120

REQUIRED_KEYS = (
    "system",
    "corpus_size",
    "median_body_tokens",
    "index_read_ceiling_tokens",
    "levels",
    "max_depth",
    "fanout",
    "discriminator_max_chars",
    "entry_fields",
    "leaf_owns",
    "shard_trigger_tokens",
    "shard_stub",
    "corpus_nests_naturally",
    "build_pattern",
    "build_tokens",
    "rebuild_trigger",
    "skip_walk_when_known",
)


def violations(rec: dict) -> list[str]:
    errs: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in rec:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    if len(str(rec["system"]).strip()) < 12:
        errs.append("system must say what the hierarchy indexes (>=12 chars)")

    for key in ("corpus_size", "median_body_tokens", "index_read_ceiling_tokens",
                "max_depth", "fanout", "discriminator_max_chars",
                "shard_trigger_tokens", "build_tokens"):
        v = rec[key]
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            errs.append(f"{key} must be a non-negative integer")
    if errs:
        return errs

    depth = rec["max_depth"]
    levels = rec["levels"]
    if not isinstance(levels, list) or not levels:
        errs.append("levels must be a non-empty list, root first")
        return errs
    if depth > MAX_DEPTH:
        errs.append(
            f"max_depth {depth} exceeds {MAX_DEPTH}: each level is a full index read paid on "
            "every lookup — widen fan-out instead (r3-fanout-and-depth-reach-the-corpus)"
        )
    if len(levels) != depth:
        errs.append(
            f"levels lists {len(levels)} tiers but max_depth is {depth} "
            "(r3-fanout-and-depth-reach-the-corpus)"
        )

    ceiling = rec["index_read_ceiling_tokens"]
    if ceiling < 1:
        errs.append("index_read_ceiling_tokens must be >= 1 (r1-declared-index-read-ceiling)")
    walk = 0
    for i, lv in enumerate(levels):
        if not isinstance(lv, dict) or "name" not in lv:
            errs.append(f"levels[{i}] must be a mapping with a name")
            continue
        rt = lv.get("read_tokens")
        if not isinstance(rt, int) or isinstance(rt, bool) or rt < 1:
            errs.append(f"levels[{i}].read_tokens must be a measured positive integer")
            continue
        walk += rt
        if rt > ceiling:
            errs.append(
                f"level {lv['name']!r} reads {rt} tokens, above the ceiling {ceiling}: shard it on "
                f"{lv.get('partition_key') or 'a declared partition key'} "
                "(r1-declared-index-read-ceiling)"
            )
        ec = lv.get("entry_count")
        if not isinstance(ec, int) or isinstance(ec, bool) or ec < 1:
            errs.append(f"levels[{i}].entry_count must be a positive integer")
        if i < len(levels) - 1 and not lv.get("partition_key"):
            errs.append(
                f"level {lv['name']!r} is not the leaf-most index and must declare a partition_key "
                "(r4-shard-trigger-is-a-number)"
            )

    # r3 — the hierarchy must be able to reach every leaf.
    if rec["fanout"] < 1:
        errs.append("fanout must be >= 1")
    elif rec["fanout"] ** depth < rec["corpus_size"]:
        errs.append(
            f"fanout^max_depth = {rec['fanout'] ** depth} does not reach corpus_size "
            f"{rec['corpus_size']}: some leaves are unreachable "
            "(r3-fanout-and-depth-reach-the-corpus)"
        )

    # r1 — the map must cost less than the destination.
    if walk and walk > rec["median_body_tokens"]:
        errs.append(
            f"cold walk costs {walk} tokens against a median body of {rec['median_body_tokens']}: "
            "the map costs more than the destination (r1-declared-index-read-ceiling)"
        )

    # r2 — entries discriminate; the leaf keeps its own summary.
    if rec["discriminator_max_chars"] > MAX_DISCRIMINATOR_CHARS:
        errs.append(
            f"discriminator_max_chars {rec['discriminator_max_chars']} exceeds "
            f"{MAX_DISCRIMINATOR_CHARS}: above this an entry is a description, not a discriminator "
            "(r2-entries-discriminate-not-describe)"
        )
    ef, lo = rec["entry_fields"], rec["leaf_owns"]
    if not isinstance(ef, list) or not ef:
        errs.append("entry_fields must be a non-empty closed list (r2-entries-discriminate-not-describe)")
        ef = []
    if not isinstance(lo, list) or not lo:
        errs.append("leaf_owns must list at least the leaf's full summary field (r2-entries-discriminate-not-describe)")
        lo = []
    overlap = sorted(set(ef) & set(lo))
    if overlap:
        errs.append(
            f"fields {overlap} appear in both entry_fields and leaf_owns: they would be paid twice "
            "(r2-entries-discriminate-not-describe)"
        )
    if lo and not any("summary" in str(f) or "description" in str(f) or "abstract" in str(f) for f in lo):
        errs.append(
            "leaf_owns must name the leaf's full summary/description/abstract field — that is the "
            "text an index must not restate (r2-entries-discriminate-not-describe)"
        )

    # r4 — the trigger must actually prevent a breach, and must not change routing.
    if rec["shard_trigger_tokens"] > ceiling:
        errs.append(
            f"shard_trigger_tokens {rec['shard_trigger_tokens']} is above the ceiling {ceiling}: "
            "the split would fire only after the ceiling is already breached "
            "(r4-shard-trigger-is-a-number)"
        )
    if rec["shard_stub"] is not True:
        errs.append(
            "shard_stub must be true: a split that changes caller routing is a migration, and "
            "migrations get deferred (r4-shard-trigger-is-a-number)"
        )

    # r5 — free structure is excluded before any paid build.
    bp = rec["build_pattern"]
    if bp not in BUILD_PATTERNS:
        errs.append(f"build_pattern must be one of {sorted(BUILD_PATTERNS)}")
    else:
        if bp == "shard" and rec["build_tokens"] != 0:
            errs.append("build_pattern 'shard' must have build_tokens 0 — sharding invokes no model (r5-shard-before-you-summarise)")
        if bp != "shard":
            if rec["corpus_nests_naturally"]:
                errs.append(
                    f"build_pattern {bp!r} but corpus_nests_naturally is true: shard the existing "
                    "nesting for zero tokens before summarising anything (r5-shard-before-you-summarise)"
                )
            if rec["build_tokens"] <= 0:
                errs.append(f"build_pattern {bp!r} must record a positive build_tokens (r5-shard-before-you-summarise)")
            if not str(rec["rebuild_trigger"]).strip():
                errs.append(f"build_pattern {bp!r} must declare a rebuild_trigger (r5-shard-before-you-summarise)")

    if rec["skip_walk_when_known"] is not True:
        errs.append(
            "skip_walk_when_known must be true: re-walking to a known leaf pays the whole index "
            "tier for information already held (r6-known-leaf-skips-the-walk)"
        )

    return errs


def load(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            print("PyYAML required for YAML records; install pyyaml or pass JSON", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(raw)
    return json.loads(raw)


def _record(**over: object) -> dict:
    base = {
        "system": "methodology retrieval over a 2600-document corpus",
        "corpus_size": 2600,
        "median_body_tokens": 3300,
        "index_read_ceiling_tokens": 4000,
        "levels": [
            {"name": "domains", "entry_count": 20, "read_tokens": 1800, "partition_key": "domain"},
            {"name": "domain-index", "entry_count": 160, "read_tokens": 1200, "partition_key": None},
        ],
        "max_depth": 2,
        "fanout": 160,
        "discriminator_max_chars": 90,
        "entry_fields": ["id", "tier", "produces", "discriminator"],
        "leaf_owns": ["summary", "body", "rationale"],
        "shard_trigger_tokens": 4000,
        "shard_stub": True,
        "corpus_nests_naturally": True,
        "build_pattern": "shard",
        "build_tokens": 0,
        "rebuild_trigger": "any leaf added, removed or retiered; stub regenerated in the same job",
        "skip_walk_when_known": True,
    }
    base.update(over)
    return base


def self_test() -> int:
    over_ceiling = _record(levels=[
        {"name": "domains", "entry_count": 20, "read_tokens": 1800, "partition_key": "domain"},
        {"name": "domain-index", "entry_count": 160, "read_tokens": 30000, "partition_key": None},
    ])
    unreachable = _record(fanout=8)
    walk_too_dear = _record(median_body_tokens=1000)
    paid_twice = _record(entry_fields=["id", "summary", "discriminator"])
    summary_over_nesting = _record(build_pattern="recursive_summary", build_tokens=115541)
    shard_costs_tokens = _record(build_tokens=115541)
    trigger_above_ceiling = _record(shard_trigger_tokens=9000)
    deep = _record(max_depth=4, levels=_record()["levels"] + [
        {"name": "group", "entry_count": 12, "read_tokens": 300, "partition_key": "group"},
        {"name": "sub", "entry_count": 12, "read_tokens": 300, "partition_key": None},
    ])
    fat_entry = _record(discriminator_max_chars=400)
    no_stub = _record(shard_stub=False)

    cases = [
        ("valid record, sharded two-level tree", _record(), 0),
        ("a level exceeds the read ceiling", over_ceiling, 1),
        ("fan-out cannot reach the corpus", unreachable, 1),
        ("cold walk costs more than the body", walk_too_dear, 1),
        ("summary in both index and leaf", paid_twice, 1),
        ("summary tree over a corpus that nests", summary_over_nesting, 1),
        ("sharding claims a build cost", shard_costs_tokens, 1),
        ("shard trigger above the ceiling", trigger_above_ceiling, 1),
        ("depth 4", deep, 1),
        ("entry cap is description-sized", fat_entry, 1),
        ("shard without a routing stub", no_stub, 1),
    ]
    failed = 0
    for name, doc, expect in cases:
        errs = violations(doc)
        got = 1 if errs else 0
        if got != expect:
            failed += 1
        status = "ok " if got == expect else "FAIL"
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
