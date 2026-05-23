#!/usr/bin/env python3
"""Validate portability-spec artefact.

USAGE:
    validate-prompt-portability-across-providers.py <input.json>
    validate-prompt-portability-across-providers.py --self-test
    validate-prompt-portability-across-providers.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROVIDERS = {"anthropic", "openai", "google", "azure", "mistral", "groq"}
LAYERS = {"tool_schema_only", "system_prompt_only", "tool_and_system", "full_adapter"}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
URL_RE = re.compile(r"^https?://")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "providers", "abstraction_layer", "tool_schema_adapter", "refusal_policy_ref", "inputs_used", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r} (rule r4)")
    pr = s.get("providers")
    if not isinstance(pr, list) or len(pr) < 2:
        v.append("providers must have ≥2 entries (rule r2; else skip-this-methodology)")
    elif isinstance(pr, list):
        for i, p in enumerate(pr):
            if not isinstance(p, dict):
                v.append(f"providers[{i}] must be object")
                continue
            if p.get("name") not in PROVIDERS:
                v.append(f"providers[{i}].name must be one of {sorted(PROVIDERS)}")
            if len((p.get("model") or "")) < 2:
                v.append(f"providers[{i}].model required")
            if not URL_RE.match(p.get("docs_url") or ""):
                v.append(f"providers[{i}].docs_url must be http(s) URL (rule r3)")
    if s.get("abstraction_layer") not in LAYERS:
        v.append(f"abstraction_layer must be one of {sorted(LAYERS)}")
    if not (s.get("tool_schema_adapter") or "").strip():
        v.append("tool_schema_adapter required")
    if not (s.get("refusal_policy_ref") or "").strip():
        v.append("refusal_policy_ref required")
    iu = s.get("inputs_used")
    if not isinstance(iu, list) or len(iu) < 2:
        v.append("inputs_used must have ≥2 entries (rule r3)")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO YYYY-MM-DD")
    return v


GOOD = {
    "artefact_id": "portability-support-bot-2026q2",
    "owner": "ruslan@faion.net",
    "providers": [
        {"name": "anthropic", "model": "claude-opus-4-7", "docs_url": "https://docs.anthropic.com/en/api/messages"},
        {"name": "openai", "model": "gpt-5-pro", "docs_url": "https://platform.openai.com/docs/api-reference/chat"},
    ],
    "abstraction_layer": "tool_and_system",
    "tool_schema_adapter": "faion.adapters.tools.universal_v2",
    "refusal_policy_ref": "git://faion/safety/refusal.md@a1b2c3d",
    "inputs_used": [
        {"name": "current_prompts", "source": "git://faion/prompts/support-bot.yaml"},
        {"name": "provider_matrix", "source": "git://faion/platform/providers.yaml"},
    ],
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "providers": [{"name": "anthropic", "model": "x", "docs_url": "nope"}],
    "abstraction_layer": "x",
    "tool_schema_adapter": "",
    "refusal_policy_ref": "",
    "inputs_used": [],
    "version": "v1",
    "last_reviewed": "yesterday",
}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("providers" in x for x in bad)
    assert any("abstraction_layer" in x for x in bad)
    assert any("tool_schema_adapter" in x for x in bad)
    assert any("owner" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-prompt-portability-across-providers.py")
    p.add_argument("path", nargs="?")
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
