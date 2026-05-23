#!/usr/bin/env python3
"""validate-code-coverage.py

Validate a coverage-gate config JSON OR an uncovered-lines extract JSON against
the schemas in 02-output-contract.xml.

Inputs:
    --file PATH       path to JSON to validate
    --kind {gate,extract}  which schema to apply (default: auto-detect)
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
import re
import sys
from pathlib import Path

ALLOWED_STACKS = {"python", "js", "ts", "go", "rust", "mixed"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_gate(obj: dict) -> list[str]:
    errs: list[str] = []
    required = ["stack", "global_threshold", "diff_threshold", "per_dir", "exclude", "version", "last_reviewed"]
    for k in required:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "stack" in obj and obj["stack"] not in ALLOWED_STACKS:
        errs.append(f"stack must be in {sorted(ALLOWED_STACKS)}")
    if obj.get("branch_coverage") is not True:
        errs.append("branch_coverage must be true")
    for k in ("global_threshold", "diff_threshold"):
        v = obj.get(k)
        if isinstance(v, int) and not (70 <= v <= 95):
            errs.append(f"{k} must be int in [70,95]")
    per_dir = obj.get("per_dir") or {}
    if not isinstance(per_dir, dict):
        errs.append("per_dir must be object")
    else:
        for d, t in per_dir.items():
            if not isinstance(t, int) or not (70 <= t <= 100):
                errs.append(f"per_dir.{d} must be int in [70,100]")
    if "exclude" in obj and not isinstance(obj["exclude"], list):
        errs.append("exclude must be list")
    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


def validate_extract(obj: dict) -> list[str]:
    errs: list[str] = []
    if "files" not in obj:
        errs.append("missing required field: files")
        return errs
    if not isinstance(obj["files"], list):
        errs.append("files must be list")
        return errs
    for i, f in enumerate(obj["files"]):
        if "path" not in f:
            errs.append(f"files[{i}] missing path")
        if "uncovered_lines" not in f:
            errs.append(f"files[{i}] missing uncovered_lines")
        elif not isinstance(f["uncovered_lines"], list):
            errs.append(f"files[{i}].uncovered_lines must be list")
        else:
            for j, ln in enumerate(f["uncovered_lines"]):
                if not isinstance(ln, int) or ln < 1:
                    errs.append(f"files[{i}].uncovered_lines[{j}] must be int >= 1")
    return errs


def auto_kind(obj: dict) -> str:
    return "extract" if "files" in obj and "stack" not in obj else "gate"


GATE_OK = {
    "stack": "python", "branch_coverage": True, "global_threshold": 80,
    "diff_threshold": 90, "per_dir": {"src/auth/": 95}, "exclude": ["src/migrations/*"],
    "version": "1.0.0", "last_reviewed": "2026-05-22",
}
GATE_BAD = {"stack": "python", "branch_coverage": False, "global_threshold": 60, "per_dir": {}}
EXTRACT_OK = {"files": [{"path": "src/a.py", "uncovered_lines": [4, 10]}]}
EXTRACT_BAD = {"files": [{"path": "x"}]}


def self_test() -> int:
    if validate_gate(GATE_OK):
        sys.stderr.write("gate-ok rejected\n"); return 1
    if not validate_gate(GATE_BAD):
        sys.stderr.write("gate-bad accepted\n"); return 1
    if validate_extract(EXTRACT_OK):
        sys.stderr.write("extract-ok rejected\n"); return 1
    if not validate_extract(EXTRACT_BAD):
        sys.stderr.write("extract-bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--kind", choices=["gate", "extract"], default=None)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    kind = args.kind or auto_kind(obj)
    errs = validate_gate(obj) if kind == "gate" else validate_extract(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
