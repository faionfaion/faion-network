#!/usr/bin/env python3
"""Validate output contract for img-gen-tools config.

USAGE:
    validate-img-gen-tools.py <input.json>   Validate ImageService config.
    validate-img-gen-tools.py --self-test    Run built-in fixture.
    validate-img-gen-tools.py --help         Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROVIDERS = {"dalle3", "flux-schnell", "sdxl", "stability"}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("providers", "fallback_chain", "cache_uri", "template_library_path", "attribution_enabled"):
        if k not in c:
            v.append(f"missing required field: {k}")
    prov = c.get("providers") or []
    if not isinstance(prov, list) or not prov:
        v.append("providers must be non-empty")
    else:
        for p in prov:
            if p not in PROVIDERS:
                v.append(f"providers contains invalid: {p!r}")
    fc = c.get("fallback_chain") or []
    if not isinstance(fc, list) or len(fc) < 2:
        v.append("fallback_chain must have >=2 entries (rule r4)")
    if not c.get("cache_uri"):
        v.append("cache_uri must be non-empty (rule r2)")
    if c.get("attribution_enabled") is not True:
        v.append("attribution_enabled must be true (rule r5)")
    return v


def _self_test() -> int:
    good = {
        "providers": ["dalle3", "flux-schnell", "sdxl"],
        "fallback_chain": ["dalle3", "flux-schnell", "sdxl"],
        "cache_uri": "s3://img-cache/",
        "template_library_path": "templates/prompt-templates.py",
        "attribution_enabled": True,
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = dict(good); bad["fallback_chain"] = ["dalle3"]
    assert any("fallback_chain" in x for x in validate(bad)), "should reject single-entry fallback"
    bad = dict(good); bad["attribution_enabled"] = False
    assert any("attribution_enabled" in x for x in validate(bad)), "should require attribution"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-img-gen-tools.py")
    p.add_argument("path", nargs="?", help="JSON config to validate")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
