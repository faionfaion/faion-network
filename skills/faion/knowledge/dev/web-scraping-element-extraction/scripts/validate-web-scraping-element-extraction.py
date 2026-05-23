#!/usr/bin/env python3
"""validate-web-scraping-element-extraction.py

Validate a per-row extraction artefact JSON against the schema + normalizer rule.

Inputs:
    --file PATH      path to row JSON
    --self-test      run built-in valid + invalid fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^wsx-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NORMALIZERS = {"text-trim", "text-collapse-ws", "text-strip-nonprintable", "price-to-float", "date-to-iso", "table-shape-check"}
VERDICTS = {"approve", "block-no-normalizer", "block-wrong-api"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "source", "row_index", "fields", "normalizers_applied", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^wsx-[a-z0-9-]{6,}$")
    if "row_index" in obj:
        if not isinstance(obj["row_index"], int) or obj["row_index"] < 0:
            errs.append("row_index must be non-negative integer")

    fields = obj.get("fields") or {}
    if not isinstance(fields, dict):
        errs.append("fields must be an object")
    else:
        for k, v in fields.items():
            if isinstance(v, str):
                if v != v.strip() or "  " in v or any(c in v for c in "\n\t\r"):
                    errs.append(f"fields.{k} contains un-normalized whitespace; apply text-trim/collapse")
                if re.search(r"^[\s$€£¥₴]*[\d.,]+\s*[$€£¥₴]?\s*$", v) and "." in v + ",":
                    # looks like a price stored as string
                    if not any(pf.get("field") == k for pf in obj.get("parse_failures", [])):
                        errs.append(f"fields.{k} looks like a raw price string; apply price-to-float or record parse_failure")

    na = obj.get("normalizers_applied") or []
    if not isinstance(na, list) or len(na) < 1:
        errs.append("normalizers_applied must be a non-empty list")
    else:
        for n in na:
            if n not in NORMALIZERS:
                errs.append(f"unknown normalizer: {n}")

    pf = obj.get("parse_failures") or []
    if pf:
        if not isinstance(pf, list):
            errs.append("parse_failures must be a list")
        else:
            for i, item in enumerate(pf):
                for sub in ("field", "reason"):
                    if sub not in item:
                        errs.append(f"parse_failures[{i}] missing {sub}")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    if verdict == "approve" and not na:
        errs.append("verdict=approve requires normalizers_applied to be non-empty")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "wsx-news-row-0042",
    "source": "example.com/news",
    "row_index": 42,
    "fields": {"title": "Migration to Go shadow router", "price": None, "published_at": "2026-05-20"},
    "normalizers_applied": ["text-trim", "text-collapse-ws", "date-to-iso"],
    "parse_failures": [],
    "verdict": "approve",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "row0042",
    "source": "example.com/news",
    "row_index": 42,
    "fields": {"title": "  Migration to Go shadow router\n\n ", "price": "$1,234.56"},
    "normalizers_applied": [],
    "verdict": "approve",
    "version": "1.0",
    "last_reviewed": "today",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to row JSON")
    ap.add_argument("--self-test", action="store_true")
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
