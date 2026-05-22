#!/usr/bin/env python3
"""Validate a ConversationalAgents config against the F-066 output contract.

Usage:
  validate-multi-agent-conversational.py <config.yaml|config.json>
  validate-multi-agent-conversational.py --self-test
  validate-multi-agent-conversational.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def violations(cfg: dict) -> list[str]:
    errs: list[str] = []
    for key in ("agents", "termination_phrase", "max_turns", "window_size", "token_budget"):
        if key not in cfg:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs
    agents = cfg["agents"]
    if not isinstance(agents, list) or len(agents) < 2:
        errs.append("agents must be a list with >=2 items")
        return errs
    names = [a.get("name") for a in agents]
    prompts = [a.get("system_prompt", "") for a in agents]
    if len(set(names)) != len(names):
        errs.append("agent names must be unique")
    if len(set(prompts)) != len(prompts):
        errs.append("agent system_prompts must be distinct (rule r5-distinct-identities)")
    for a in agents:
        if len(a.get("system_prompt", "")) < 32:
            errs.append(f"agent {a.get('name')}: system_prompt too short (<32 chars)")
    if len(cfg.get("termination_phrase", "")) < 3:
        errs.append("termination_phrase must be >=3 chars (rule r1-dual-termination)")
    if not (2 <= cfg.get("max_turns", 0) <= 30):
        errs.append("max_turns must be in [2, 30] (rule r2-max-turns-ceiling)")
    if not (1 <= cfg.get("window_size", 0) <= 8):
        errs.append("window_size must be in [1, 8] (rule r3-sliding-window)")
    if cfg.get("token_budget", 0) < 5000:
        errs.append("token_budget must be >= 5000 (rule r4-per-turn-budget-audit)")
    return errs


_GOOD = {
    "agents": [
        {"name": "proposer", "model": "sonnet", "system_prompt": "You propose solutions for the user's debugging task."},
        {"name": "critic", "model": "opus", "system_prompt": "You critique the proposer; surface concrete counterexamples."},
    ],
    "termination_phrase": "TASK COMPLETE",
    "max_turns": 12, "window_size": 3, "token_budget": 20000,
}
_BAD = {
    "agents": [{"name": "a", "model": "sonnet", "system_prompt": "resp"}, {"name": "b", "model": "sonnet", "system_prompt": "resp"}],
    "termination_phrase": "", "max_turns": 200, "window_size": 99, "token_budget": 100,
}


def self_test() -> int:
    g, b = violations(_GOOD), violations(_BAD)
    if g:
        sys.stderr.write(f"self-test: good failed: {g}\n"); return 1
    if not b:
        sys.stderr.write("self-test: bad passed\n"); return 1
    sys.stdout.write(f"self-test ok (bad surfaced {len(b)} violations)\n"); return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        sys.stdout.write(__doc__ or ""); return 0
    if argv[0] == "--self-test":
        return self_test()
    p = Path(argv[0])
    try:
        if p.suffix in (".yaml", ".yml"):
            if yaml is None:
                raise SystemExit("PyYAML not installed")
            cfg = yaml.safe_load(p.read_text())
        else:
            cfg = json.loads(p.read_text())
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
