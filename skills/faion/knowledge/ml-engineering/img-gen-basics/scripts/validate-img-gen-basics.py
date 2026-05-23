#!/usr/bin/env python3
"""Validate output contract for img-gen-basics config.

USAGE:
    validate-img-gen-basics.py <input.json>   Validate a config.
    validate-img-gen-basics.py --self-test    Run built-in fixture.
    validate-img-gen-basics.py --help         Show this help.

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

PROVIDERS = {"dalle3", "flux-schnell", "sdxl"}
DALLE_TIER1_RL = 5


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("provider", "prompt_builder", "storage_uri", "rate_limit_per_min", "log_revised_prompt"):
        if k not in c:
            v.append(f"missing required field: {k}")
    if c.get("provider") and c["provider"] not in PROVIDERS:
        v.append(f"provider invalid: {c['provider']!r}")
    pb = c.get("prompt_builder") or {}
    if not pb.get("subject") or not pb.get("style"):
        v.append("prompt_builder.subject and .style required (rule r1)")
    if not c.get("storage_uri"):
        v.append("storage_uri must be non-empty (rule r3)")
    rl = c.get("rate_limit_per_min")
    if isinstance(rl, int) and c.get("provider") == "dalle3" and rl > DALLE_TIER1_RL:
        v.append(f"rate_limit_per_min {rl} > DALL-E 3 tier-1 cap {DALLE_TIER1_RL} (rule r4)")
    if c.get("log_revised_prompt") is not True:
        v.append("log_revised_prompt must be true (rule r2)")
    return v


def _self_test() -> int:
    good = {
        "provider": "dalle3",
        "prompt_builder": {"subject": "skyline", "style": "cinematic"},
        "storage_uri": "s3://media/imgs/",
        "rate_limit_per_min": 5,
        "log_revised_prompt": True,
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = dict(good); bad["log_revised_prompt"] = False
    assert any("log_revised_prompt" in x for x in validate(bad)), "should require revised_prompt logging"
    bad = dict(good); bad["rate_limit_per_min"] = 60
    assert any("rate_limit_per_min" in x for x in validate(bad)), "should flag RL >5 for DALL-E 3"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-img-gen-basics.py")
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
