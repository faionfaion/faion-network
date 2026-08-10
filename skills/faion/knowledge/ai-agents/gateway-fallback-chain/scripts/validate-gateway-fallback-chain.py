#!/usr/bin/env python3
"""validate-gateway-fallback-chain.py

Purpose:
    Validate a gateway call request body: presence of `models` chain,
    at least 2 distinct providers, primary model present in chain.

Inputs:
    --file PATH      JSON to validate
    --self-test      Validate the built-in smoke fixture

Outputs:
    Stdout: validation report
    Exit 0 on pass, 1 on failure, 2 on usage error.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MODEL_RE = re.compile(r"^[a-z0-9-]+/[a-z0-9.\-]+$")
HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj.get("model"), str):
        errs.append("model: required string missing")
    if not isinstance(obj.get("messages"), list) or not obj["messages"]:
        errs.append("messages: required non-empty list")
    models = obj.get("models")
    if not isinstance(models, list) or len(models) < 2:
        errs.append("models: must be a list of at least 2 entries")
        return errs
    for i, m in enumerate(models):
        if not isinstance(m, str) or not MODEL_RE.match(m):
            errs.append(f"models[{i}]: {m!r} does not match provider/model pattern")
    providers = {m.split("/", 1)[0] for m in models if isinstance(m, str) and "/" in m}
    if len(providers) < 2:
        errs.append(f"models: must include at least 2 distinct providers; got {sorted(providers)}")
    if obj.get("model") and obj["model"] not in models:
        errs.append(f"model {obj['model']!r} must appear in models chain")
    return errs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--file", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    target = SMOKE if args.self_test else args.file
    if target is None:
        p.error("either --file or --self-test must be given")
    if not target.exists():
        sys.stdout.write(f"FAIL: file not found: {target}\n")
        return 1
    obj = json.loads(target.read_text(encoding="utf-8"))
    obj = {k: v for k, v in obj.items() if not k.startswith("_")}
    errs = validate(obj)
    if errs:
        sys.stdout.write(f"FAIL: {target}\n")
        for e in errs:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write(f"OK: {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
