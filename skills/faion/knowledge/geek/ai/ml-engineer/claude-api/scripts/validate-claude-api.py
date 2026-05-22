#!/usr/bin/env python3
"""validate-claude-api.py

Validate a Claude API integration-record JSON against content/02-output-contract.xml.

Inputs:
    --file PATH      path to integration-record JSON
    --self-test      run built-in fixtures (valid + invalid)
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^cai-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED_MODELS = {"claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-7"}
ALLOWED_SHAPES = {"sync", "streaming", "tool-loop", "batch"}
ALLOWED_STRAT = {"exponential-jitter", "linear", "none"}
ALLOWED_SECRETS = {"env", "1password", "aws-secrets-manager", "vault"}
ALLOWED_TTL = {300, 3600}
ALLOWED_PREFIX_POS = {"system", "first-content-block"}
HAIKU_CACHE_MIN = 2048
NON_HAIKU_CACHE_MIN = 1024


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "model", "max_tokens", "shape", "retry", "caching", "tooling", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^cai-[a-z0-9-]{6,}$")
    if "model" in obj and obj["model"] not in ALLOWED_MODELS:
        errs.append(f"model must be one of {sorted(ALLOWED_MODELS)}")
    if "max_tokens" in obj:
        mt = obj["max_tokens"]
        if not isinstance(mt, int) or not (1 <= mt <= 32000):
            errs.append("max_tokens must be int in [1, 32000]")
    if "shape" in obj and obj["shape"] not in ALLOWED_SHAPES:
        errs.append(f"shape must be one of {sorted(ALLOWED_SHAPES)}")
    if obj.get("shape") == "tool-loop":
        mt = obj.get("max_turns")
        if not isinstance(mt, int) or not (1 <= mt <= 50):
            errs.append("tool-loop shape requires max_turns int in [1,50]")
    if obj.get("shape") == "batch" and "max_turns" in obj:
        errs.append("batch shape must not declare max_turns")
    retry = obj.get("retry") or {}
    if not isinstance(retry, dict):
        errs.append("retry must be object")
    else:
        if not retry.get("enabled"):
            errs.append("retry.enabled must be true (rule exponential-backoff-on-429-5xx)")
        ma = retry.get("max_attempts")
        if not isinstance(ma, int) or not (1 <= ma <= 10):
            errs.append("retry.max_attempts must be int in [1,10]")
        if retry.get("strategy") not in ALLOWED_STRAT:
            errs.append(f"retry.strategy must be one of {sorted(ALLOWED_STRAT)}")
        if retry.get("strategy") == "none" and retry.get("enabled"):
            errs.append("retry strategy=none contradicts enabled=true")
    cache = obj.get("caching") or {}
    if not isinstance(cache, dict):
        errs.append("caching must be object")
    else:
        if cache.get("enabled"):
            size = cache.get("block_token_size")
            if not isinstance(size, int):
                errs.append("caching.block_token_size must be int when enabled")
            else:
                model = obj.get("model", "")
                minimum = HAIKU_CACHE_MIN if "haiku" in model else NON_HAIKU_CACHE_MIN
                if size < minimum:
                    errs.append(f"caching.block_token_size {size} below {minimum} for model {model} (rule cacheable-block-minimum-size)")
            if cache.get("ttl_seconds") not in ALLOWED_TTL:
                errs.append(f"caching.ttl_seconds must be one of {sorted(ALLOWED_TTL)}")
            if cache.get("prefix_position") not in ALLOWED_PREFIX_POS:
                errs.append(f"caching.prefix_position must be one of {sorted(ALLOWED_PREFIX_POS)}")
    tooling = obj.get("tooling") or {}
    tc = tooling.get("tool_count", 0)
    if not isinstance(tc, int) or not (0 <= tc <= 10):
        errs.append("tooling.tool_count must be int in [0,10]")
    if obj.get("shape") == "tool-loop" and tc == 0:
        errs.append("tool-loop shape requires tool_count >= 1")
    et = obj.get("extended_thinking") or {}
    if et.get("enabled"):
        budget = et.get("budget_tokens")
        if not isinstance(budget, int) or budget < 1024:
            errs.append("extended_thinking.budget_tokens must be int >= 1024")
        if obj.get("model") != "claude-opus-4-7":
            errs.append("extended_thinking only allowed on claude-opus-4-7")
    if "secrets_source" in obj and obj["secrets_source"] not in ALLOWED_SECRETS:
        errs.append(f"secrets_source must be one of {sorted(ALLOWED_SECRETS)} (rule no-hardcoded-api-key)")
    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "cai-rag-summariser",
    "model": "claude-sonnet-4-6",
    "max_tokens": 4096,
    "shape": "tool-loop",
    "max_turns": 10,
    "retry": {"enabled": True, "max_attempts": 5, "strategy": "exponential-jitter"},
    "caching": {"enabled": True, "block_token_size": 2400, "ttl_seconds": 300, "prefix_position": "system"},
    "tooling": {"tool_count": 3, "forced_tool": False, "schema_validation": True},
    "extended_thinking": {"enabled": False},
    "secrets_source": "1password",
    "version": "1.1.0",
    "last_reviewed": "2026-05-22",
}

INVALID_FIXTURE = {
    "artefact_id": "x",
    "model": "claude-3-5-sonnet",
    "max_tokens": 999999,
    "shape": "batch",
    "max_turns": 100,
    "retry": {"enabled": False, "max_attempts": 0, "strategy": "none"},
    "caching": {"enabled": True, "block_token_size": 500, "ttl_seconds": 60},
    "tooling": {"tool_count": 25, "forced_tool": False},
    "secrets_source": "hardcoded",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
