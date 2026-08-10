#!/usr/bin/env python3
"""validate-inverted-header-content-first.py

Purpose:
    Validate a BlogPost-shaped JSON: body appears as the FIRST key
    (insertion order preserved by Python's json module), all required
    fields present.

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

SLUG_RE = re.compile(r"^[a-z0-9-]{1,80}$")
HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    keys = [k for k in obj.keys() if not k.startswith("_")]
    if not keys or keys[0] != "body":
        errs.append(f"`body` must be the FIRST key; got order {keys}")
    body = obj.get("body")
    if not isinstance(body, str) or len(body) < 200:
        errs.append("body: must be string >= 200 chars")
    title = obj.get("title")
    if not isinstance(title, str) or not (4 <= len(title) <= 90):
        errs.append("title: must be 4-90 char string")
    slug = obj.get("slug")
    if not isinstance(slug, str) or not SLUG_RE.match(slug):
        errs.append(f"slug: {slug!r} does not match kebab-case pattern")
    tags = obj.get("tags")
    if not isinstance(tags, list) or not (3 <= len(tags) <= 5):
        errs.append("tags: must be list of 3-5 items")
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
