#!/usr/bin/env python3
"""validate-agents.py — Validate a faion-mvp-scope-analyzer-agent / faion-mlp-agent run record.

Inputs:
  - <run.json>  Path to the run record JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - run validates.
  1 - run violates mode / vcs / comparables / review rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_AGENTS = {"faion-mvp-scope-analyzer-agent", "faion-mlp-agent"}
ALLOWED_MODES = {"analyze", "find-gaps", "propose", "update", "plan", "mvp-scope"}
MIN_COMPARABLES = 3

VALID_FIXTURE = {
    "agent": "faion-mlp-agent",
    "mode": "update",
    "input_artefacts": [{"name": "propose-output", "source": "runs/2026-05-22/propose.json"}],
    "output_artefacts": ["specs/mlp-v2.md"],
    "human_review_status": "approved",
    "vcs_state": {"clean_tree_before_run": True, "commit_sha_before_run": "abc123"},
}
INVALID_FIXTURE = {
    "agent": "faion-mlp-agent",
    "mode": "update",
    "input_artefacts": [],
    "output_artefacts": ["specs/mlp-v2.md"],
    "human_review_status": "pending",
    "vcs_state": {"clean_tree_before_run": False, "commit_sha_before_run": ""},
}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    agent = spec.get("agent")
    if agent not in ALLOWED_AGENTS:
        out.append(f"agent must be one of {sorted(ALLOWED_AGENTS)}")
    mode = spec.get("mode")
    if mode not in ALLOWED_MODES:
        out.append(f"mode must be one of {sorted(ALLOWED_MODES)}")
    inputs = spec.get("input_artefacts", [])
    if not isinstance(inputs, list) or not inputs:
        out.append("input_artefacts must be non-empty")
    outputs = spec.get("output_artefacts", [])
    if not isinstance(outputs, list) or not outputs:
        out.append("output_artefacts must be non-empty")
    if mode == "update":
        if spec.get("human_review_status") != "approved":
            out.append("mode:update requires human_review_status == 'approved' (rule r2)")
        vcs = spec.get("vcs_state", {})
        if not vcs.get("clean_tree_before_run"):
            out.append("mode:update requires vcs_state.clean_tree_before_run == true (rule r3)")
    if agent == "faion-mvp-scope-analyzer-agent":
        cmp_list = spec.get("comparables", [])
        if not isinstance(cmp_list, list) or len(cmp_list) < MIN_COMPARABLES:
            out.append(f"faion-mvp-scope-analyzer-agent requires >= {MIN_COMPARABLES} comparables (rule r4)")
    weights = spec.get("mlp_dimensions_weights")
    if isinstance(weights, dict) and weights:
        total = sum(float(weights.get(k, 0)) for k in ("delight", "ease", "speed", "trust", "personality"))
        if abs(total - 1.0) > 0.01 and total > 0:
            out.append(f"mlp_dimensions_weights should sum to 1.0 (got {total:.2f})")
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
