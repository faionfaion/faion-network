#!/usr/bin/env python3
"""validate-ai-enhanced-design-systems.py

Validate an artefact for the ai-enhanced-design-systems methodology against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["ds_root", "token_map", "doc_generator", "token_scanner", "variant_generator", "human_review_required"]
PLACEHOLDERS = {"tbd", "todo", "fixme", "xxx", "fill_me"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    # placeholder string detection
    def walk(node, path: str):
        if isinstance(node, str):
            if node.strip().lower() in PLACEHOLDERS:
                errs.append(f"placeholder value at {path}: {node!r}")
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")
    walk(obj, "")
    return errs


OK = json.loads("{\"ds_root\": \"packages/ds\", \"token_map\": \"packages/ds/tokens.json\", \"doc_generator\": {\"source\": \"packages/ds/src\", \"story_root\": \"packages/ds/stories\", \"output\": \"packages/ds/docs\"}, \"token_scanner\": {\"block_on_violation\": true, \"scan_globs\": [\"apps/**/*.tsx\"]}, \"variant_generator\": {\"visreg_provider\": \"chromatic\", \"max_variants_per_component\": 24}, \"human_review_required\": true}")
BAD = json.loads("{\"ds_root\": \"packages/ds\", \"token_scanner\": {\"block_on_violation\": false}, \"human_review_required\": false}")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
