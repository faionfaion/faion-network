#!/usr/bin/env python3
"""validate-go-backend.py — verify a Go repo follows the cmd/ + internal/ layout invariants.

Usage:
    validate-go-backend.py --root /path/to/repo
    validate-go-backend.py --self-test

Inputs:
    --root PATH   repo root containing go.mod
Outputs: stdout JSON {ok, violations}
Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_INTERNAL = ["handler", "service", "repository", "model", "middleware", "config"]
FORBIDDEN = [
    (re.compile(r"c\.JSON\(\s*http\.Status[BNFC45]"), "rule:r8 c.JSON for error"),
    (re.compile(r"c\.JSON\(\s*4\d\d|c\.JSON\(\s*5\d\d"), "rule:r8 c.JSON for error"),
    (re.compile(r"\bBindJSON\("), "rule:r7 BindJSON instead of ShouldBindJSON"),
    (re.compile(r"go\s+func\s*\([^)]*\)\s*\{[^}]*\bc\."), "rule:r5 gin.Context in goroutine"),
]


def find_module_path(root: Path) -> str | None:
    gomod = root / "go.mod"
    if not gomod.exists():
        return None
    for line in gomod.read_text(encoding="utf-8").splitlines():
        if line.startswith("module "):
            return line.split(maxsplit=1)[1].strip()
    return None


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    module = find_module_path(root)
    if not module:
        v.append({"rule": "structure", "message": "go.mod missing or has no module line"})
        return v
    main_go = root / "cmd" / "api" / "main.go"
    if not main_go.exists():
        v.append({"rule": "rule:r1", "message": "missing cmd/api/main.go"})
    else:
        line_count = len(main_go.read_text(encoding="utf-8").splitlines())
        if line_count > 80:
            v.append({"rule": "rule:r4", "message": f"main.go has {line_count} lines (>80), should be thin"})
    internal = root / "internal"
    if not internal.is_dir():
        v.append({"rule": "rule:r1", "message": "missing internal/ directory"})
        return v
    present = [d.name for d in internal.iterdir() if d.is_dir()]
    missing = [d for d in REQUIRED_INTERNAL if d not in present]
    if len(missing) > 1:
        v.append({"rule": "rule:r1", "message": f"missing internal subdirs: {missing}"})
    interface_in_repo = False
    for f in (internal / "repository").rglob("*.go") if (internal / "repository").is_dir() else []:
        text = f.read_text(encoding="utf-8")
        if re.search(r"\btype\s+\w+\s+interface\s*\{", text):
            interface_in_repo = True
            v.append({"rule": "rule:r2", "file": str(f), "message": "interface declared in repository/ — should live in service/"})
    for f in root.rglob("*.go"):
        if "/vendor/" in str(f):
            continue
        text = f.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), 1):
            for pat, rule in FORBIDDEN:
                if pat.search(line):
                    v.append({"rule": rule, "file": str(f), "line": idx, "snippet": line.strip()})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "go.mod").write_text("module example.com/svc\n\ngo 1.21\n", encoding="utf-8")
        (root / "cmd/api").mkdir(parents=True)
        (root / "cmd/api/main.go").write_text("package main\nfunc main() {}\n", encoding="utf-8")
        for d in REQUIRED_INTERNAL:
            (root / "internal" / d).mkdir(parents=True)
        v = scan(root)
        assert not v, f"good case must pass: {v}"
        (root / "internal/repository/user.go").write_text(
            "package repository\ntype UserRepository interface { Get() string }\n", encoding="utf-8"
        )
        v = scan(root)
        assert any("rule:r2" in x["rule"] for x in v), f"should flag r2: {v}"
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.root:
        ap.error("--root required")
        return 2
    violations = scan(args.root)
    sys.stdout.write(json.dumps({"ok": not violations, "violations": violations}, indent=2) + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
