#!/usr/bin/env python3
"""Validate output contract for multi-agent-orchestration-decision-tree.

USAGE:
    validate-multi-agent-orchestration-decision-tree.py <input.json>  Validate a record.
    validate-multi-agent-orchestration-decision-tree.py --self-test    Run built-in fixture.
    validate-multi-agent-orchestration-decision-tree.py --help         Show this help.

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

PLURAL_OWNER = re.compile(r"^(team|we|us|engineering|the (team|squad|group))$", re.I)
TOPOLOGIES = {"single", "hierarchical", "collaborative", "conversational"}
HANDOFF_KEYS = ("task_id", "scoped_context", "success_criteria", "escalation")
ROLLBACK_KEYS = ("latency_threshold_ms", "cost_threshold_multiplier", "quality_threshold_pp")


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("subtasks", "topology_pick", "handoff_protocol", "judge_actor_used", "rollback_trigger", "owner"):
        if k not in c:
            v.append(f"missing required field: {k}")
    tp = c.get("topology_pick")
    if tp and tp not in TOPOLOGIES:
        v.append(f"topology_pick invalid: {tp!r}")
    hp = c.get("handoff_protocol") or {}
    if tp and tp != "single":
        for k in HANDOFF_KEYS:
            if not hp.get(k):
                v.append(f"handoff_protocol.{k} required for non-single topology (rule r3, fm-02)")
    judge = c.get("judge_actor_used") or {}
    if judge.get("used"):
        lift = judge.get("quality_lift_pp")
        cm = judge.get("cost_multiplier")
        if isinstance(lift, (int, float)) and lift < 2:
            v.append(f"judge_actor.quality_lift_pp={lift} < 2 — judge-actor not justified (rule r4)")
        if isinstance(cm, (int, float)) and cm > 2:
            v.append(f"judge_actor.cost_multiplier={cm} > 2 — too expensive")
    rb = c.get("rollback_trigger") or {}
    for k in ROLLBACK_KEYS:
        if k not in rb:
            v.append(f"rollback_trigger.{k} required (rule r5)")
    owner = (c.get("owner") or "").strip()
    if not owner:
        v.append("owner empty")
    elif PLURAL_OWNER.match(owner):
        v.append(f"owner is plural/generic: {owner!r}")
    return v


def _self_test() -> int:
    good = {
        "subtasks": ["plan", "execute", "verify"],
        "topology_pick": "hierarchical",
        "handoff_protocol": {
            "task_id": "<uuid>",
            "scoped_context": "subset by tag",
            "success_criteria": "passes verifier",
            "escalation": "human-on-call",
        },
        "judge_actor_used": {"used": True, "quality_lift_pp": 3.5, "cost_multiplier": 1.4},
        "rollback_trigger": {"latency_threshold_ms": 2500, "cost_threshold_multiplier": 2.0, "quality_threshold_pp": -2},
        "owner": "alice@example.com",
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = dict(good); bad["judge_actor_used"] = {"used": True, "quality_lift_pp": 0.5, "cost_multiplier": 1.4}
    assert any("quality_lift_pp" in x for x in validate(bad)), "should reject cargo-cult judge"
    bad = dict(good); bad["handoff_protocol"] = {}
    assert any("handoff_protocol" in x for x in validate(bad)), "should require hand-off fields for multi-agent"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-multi-agent-orchestration-decision-tree.py")
    p.add_argument("path", nargs="?", help="JSON record to validate")
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
