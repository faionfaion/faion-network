#!/usr/bin/env python3
"""Validate a langchain-memory decision-record against the embedded JSON schema.

Usage:
    validate-langchain-memory.py <path-to-decision-record.json>
    validate-langchain-memory.py --self-test
    validate-langchain-memory.py --help

Inputs:
    Path to a JSON file produced by the langchain-memory methodology.

Outputs:
    Writes violation list to stderr. JSON summary to stdout on --json.

Exit codes:
    0 = valid
    1 = invalid (one or more violations)
    2 = bad invocation (file missing, malformed JSON, etc.)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_MEMORY = {"buffer", "summary", "vector", "entity"}
ALLOWED_BACKEND = {"in-memory", "redis", "postgres", "chroma", "pinecone"}
ALLOWED_SESSION = {"uuid", "hashed-user-id", "thread-id"}
ALLOWED_RECALL = {"recency", "semantic", "mixed"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE_REF = re.compile(r"^r\d+$")


def _violations(rec: dict) -> list[str]:
    v: list[str] = []
    if rec.get("slug") != "langchain-memory":
        v.append("slug must equal 'langchain-memory'")
    if not SEMVER.match(rec.get("version", "")):
        v.append("version must be semver")
    d = rec.get("decision") or {}
    if d.get("memory_type") not in ALLOWED_MEMORY:
        v.append(f"decision.memory_type must be one of {sorted(ALLOWED_MEMORY)}")
    if d.get("store_backend") not in ALLOWED_BACKEND:
        v.append(f"decision.store_backend must be one of {sorted(ALLOWED_BACKEND)}")
    if d.get("session_id_strategy") not in ALLOWED_SESSION:
        v.append(f"decision.session_id_strategy must be one of {sorted(ALLOWED_SESSION)}")
    ttl = d.get("ttl_seconds")
    if not isinstance(ttl, int) or ttl < 60:
        v.append("decision.ttl_seconds must be int >=60")
    dr = rec.get("drivers") or {}
    if not isinstance(dr.get("expected_turns"), int) or dr.get("expected_turns", 0) < 1:
        v.append("drivers.expected_turns must be int >=1")
    if dr.get("recall_pattern") not in ALLOWED_RECALL:
        v.append(f"drivers.recall_pattern must be one of {sorted(ALLOWED_RECALL)}")
    if not isinstance(dr.get("entity_focus"), bool):
        v.append("drivers.entity_focus must be bool")
    rej = rec.get("rejected") or []
    if not isinstance(rej, list) or len(rej) < 1:
        v.append("rejected must have >=1 entry")
    else:
        for i, r in enumerate(rej):
            if r.get("memory_type") not in ALLOWED_MEMORY:
                v.append(f"rejected[{i}].memory_type invalid")
            if not isinstance(r.get("reason"), str) or len(r.get("reason", "")) < 10:
                v.append(f"rejected[{i}].reason must be string of length >=10")
    w = rec.get("wiring") or {}
    if not isinstance(w.get("snippet"), str) or len(w.get("snippet", "")) < 40:
        v.append("wiring.snippet must be string of length >=40")
    if not w.get("history_messages_key"):
        v.append("wiring.history_messages_key required")
    if not w.get("input_messages_key"):
        v.append("wiring.input_messages_key required")
    audit = rec.get("audit") or {}
    refs = audit.get("rule_refs") or []
    if not refs:
        v.append("audit.rule_refs must contain >=1 rule id")
    for r in refs:
        if not RULE_REF.match(str(r)):
            v.append(f"audit.rule_refs entry '{r}' must match ^r\\d+$")
    return v


def _self_test() -> int:
    good = {
        "slug": "langchain-memory",
        "version": "2.0.0",
        "decision": {
            "memory_type": "buffer",
            "store_backend": "redis",
            "session_id_strategy": "uuid",
            "ttl_seconds": 3600,
        },
        "drivers": {"expected_turns": 6, "recall_pattern": "recency", "entity_focus": False},
        "rejected": [{"memory_type": "summary", "reason": "under-10-turns no need"}],
        "wiring": {
            "snippet": "RunnableWithMessageHistory(chain, get_session_history, input_messages_key='input', history_messages_key='history')",
            "history_messages_key": "history",
            "input_messages_key": "input",
        },
        "audit": {"rule_refs": ["r1", "r13"]},
    }
    if _violations(good):
        return 1
    bad = dict(good)
    bad["decision"] = {**good["decision"], "ttl_seconds": 0}
    if not _violations(bad):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) < 2:
        sys.stderr.write("usage: validate-langchain-memory.py <file.json>\n")
        return 2
    p = Path(argv[1])
    if not p.exists():
        sys.stderr.write(f"missing: {p}\n")
        return 2
    try:
        rec = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"bad json: {e}\n")
        return 2
    vs = _violations(rec)
    if vs:
        for x in vs:
            sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
