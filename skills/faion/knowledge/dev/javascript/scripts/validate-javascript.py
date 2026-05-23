#!/usr/bin/env python3
"""validate-javascript.py — check tsconfig flags, no any in src/.

Usage:
    validate-javascript.py --root /path/to/repo
    validate-javascript.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ANY_DECL = re.compile(r":\s*any\b|<any>|as any\b")


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    tsc = root / "tsconfig.json"
    if tsc.exists():
        try:
            data = json.loads(tsc.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            v.append({"rule": "schema", "file": str(tsc), "message": "tsconfig.json not valid JSON"})
            data = {}
        opts = data.get("compilerOptions", {})
        for flag in ("strict", "noUncheckedIndexedAccess", "exactOptionalPropertyTypes"):
            if not opts.get(flag):
                v.append({"rule": "rule:r1", "file": str(tsc), "message": f"tsconfig: {flag} not enabled"})
    else:
        v.append({"rule": "rule:r1", "file": str(root), "message": "no tsconfig.json found"})
    src = root / "src"
    if src.is_dir():
        for f in src.rglob("*.ts"):
            if "/node_modules/" in str(f):
                continue
            for idx, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if ANY_DECL.search(line):
                    v.append({"rule": "rule:r1", "file": str(f), "line": idx, "snippet": line.strip()})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tsconfig.json").write_text(json.dumps({
            "compilerOptions": {"strict": True, "noUncheckedIndexedAccess": True, "exactOptionalPropertyTypes": True}
        }), encoding="utf-8")
        (root / "src").mkdir()
        (root / "src/x.ts").write_text("export const a: number = 1;\n", encoding="utf-8")
        assert not scan(root)
        (root / "src/bad.ts").write_text("export const b: any = 1;\n", encoding="utf-8")
        v = scan(root)
        assert any("rule:r1" in x["rule"] for x in v)
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
