#!/usr/bin/env python3
"""validate-agentic-ai-product-development.py — Validate an agentic-AI product spec.

Inputs:
  - <spec.json>  Path to the spec JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - spec validates.
  1 - spec violates contract.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

OWNER_RE = re.compile(r"^[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
PREDICATE_OP_RE = re.compile(r"(==|!=|>=|<=|>|<|\bAND\b|\bOR\b)")

VALID_FIXTURE = {
    "product": "support-agent-v1",
    "owner": "ai-pm:alice",
    "version": "1.0.0",
    "goal_state": {
        "predicate": "ticket.status == 'resolved' AND csat >= 4",
        "evidence_source": "tickets_table + csat_survey",
    },
    "autonomous_actions": [
        {"action": "respond-faq", "trigger": "intent == 'faq' AND confidence > 0.8"}
    ],
    "escalation": {
        "triggers": ["confidence < 0.7", "retry_count > 2"],
        "human_role": "support-lead",
        "written_before_happy_path": True,
    },
    "metrics": {
        "goal_achievement_rate_target": 0.75,
        "autonomy_ratio_target": 0.6,
        "cost_per_task_target": 0.40,
    },
    "behavioural_regression": {
        "test_set_path": "tests/behavioural/v1.jsonl",
        "trigger_on_model_bump": True,
    },
}
INVALID_FIXTURE = {
    "product": "x",
    "goal_state": {"predicate": "solves the ticket"},
    "autonomous_actions": [{"action": "handle complex cases"}],
    "metrics": {"click_through_rate": 0.1},
}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    for k in ("product", "owner", "version", "goal_state", "autonomous_actions", "escalation", "metrics", "behavioural_regression"):
        if k not in spec:
            out.append(f"{k} missing")
    if "owner" in spec and not OWNER_RE.match(str(spec["owner"])):
        out.append("owner must be role:person")
    if "version" in spec and not SEMVER_RE.match(str(spec["version"])):
        out.append("version must be semver")
    goal = spec.get("goal_state", {})
    if isinstance(goal, dict):
        pred = str(goal.get("predicate", ""))
        if not pred or not PREDICATE_OP_RE.search(pred):
            out.append("goal_state.predicate must be machine-verifiable (contain operators)")
        if not goal.get("evidence_source"):
            out.append("goal_state.evidence_source missing")
    actions = spec.get("autonomous_actions", [])
    if not isinstance(actions, list) or not actions:
        out.append("autonomous_actions must be non-empty list")
    else:
        for i, a in enumerate(actions):
            if not isinstance(a, dict) or "action" not in a or not a.get("trigger"):
                out.append(f"autonomous_actions[{i}] missing trigger")
    esc = spec.get("escalation", {})
    if isinstance(esc, dict):
        if not esc.get("triggers"):
            out.append("escalation.triggers missing")
        if not esc.get("human_role"):
            out.append("escalation.human_role missing")
        if esc.get("written_before_happy_path") is not True:
            out.append("escalation.written_before_happy_path must be true")
    metrics = spec.get("metrics", {})
    for k in ("goal_achievement_rate_target", "autonomy_ratio_target", "cost_per_task_target"):
        if k not in metrics:
            out.append(f"metrics.{k} missing")
    forbidden_metric_keys = {"click_through_rate", "cost_per_user", "session_length"}
    primary_forbidden = set(metrics.keys()) & forbidden_metric_keys
    if primary_forbidden:
        out.append(f"metrics use forbidden primary keys: {sorted(primary_forbidden)}")
    br = spec.get("behavioural_regression", {})
    if not isinstance(br, dict) or not br.get("test_set_path") or br.get("trigger_on_model_bump") is not True:
        out.append("behavioural_regression must include test_set_path and trigger_on_model_bump==true")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(spec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
