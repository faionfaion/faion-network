#!/usr/bin/env python3
"""validate-go-concurrency.py — grep concurrency antipatterns in Go source.

Usage:
    validate-go-concurrency.py --root /path/to/repo
    validate-go-concurrency.py --self-test

Inputs:
    --root PATH    Go module root
Outputs: stdout JSON {ok, violations}
Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# (regex, rule, description)
CHECKS = [
    (re.compile(r"^\s*go\s+func\s*\(\s*\)\s*\{"), "rule:r2", "bare go func() — no ctx, may leak"),
    (re.compile(r"go\s+func[^)]*\{\s*$"), "rule:r2", "goroutine without explicit exit comment"),
]
WG_ADD_BODY = re.compile(r"go\s+func[^}]*\bwg\.Add\(", re.DOTALL)


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    for f in root.rglob("*.go"):
        if "/vendor/" in str(f) or f.name.endswith("_test.go") is False and "_test_" in f.name:
            pass
        text = f.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), 1):
            for pat, rule, desc in CHECKS:
                if pat.search(line):
                    look = "\n".join(text.splitlines()[idx - 1 : idx + 6])
                    if "ctx.Done" in look or "<-ctx" in look or "range" in look or "for job" in look:
                        continue
                    v.append({"rule": rule, "file": str(f), "line": idx, "snippet": line.strip(), "note": desc})
        if WG_ADD_BODY.search(text):
            v.append({"rule": "rule:r6", "file": str(f), "line": 0, "note": "wg.Add inside go func body"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        good = root / "good.go"
        good.write_text(
            "package x\nfunc Run(ctx context.Context, ch chan int){\n"
            "    go func() {\n        select { case ch <- 1: case <-ctx.Done(): return }\n    }()\n}\n",
            encoding="utf-8",
        )
        assert not scan(root), f"good case must pass"
        bad = root / "bad.go"
        bad.write_text(
            "package x\nfunc Leak() {\n    go func() {\n        for { time.Sleep(time.Second) }\n    }()\n}\n",
            encoding="utf-8",
        )
        v = scan(root)
        assert v, f"bad case must flag: {v}"
        assert any("rule:r2" in x["rule"] for x in v)
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
