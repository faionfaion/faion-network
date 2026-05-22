#!/usr/bin/env python3
"""validate-pnpm-package-management.py — verify packageManager pin, lockfile, no shamefully-hoist.

Usage:
    validate-pnpm-package-management.py --root /path/to/repo
    validate-pnpm-package-management.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PNPM_RE = re.compile(r"^pnpm@\d+\.\d+\.\d+")


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            v.append({"rule": "schema", "message": "invalid package.json"})
            data = {}
        pm = data.get("packageManager", "")
        if not PNPM_RE.match(pm):
            v.append({"rule": "rule:r1", "message": f"packageManager {pm!r} not pinned to pnpm@X.Y.Z"})
    else:
        v.append({"rule": "rule:r1", "message": "package.json not found"})
    if not (root / "pnpm-lock.yaml").exists():
        v.append({"rule": "rule:r5", "message": "pnpm-lock.yaml missing — must be committed"})
    npmrc = root / ".npmrc"
    if npmrc.exists():
        for idx, line in enumerate(npmrc.read_text(encoding="utf-8").splitlines(), 1):
            if "shamefully-hoist" in line and "true" in line:
                v.append({"rule": "rule:r2", "file": str(npmrc), "line": idx, "snippet": line.strip()})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "package.json").write_text(json.dumps({"packageManager": "pnpm@9.6.0"}), encoding="utf-8")
        (root / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n", encoding="utf-8")
        assert not scan(root)
        (root / ".npmrc").write_text("shamefully-hoist=true\n", encoding="utf-8")
        v = scan(root)
        assert any(x["rule"] == "rule:r2" for x in v), v
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
    v = scan(args.root)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
