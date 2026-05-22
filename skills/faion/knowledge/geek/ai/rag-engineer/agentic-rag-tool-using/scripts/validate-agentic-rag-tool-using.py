#!/usr/bin/env python3
"""validate-agentic-rag-tool-using — verify ToolUsingRAG output JSON.

Inputs:
  argv[1]  path to JSON output file
Flags:
  --help        print this help and exit 0
  --self-test   run built-in fixture, exit 0 on pass / 1 on fail
Exit codes:
  0  output passes the schema + cap + allow-list invariants
  1  one or more violations (printed to stderr)
  2  CLI usage error

Deps: stdlib only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_TOOLS = {"vector_search", "keyword_search", "sql_query", "web_search", "generate_answer"}


def validate(obj: dict) -> list[str]:
    errors: list[str] = []
    for key in ("answer", "trace", "calls_used", "max_calls", "synthesis_model", "routing_model"):
        if key not in obj:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors
    if not isinstance(obj["answer"], str) or len(obj["answer"]) < 1:
        errors.append("answer must be non-empty string")
    if not isinstance(obj["trace"], list) or len(obj["trace"]) < 1:
        errors.append("trace must be a non-empty list")
    for i, entry in enumerate(obj.get("trace", [])):
        for key in ("iteration", "tool", "query", "result_summary", "latency_ms"):
            if key not in entry:
                errors.append(f"trace[{i}] missing {key}")
        if entry.get("tool") not in ALLOWED_TOOLS:
            errors.append(f"trace[{i}] tool {entry.get('tool')!r} not in allowed set")
        if isinstance(entry.get("result_summary"), str) and len(entry["result_summary"]) > 200:
            errors.append(f"trace[{i}] result_summary > 200 chars")
    if obj.get("calls_used", 0) > obj.get("max_calls", 0):
        errors.append("calls_used exceeds max_calls")
    if obj.get("web_search_allowlist_violations"):
        errors.append(f"web_search allow-list violations: {obj['web_search_allowlist_violations']}")
    return errors


def _self_test() -> int:
    good = {
        "answer": "ok",
        "trace": [{"iteration": 1, "tool": "vector_search", "query": "q", "result_summary": "s", "latency_ms": 1}],
        "calls_used": 1, "max_calls": 3,
        "synthesis_model": "sonnet", "routing_model": "haiku",
        "web_search_allowlist_violations": [],
    }
    bad = {**good, "calls_used": 9}
    if validate(good):
        return 1
    if not validate(bad):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-agentic-rag-tool-using.py <output.json>\n")
        return 2
    path = Path(argv[1])
    obj = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(obj)
    if errors:
        for e in errors:
            sys.stderr.write(f"ERROR: {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
