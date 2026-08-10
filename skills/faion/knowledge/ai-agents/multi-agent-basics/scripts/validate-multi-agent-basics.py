#!/usr/bin/env python3
"""Validate a multi-agent spec (YAML or JSON) against the F-066 output contract.

Usage:
  validate-multi-agent-basics.py <spec.yaml|spec.json>      Validate one spec.
  validate-multi-agent-basics.py --self-test                Run against built-in fixtures.
  validate-multi-agent-basics.py --help                     Show this help.

Exit codes:
  0 — spec valid.
  1 — spec violates one or more contract rules.
  2 — usage error or unreadable input.

Inputs:  one spec file matching MultiAgentSpec schema.
Outputs: violations on stderr.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None  # falls through to json-only mode

NAME_RE = re.compile(r"^[a-z][a-z0-9_-]{1,32}$")
SVER_RE = re.compile(r"^v\d+$")
PATTERNS = {"sequential", "parallel", "hierarchical", "debate", "collaborative", "conversational"}
AUTHORITIES = {"orchestrator", "judge", "majority_vote", "human_in_loop"}
MODELS = {"opus", "sonnet", "haiku", "gpt-4o", "gpt-4o-mini", "o3", "o4-mini", "gpt-5"}
TERMINATIONS = {"max_turns", "phrase", "shape_check", "predicate"}

# Words too generic to count as overlap signals.
STOPWORDS = {"the", "and", "of", "to", "for", "a", "in", "on", "with", "from", "as", "that", "by", "or", "an", "produce", "write", "generate", "ensure", "agent"}


def _significant_nouns(role: str) -> set[str]:
    return {w for w in re.findall(r"[a-zA-Z]+", role.lower()) if len(w) > 3 and w not in STOPWORDS}


def violations(spec: dict) -> list[str]:
    errs: list[str] = []
    for key in ("task", "agents", "pattern", "message_schema", "budget", "termination", "decision_authority"):
        if key not in spec:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    if spec["pattern"] not in PATTERNS:
        errs.append(f"pattern invalid: {spec['pattern']!r} (allowed: {sorted(PATTERNS)})")
    if spec["decision_authority"] not in AUTHORITIES:
        errs.append(f"decision_authority invalid: {spec['decision_authority']!r}")

    agents = spec["agents"]
    if not isinstance(agents, list) or len(agents) < 2:
        errs.append("agents must be a list with >=2 items")
        return errs

    sum_budget = 0
    for ag in agents:
        for k in ("name", "role", "model", "system_prompt", "token_budget", "timeout_s"):
            if k not in ag:
                errs.append(f"agent {ag.get('name', '?')}: missing {k}")
        if "name" in ag and not NAME_RE.match(ag["name"]):
            errs.append(f"agent name invalid: {ag['name']!r}")
        if ag.get("model") not in MODELS:
            errs.append(f"agent {ag.get('name')}: model {ag.get('model')!r} not in allow-list")
        if isinstance(ag.get("system_prompt"), str) and len(ag["system_prompt"]) < 32:
            errs.append(f"agent {ag.get('name')}: system_prompt too short (<32 chars)")
        if isinstance(ag.get("token_budget"), int):
            sum_budget += ag["token_budget"]

    for i, a in enumerate(agents):
        for b in agents[i + 1:]:
            overlap = _significant_nouns(a.get("role", "")) & _significant_nouns(b.get("role", ""))
            if len(overlap) >= 3:
                errs.append(f"role overlap between {a['name']} and {b['name']}: shared nouns {sorted(overlap)}")

    ms = spec["message_schema"]
    if not isinstance(ms, dict) or "schema_version" not in ms or not SVER_RE.match(str(ms.get("schema_version", ""))):
        errs.append("message_schema.schema_version must match ^v\\d+$ (rule r3-structured-json)")

    budget = spec["budget"]
    if budget.get("total_tokens", 0) < sum_budget:
        errs.append(f"budget.total_tokens ({budget.get('total_tokens')}) < sum(agents.token_budget) ({sum_budget})")
    if sum_budget > 0.9 * budget.get("total_tokens", 1):
        errs.append("sum(agents.token_budget) exceeds 90% of total_tokens — leave ≥10% for orchestrator overhead")

    term = spec["termination"]
    if term.get("kind") not in TERMINATIONS:
        errs.append(f"termination.kind invalid: {term.get('kind')!r}")
    if term.get("kind") == "max_turns" and term.get("max_turns", 0) > 30:
        errs.append("termination.max_turns > 30 looks like a runaway; cap explicitly")

    if spec["pattern"] == "debate":
        names = {a["name"] for a in agents}
        if len(agents) < 3 or "judge" not in names:
            errs.append("pattern=debate requires >=3 agents including one named 'judge'")

    return errs


_FIXTURE_GOOD = {
    "task": "Summarise pydantic v2 deprecations in 200 words",
    "pattern": "sequential",
    "decision_authority": "orchestrator",
    "message_schema": {"schema_version": "v1", "fields": ["schema_version", "from", "to", "payload"]},
    "budget": {"total_tokens": 16000, "wallclock_s": 180},
    "termination": {"kind": "predicate", "predicate": "result.summary != null"},
    "agents": [
        {"name": "researcher", "role": "Gather pydantic v2 changelog deprecation notes", "model": "haiku",
         "system_prompt": "You are a research specialist; output JSON findings", "token_budget": 4000, "timeout_s": 45},
        {"name": "writer", "role": "Compose 200-word summary from findings without new claims", "model": "sonnet",
         "system_prompt": "You are a technical writer; output JSON summary", "token_budget": 5000, "timeout_s": 60},
        {"name": "editor", "role": "Tighten clarity and verify every claim has source_url", "model": "sonnet",
         "system_prompt": "You are a senior editor; output JSON final_summary", "token_budget": 3500, "timeout_s": 45},
    ],
}

_FIXTURE_BAD = {
    "task": "x",
    "pattern": "debate",
    "decision_authority": "vibes",
    "message_schema": {"fields": []},
    "budget": {"total_tokens": 100, "wallclock_s": 10},
    "termination": {"kind": "max_turns", "max_turns": 9000},
    "agents": [
        {"name": "researcher", "role": "Research findings and write findings summary", "model": "opus",
         "system_prompt": "x", "token_budget": 5000, "timeout_s": 30},
        {"name": "Researcher2", "role": "Research findings and write summary findings again", "model": "opus",
         "system_prompt": "x", "token_budget": 5000, "timeout_s": 30},
    ],
}


def self_test() -> int:
    good = violations(_FIXTURE_GOOD)
    bad = violations(_FIXTURE_BAD)
    failed = False
    if good:
        sys.stderr.write(f"self-test: good fixture unexpectedly failed: {good}\n")
        failed = True
    if not bad:
        sys.stderr.write("self-test: bad fixture unexpectedly passed\n")
        failed = True
    if failed:
        return 1
    sys.stdout.write(f"self-test ok (bad surfaced {len(bad)} violations)\n")
    return 0


def _load(path: Path) -> dict:
    txt = path.read_text()
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            raise SystemExit("PyYAML not installed; cannot read YAML")
        return yaml.safe_load(txt)
    return json.loads(txt)


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        sys.stdout.write(__doc__ or "")
        return 0
    if argv[0] == "--self-test":
        return self_test()
    try:
        spec = _load(Path(argv[0]))
    except (OSError, ValueError) as e:
        sys.stderr.write(f"cannot read spec {argv[0]}: {e}\n")
        return 2
    errs = violations(spec)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write(f"{argv[0]}: ok\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
