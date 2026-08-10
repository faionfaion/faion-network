#!/usr/bin/env python3
"""validate-stream-json-orchestration.py — validate a StreamJsonRunReport.

Inputs:
  - <report.json>  Path to a JSON file matching the 02-output-contract schema.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - report validates.
  1 - report violates schema or self-check rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in fixtures.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CLI_VALUES = {"claude-code", "codex", "aider", "opencode"}
SUBTYPES = {"success", "error_max_turns", "error_during_execution", "killed_by_orchestrator"}
KILL_REASONS = {None, "budget_cap", "safety_veto", "max_turns", "timeout", "user_abort"}
REPLAY_RE = re.compile(r"^runs/.+\.jsonl$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})$")

VALID_FIXTURE = {
    "session_id": "sess_abc123",
    "cli": "claude-code",
    "started_at": "2026-05-22T13:45:01Z",
    "ended_at": "2026-05-22T13:46:32Z",
    "events_count": 47,
    "result_subtype": "success",
    "total_cost_usd": 0.234,
    "kill_reason": None,
    "replay_path": "runs/sess_abc123.jsonl",
    "allowed_tools": ["Read", "Grep"],
    "max_turns": 20,
}

INVALID_FIXTURE = {
    "session_id": "",
    "cli": "claude-code",
    "started_at": "2026-05-22T13:45:01Z",
    "ended_at": "2026-05-22T13:46:32Z",
    "events_count": 0,
    "result_subtype": "success",
    "total_cost_usd": -0.5,
    "kill_reason": None,
    "replay_path": "out.txt",
}


def validate(report: dict) -> list[str]:
    v: list[str] = []
    required = ["session_id", "cli", "started_at", "ended_at", "events_count", "result_subtype", "total_cost_usd", "kill_reason", "replay_path"]
    for k in required:
        if k not in report:
            v.append(f"missing required key: {k}")
    if v:
        return v
    if not isinstance(report["session_id"], str) or not report["session_id"]:
        v.append("session_id must be non-empty string")
    if report["cli"] not in CLI_VALUES:
        v.append(f"cli must be one of {sorted(CLI_VALUES)} (got {report['cli']!r})")
    for tkey in ("started_at", "ended_at"):
        if not ISO_RE.match(str(report[tkey])):
            v.append(f"{tkey} must be ISO 8601 date-time")
    if not isinstance(report["events_count"], int) or report["events_count"] < 1:
        v.append("events_count must be int >= 1")
    if report["result_subtype"] not in SUBTYPES:
        v.append(f"result_subtype not in closed enum (got {report['result_subtype']!r})")
    if not isinstance(report["total_cost_usd"], (int, float)) or report["total_cost_usd"] < 0:
        v.append("total_cost_usd must be number >= 0")
    if report["kill_reason"] not in KILL_REASONS:
        v.append(f"kill_reason not in closed enum (got {report['kill_reason']!r})")
    if not REPLAY_RE.match(str(report["replay_path"])):
        v.append("replay_path must match ^runs/.+\\.jsonl$")
    # consistency
    if report.get("kill_reason") is None and report.get("result_subtype") == "killed_by_orchestrator":
        v.append("result_subtype=killed_by_orchestrator requires non-null kill_reason")
    if report.get("kill_reason") is not None and report.get("result_subtype") != "killed_by_orchestrator":
        v.append("kill_reason set but result_subtype != killed_by_orchestrator")
    return v


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv or "-h" in argv else 2
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
        report = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    violations = validate(report)
    if violations:
        sys.stdout.write("FAIL\n")
        for x in violations:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
