#!/usr/bin/env python3
"""Validate a CollaborativeGroup config against the F-066 output contract.

Usage:
  validate-multi-agent-collaborative.py <config.yaml|config.json>
  validate-multi-agent-collaborative.py --self-test
  validate-multi-agent-collaborative.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def violations(cfg: dict) -> list[str]:
    errs: list[str] = []
    for key in ("contributors", "synthesizer", "max_iterations", "token_budget", "workspace_entry_schema"):
        if key not in cfg:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs
    contributors = cfg["contributors"]
    if not isinstance(contributors, list) or len(contributors) < 2:
        errs.append("contributors must be a list with >=2 items")
    names = [c.get("name") for c in contributors]
    if len(set(names)) != len(names):
        errs.append("contributor names must be unique")
    synth = cfg["synthesizer"]
    if synth.get("name") in names:
        errs.append(f"synthesizer.name {synth.get('name')!r} must not be a contributor (rule r3-independent-synthesizer)")
    if not (1 <= cfg["max_iterations"] <= 10):
        errs.append("max_iterations must be in [1, 10] (rule r2-iteration-cap)")
    if cfg["token_budget"] < 5000:
        errs.append("token_budget must be >= 5000")
    lower_bound = cfg["max_iterations"] * len(contributors) * 1500
    if cfg["token_budget"] < lower_bound:
        errs.append(f"token_budget {cfg['token_budget']} < lower bound {lower_bound} (max_iterations × contributors × 1500)")
    ws = cfg["workspace_entry_schema"]
    if "schema_version" not in ws:
        errs.append("workspace_entry_schema must declare schema_version")
    for c in contributors:
        if len(c.get("system_prompt", "")) < 32:
            errs.append(f"contributor {c.get('name')!r}: system_prompt too short (<32 chars)")
    return errs


_GOOD = {
    "contributors": [
        {"name": "a", "model": "sonnet", "system_prompt": "You are a UX lead. Output JSON {idea,rationale,risk}."},
        {"name": "b", "model": "sonnet", "system_prompt": "You are a backend lead. Output JSON {idea,rationale,risk}."},
    ],
    "synthesizer": {"name": "editor", "model": "opus"},
    "max_iterations": 4, "token_budget": 30000,
    "workspace_entry_schema": {"agent": "str", "iteration": "int", "content": "object", "ts": "str", "schema_version": "v1"},
}
_BAD = {"contributors": [{"name": "x", "model": "sonnet", "system_prompt": "..."}],
        "synthesizer": {"name": "x", "model": "sonnet"}, "max_iterations": 50, "token_budget": 100,
        "workspace_entry_schema": {}}


def self_test() -> int:
    g, b = violations(_GOOD), violations(_BAD)
    if g:
        sys.stderr.write(f"self-test: good fixture failed: {g}\n"); return 1
    if not b:
        sys.stderr.write("self-test: bad fixture passed\n"); return 1
    sys.stdout.write(f"self-test ok (bad surfaced {len(b)} violations)\n"); return 0


def _load(p: Path) -> dict:
    txt = p.read_text()
    if p.suffix in (".yaml", ".yml"):
        if yaml is None:
            raise SystemExit("PyYAML not installed")
        return yaml.safe_load(txt)
    return json.loads(txt)


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        sys.stdout.write(__doc__ or ""); return 0
    if argv[0] == "--self-test":
        return self_test()
    try:
        cfg = _load(Path(argv[0]))
    except (OSError, ValueError) as e:
        sys.stderr.write(f"cannot read {argv[0]}: {e}\n"); return 2
    errs = violations(cfg)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write(f"{argv[0]}: ok\n"); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
