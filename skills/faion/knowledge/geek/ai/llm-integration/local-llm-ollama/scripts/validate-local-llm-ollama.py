#!/usr/bin/env python3
"""Validate output contract for local-llm-ollama config.

USAGE:
    validate-local-llm-ollama.py <input.json>   Validate an ollama-config.json.
    validate-local-llm-ollama.py --self-test    Run built-in fixture.
    validate-local-llm-ollama.py --help         Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

QUANT = {"q4_K_M", "q5_K_M", "q6_K", "q8_0", "f16"}
SIZE_FLOOR = {"7b": 8, "8b": 8, "13b": 16, "30b": 32, "34b": 32, "70b": 48}


def _size_floor(model: str) -> int | None:
    m = re.search(r"(\d+)b\b", model.lower())
    if not m:
        return None
    n = int(m.group(1))
    if n <= 8:
        return 8
    if n <= 13:
        return 16
    if n <= 34:
        return 32
    return 48


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("base_url", "model", "ram_floor_gb", "health_check_required", "openai_compat", "fallback_cloud_model"):
        if k not in c:
            v.append(f"missing required field: {k}")
    bu = c.get("base_url", "")
    if not bu.endswith("/v1"):
        v.append("base_url must end with /v1 (rule r4)")
    if c.get("health_check_required") is not True:
        v.append("health_check_required must be true (rule r2)")
    if c.get("openai_compat") is not True:
        v.append("openai_compat must be true (rule r4)")
    if not c.get("fallback_cloud_model"):
        v.append("fallback_cloud_model required")
    model = c.get("model", "")
    floor_required = _size_floor(model)
    floor_set = c.get("ram_floor_gb")
    if floor_required and isinstance(floor_set, int) and floor_set < floor_required:
        v.append(f"ram_floor_gb {floor_set} < required {floor_required} for {model} (rule r3)")
    q = c.get("quantisation")
    if q and q not in QUANT:
        v.append(f"quantisation invalid: {q!r}")
    return v


def _self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text())
    clean = {k: v for k, v in smoke.items() if not k.startswith("_")}
    assert validate(clean) == [], f"smoke must pass: {validate(clean)}"
    bad = dict(clean)
    bad["model"] = "llama3.1:70b"
    assert any("ram_floor_gb" in x for x in validate(bad)), "should flag 70B on 8GB"
    bad = dict(clean)
    bad["openai_compat"] = False
    assert any("openai_compat" in x for x in validate(bad)), "should flag non-OpenAI-compat"
    bad = dict(clean)
    bad["base_url"] = "http://localhost:11434"
    assert any("/v1" in x for x in validate(bad)), "should require /v1"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-local-llm-ollama.py")
    p.add_argument("path", nargs="?", help="JSON config to validate")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    raw = json.loads(Path(args.path).read_text())
    clean = {k: v for k, v in raw.items() if not k.startswith("_")}
    out = validate(clean)
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
