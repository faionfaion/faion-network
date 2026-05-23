#!/usr/bin/env python3
"""Validate rag-bench-spec artefact.

USAGE:
    validate-rag-bench-harness-template.py <input.json>
    validate-rag-bench-harness-template.py --self-test
    validate-rag-bench-harness-template.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "corpus", "query_set", "runners", "metrics", "leaderboard_path", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r}")
    c = s.get("corpus") or {}
    if len((c.get("sha") or "")) < 7:
        v.append("corpus.sha must be ≥7 chars (rule r1)")
    if not isinstance(c.get("doc_count"), int) or c.get("doc_count", 0) < 1:
        v.append("corpus.doc_count must be ≥1")
    qs = s.get("query_set") or {}
    if qs.get("gold_labels") is not True:
        v.append("query_set.gold_labels must be true (rule r2)")
    if not isinstance(qs.get("size"), int) or qs.get("size", 0) < 10:
        v.append("query_set.size must be ≥10")
    runners = s.get("runners")
    if not isinstance(runners, list) or len(runners) < 1:
        v.append("runners must be non-empty list")
    if isinstance(runners, list):
        for i, r in enumerate(runners):
            if not isinstance(r, dict):
                v.append(f"runners[{i}] must be object")
                continue
            for k in ("name", "version", "config_hash"):
                if not (r.get(k) or "").strip():
                    v.append(f"runners[{i}].{k} required (rule r3)")
            if len((r.get("config_hash") or "")) < 7:
                v.append(f"runners[{i}].config_hash must be ≥7 chars (rule r3)")
    if not isinstance(s.get("metrics"), list) or len(s.get("metrics") or []) < 1:
        v.append("metrics must be non-empty (rule r4)")
    if not (s.get("leaderboard_path") or "").strip():
        v.append("leaderboard_path required")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO YYYY-MM-DD")
    return v


GOOD = {
    "artefact_id": "rag-bench-chunking-2026q2",
    "owner": "ruslan@faion.net",
    "corpus": {"path": "warehouse://kb", "sha": "a1b2c3d4e5f", "doc_count": 50000},
    "query_set": {"path": "git://faion/eval/q.jsonl", "gold_labels": True, "size": 800},
    "runners": [
        {"name": "bm25", "version": "0.2.2", "config_hash": "9f8e7d6"},
        {"name": "dense", "version": "bge-large", "config_hash": "1a2b3c4"},
    ],
    "metrics": ["Recall@10", "MRR"],
    "leaderboard_path": "git://faion/leaderboards/rag.json",
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "corpus": {"path": "live", "sha": "", "doc_count": 0},
    "query_set": {"path": "x", "gold_labels": False, "size": 3},
    "runners": [{"name": "bm25"}],
    "metrics": [],
    "leaderboard_path": "",
    "version": "v1",
    "last_reviewed": "yesterday",
}


def _self_test() -> int:
    errs = validate(GOOD)
    assert errs == [], f"happy failed: {errs}"
    bad = validate(BAD)
    assert any("corpus.sha" in x for x in bad)
    assert any("gold_labels" in x for x in bad)
    assert any("config_hash" in x for x in bad)
    assert any("metrics" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-rag-bench-harness-template.py")
    p.add_argument("path", nargs="?")
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
