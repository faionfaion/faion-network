#!/usr/bin/env python3
"""validate-db-comparison — verify decision.json.

Inputs: argv[1] = decision.json path.
Flags: --help, --self-test.
Exit: 0 pass, 1 fail, 2 cli misuse.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_DB = {"chroma", "qdrant", "weaviate", "pgvector", "pinecone", "milvus"}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def validate(d: dict) -> list[str]:
    errors: list[str] = []
    for key in ("decision_version", "decision_owner", "last_reviewed", "year_one_vectors", "chosen", "score_matrix", "fallbacks", "migration_plan"):
        if key not in d:
            errors.append(f"missing {key}")
    if "decision_version" in d and not SEMVER_RE.match(str(d["decision_version"])):
        errors.append("decision_version not semver")
    if d.get("chosen") not in ALLOWED_DB:
        errors.append("chosen not in allowed enum")
    if not d.get("fallbacks"):
        errors.append("fallbacks required (>=1)")
    for i, fb in enumerate(d.get("fallbacks", [])):
        if "db" not in fb or "trigger" not in fb:
            errors.append(f"fallback {i} missing db or trigger")
    if len(d.get("migration_plan", "")) < 20:
        errors.append("migration_plan < 20 chars")
    return errors


def _self_test() -> int:
    good = {"decision_version": "1.0.0", "decision_owner": "founder",
            "last_reviewed": "2026-05-22", "year_one_vectors": 100,
            "chosen": "qdrant", "score_matrix": {"qdrant": {}},
            "fallbacks": [{"db": "weaviate", "trigger": "growth"}],
            "migration_plan": "phase1 single-node; phase2 replica"}
    if validate(good):
        return 1
    if not validate({**good, "chosen": "best"}):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-db-comparison.py <decision.json>\n")
        return 2
    d = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errors = validate(d)
    if errors:
        for e in errors:
            sys.stderr.write(f"ERROR: {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
