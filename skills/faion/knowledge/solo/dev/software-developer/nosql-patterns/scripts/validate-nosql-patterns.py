#!/usr/bin/env python3
"""validate-nosql-patterns.py

Validate an artefact produced by the nosql-patterns methodology against the JSON
Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://faion.net/schemas/nosql-patterns.json",
    "type": "object",
    "required": ["store_class", "access_patterns", "model", "ttl_policy", "indexes"],
    "properties": {
        "store_class": {"type": "string", "enum": ["document", "key_value", "wide_column", "graph"]},
        "access_patterns": {"type": "array", "minItems": 1},
        "model": {"type": "object", "required": ["entities", "embed_or_reference"]},
        "ttl_policy": {"type": "array"},
        "indexes": {"type": "array"},
        "partition_key": {"type": "object"},
    },
}
REQUIRED = SCHEMA["required"]


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "store_class" in obj and obj["store_class"] not in SCHEMA["properties"]["store_class"]["enum"]:
        errs.append(f"store_class must be one of {SCHEMA['properties']['store_class']['enum']}")
    if "access_patterns" in obj:
        if not isinstance(obj["access_patterns"], list):
            errs.append("access_patterns must be array")
        elif len(obj["access_patterns"]) < 1:
            errs.append("access_patterns must have minItems=1")
        else:
            for i, ap in enumerate(obj["access_patterns"]):
                if not isinstance(ap, dict):
                    errs.append(f"access_patterns[{i}] must be object"); continue
                for k in ("name", "qps", "latency_ms_p95"):
                    if k not in ap:
                        errs.append(f"access_patterns[{i}] missing {k}")
    if "model" in obj and isinstance(obj["model"], dict):
        for k in ("entities", "embed_or_reference"):
            if k not in obj["model"]:
                errs.append(f"model missing {k}")
    if "ttl_policy" in obj and isinstance(obj["ttl_policy"], list):
        import re
        rx = re.compile(r"^[a-z][a-z0-9_-]*:[a-z0-9_-]+(:[a-z0-9_-]+)?$")
        for i, p in enumerate(obj["ttl_policy"]):
            if not isinstance(p, dict):
                errs.append(f"ttl_policy[{i}] must be object"); continue
            if "prefix" not in p or not rx.match(str(p.get("prefix", ""))):
                errs.append(f"ttl_policy[{i}] prefix violates namespace pattern")
            if not isinstance(p.get("ttl_seconds"), int) or p.get("ttl_seconds", 0) < 1:
                errs.append(f"ttl_policy[{i}] ttl_seconds must be integer >=1")
    if "indexes" in obj and isinstance(obj["indexes"], list):
        for i, idx in enumerate(obj["indexes"]):
            if not isinstance(idx, dict):
                errs.append(f"indexes[{i}] must be object"); continue
            for k in ("collection_or_label", "fields"):
                if k not in idx:
                    errs.append(f"indexes[{i}] missing {k}")
    return errs


def self_test() -> int:
    good = {
        "store_class": "document",
        "access_patterns": [{"name": "q1", "qps": 100, "latency_ms_p95": 20}],
        "model": {"entities": ["x"], "embed_or_reference": {"y": "embed"}},
        "ttl_policy": [{"prefix": "svc:entity", "ttl_seconds": 60}],
        "indexes": [{"collection_or_label": "x", "fields": ["id"]}],
        "partition_key": {"key": "id", "primary_query": "get x by id"},
    }
    if validate(good):
        sys.stderr.write("self-test: good fixture rejected\n"); return 1
    if not validate({}):
        sys.stderr.write("self-test: empty fixture accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
