#!/usr/bin/env python3
"""Validate a Checkpoint Ledger Spec against the on-disk-checkpoint-ledger contract.

Several fields exist only so a guard is stated rather than assumed, and those have
exactly one permitted value (mark_creates_dirs, in_flight_written,
auto_redispatch_on_stale, cli_writes_checkpoints, gitignored). The validator
rejects the other value with the rule that forbids it.

Usage:
  validate-on-disk-checkpoint-ledger.py <spec.yaml|spec.json>
  validate-on-disk-checkpoint-ledger.py --self-test
  validate-on-disk-checkpoint-ledger.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

MARKER_STATES = {"in-flight", "done", "failed"}
RECORD_FIELDS = {"identity", "snapshot", "provenance", "status"}
BOUNDARIES = {"model_call", "non_idempotent_side_effect", "risky_step", "human_gate"}
HISTORY_TOKENS = ("iso_ts", "phase", "status")
PHASE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

REQUIRED_KEYS = (
    "system",
    "state_root",
    "gitignored",
    "unit_id_pattern",
    "lineage",
    "enrol_command",
    "mark_command",
    "mark_creates_dirs",
    "marker_states",
    "in_flight_written",
    "history_file",
    "history_line_format",
    "lock",
    "record_fields",
    "write_boundaries",
    "has_non_idempotent_side_effects",
    "has_human_gate",
    "rollback_command",
    "dead_letter_after_minutes",
    "liveness_check",
    "auto_redispatch_on_stale",
    "cli_writes_checkpoints",
)

# field -> (required value, rule id, why)
FIXED = {
    "gitignored": (True, "r3-append-only-per-unit-history", "run state in version control conflicts on every tick"),
    "mark_creates_dirs": (False, "r1-identity-checked-before-write", "a marker writer that creates directories turns a typo into a phantom unit"),
    "auto_redispatch_on_stale": (False, "r6-stale-in-flight-goes-to-dead-letter", "blind resume runs ahead of the rate-limit gate"),
    "cli_writes_checkpoints": (False, "r7-orchestration-decisions-stay-caller-side", "a tool that does not own the run must not advance it"),
}


def violations(spec: dict) -> list[str]:
    errs: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in spec:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    if len(str(spec["system"]).strip()) < 12:
        errs.append("system must name the orchestrator being specified (>=12 chars)")

    for key, (want, rule, why) in FIXED.items():
        if spec[key] is not want:
            errs.append(f"{key} must be {str(want).lower()}: {why} ({rule})")

    if spec["in_flight_written"] != "before_dispatch":
        errs.append(
            "in_flight_written must be 'before_dispatch': a marker written after dispatch turns "
            "a crash into silence (r2-in-flight-marker-before-dispatch)"
        )

    # r1 — one creation path, and it is not the marker writer.
    if str(spec["enrol_command"]).strip() == str(spec["mark_command"]).strip():
        errs.append(
            "enrol_command and mark_command must be distinct: directory creation has exactly one "
            "path (r1-identity-checked-before-write)"
        )
    try:
        re.compile(str(spec["unit_id_pattern"]))
    except re.error as exc:
        errs.append(f"unit_id_pattern is not a valid regex: {exc} (r1-identity-checked-before-write)")

    # Lineage is what makes "at or after" meaningful for rollback.
    lineage = spec["lineage"]
    if not isinstance(lineage, list) or len(lineage) < 2:
        errs.append("lineage must be an ordered list of >=2 phase names (r5-rollback-is-truncate-and-requeue)")
        lineage = []
    else:
        if len(set(lineage)) != len(lineage):
            errs.append("lineage phase names must be unique (r5-rollback-is-truncate-and-requeue)")
        for p in lineage:
            if not isinstance(p, str) or not PHASE_RE.fullmatch(p):
                errs.append(f"lineage phase {p!r} must match ^[a-z0-9][a-z0-9-]*$ (used in marker filenames)")

    # r5 — the three-state vocabulary is closed; rolled-back is a history verb.
    states = spec["marker_states"]
    if not isinstance(states, list) or set(states) != MARKER_STATES:
        extra = sorted(set(states) - MARKER_STATES) if isinstance(states, list) else []
        missing = sorted(MARKER_STATES - set(states)) if isinstance(states, list) else sorted(MARKER_STATES)
        detail = []
        if extra:
            detail.append(f"unexpected {extra}")
        if missing:
            detail.append(f"missing {missing}")
        errs.append(
            "marker_states must be exactly ['in-flight', 'done', 'failed'] — "
            + (", ".join(detail) if detail else "wrong shape")
            + "; 'rolled-back' is a history verb, not a marker (r5-rollback-is-truncate-and-requeue)"
        )

    # r3 — the history line must carry enough to reconstruct the run.
    fmt = str(spec["history_line_format"])
    for token in HISTORY_TOKENS:
        if token not in fmt:
            errs.append(f"history_line_format missing {token!r} (r3-append-only-per-unit-history)")
    if not any(t in fmt for t in ("reason", "commit", "detail")):
        errs.append(
            "history_line_format must carry a reason/commit/detail token; a status with no cause "
            "is unreadable after an incident (r3-append-only-per-unit-history)"
        )
    if len(str(spec["lock"]).strip()) < 4:
        errs.append("lock must name the mutual-exclusion mechanism guarding appends (r3-append-only-per-unit-history)")

    rf = spec["record_fields"]
    if not isinstance(rf, list) or not RECORD_FIELDS.issubset(set(rf)):
        missing = sorted(RECORD_FIELDS - set(rf)) if isinstance(rf, list) else sorted(RECORD_FIELDS)
        errs.append(f"record_fields missing {missing} (02-output-contract)")

    # r4 — boundaries follow from what the run actually does.
    wb = spec["write_boundaries"]
    if not isinstance(wb, list):
        errs.append("write_boundaries must be a list (r4-declared-write-boundaries)")
    else:
        for b in sorted(set(wb) - BOUNDARIES):
            errs.append(f"write_boundaries has unknown boundary {b!r}; vocabulary is {sorted(BOUNDARIES)}")
        if "model_call" not in wb:
            errs.append("write_boundaries must include 'model_call' (r4-declared-write-boundaries)")
        if spec["has_non_idempotent_side_effects"] and "non_idempotent_side_effect" not in wb:
            errs.append(
                "has_non_idempotent_side_effects is true but 'non_idempotent_side_effect' is not a "
                "write boundary: a resume would repeat it (r4-declared-write-boundaries)"
            )
        if spec["has_human_gate"] and "human_gate" not in wb:
            errs.append(
                "has_human_gate is true but 'human_gate' is not a write boundary: the gate would "
                "have to be held by a live process (r4-declared-write-boundaries)"
            )

    # r5 — rollback must be addressable by unit AND phase.
    rb = str(spec["rollback_command"])
    if "<unit" not in rb and "$unit" not in rb and "{unit" not in rb:
        errs.append("rollback_command must take a unit argument (r5-rollback-is-truncate-and-requeue)")
    if "<phase" not in rb and "$phase" not in rb and "{phase" not in rb:
        errs.append(
            "rollback_command must take a phase argument; rolling a whole unit back is a delete, "
            "not a rollback (r5-rollback-is-truncate-and-requeue)"
        )

    # r6 — sweep needs a real threshold and a real liveness check.
    dl = spec["dead_letter_after_minutes"]
    if not isinstance(dl, int) or isinstance(dl, bool) or dl < 1:
        errs.append("dead_letter_after_minutes must be a positive integer (r6-stale-in-flight-goes-to-dead-letter)")
    if len(str(spec["liveness_check"]).strip()) < 8:
        errs.append(
            "liveness_check must state how the sweep proves the agent is gone; a timer alone is "
            "not a liveness check (r6-stale-in-flight-goes-to-dead-letter)"
        )

    return errs


def load(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            print("PyYAML required for YAML specs; install pyyaml or pass JSON", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(raw)
    return json.loads(raw)


def _spec(**over: object) -> dict:
    base = {
        "system": "cron-driven agent pool over an on-disk task queue",
        "state_root": ".pool/states",
        "gitignored": True,
        "unit_id_pattern": "^[a-z0-9][a-z0-9-]{2,63}$",
        "lineage": ["brief", "draft", "review", "publish"],
        "enrol_command": "scripts/enrol.sh <unit>",
        "mark_command": "scripts/mark.sh <unit> <phase> <status> [reason]",
        "mark_creates_dirs": False,
        "marker_states": ["in-flight", "done", "failed"],
        "in_flight_written": "before_dispatch",
        "history_file": "history.log",
        "history_line_format": "<iso_ts> <phase> <status> <commit-or-reason>",
        "lock": "flock on .pool/states/.lock",
        "record_fields": ["identity", "snapshot", "provenance", "status"],
        "write_boundaries": ["model_call", "non_idempotent_side_effect", "risky_step", "human_gate"],
        "has_non_idempotent_side_effects": True,
        "has_human_gate": True,
        "rollback_command": "scripts/rollback.sh <unit> <phase> <reason>",
        "dead_letter_after_minutes": 180,
        "liveness_check": "pid in the marker is checked with kill -0 before any sweep action",
        "auto_redispatch_on_stale": False,
        "cli_writes_checkpoints": False,
    }
    base.update(over)
    return base


def self_test() -> int:
    cases = [
        ("valid spec", _spec(), 0),
        ("marker written after dispatch", _spec(in_flight_written="after_dispatch"), 1),
        ("mark tool creates directories", _spec(mark_creates_dirs=True), 1),
        ("extra marker state 'skipped'", _spec(marker_states=["in-flight", "done", "failed", "skipped"]), 1),
        ("stale markers auto-redispatched", _spec(auto_redispatch_on_stale=True), 1),
        ("side effects but no side-effect boundary", _spec(write_boundaries=["model_call", "risky_step", "human_gate"]), 1),
        ("rollback takes no phase", _spec(rollback_command="scripts/rollback.sh <unit>"), 1),
        ("liveness check is just a timer", _spec(liveness_check="age"), 1),
        ("enrol and mark are the same command", _spec(enrol_command="scripts/mark.sh <unit> <phase> <status> [reason]"), 1),
        ("history line has no reason token", _spec(history_line_format="<iso_ts> <phase> <status>"), 1),
        ("cli advances the run", _spec(cli_writes_checkpoints=True), 1),
        ("single-phase lineage", _spec(lineage=["only"]), 1),
    ]
    failed = 0
    for name, doc, expect in cases:
        errs = violations(doc)
        got = 1 if errs else 0
        if got != expect:
            failed += 1
        status = "ok " if got == expect else "FAIL"
        print(f"[{status}] {name}" + (f" -> {errs[0]}" if errs else ""))
    print(f"\n{len(cases) - failed}/{len(cases)} self-tests passed")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[1] == "--self-test":
        return self_test()
    path = Path(argv[1])
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    errs = violations(load(path))
    if not errs:
        print(f"OK  {path}")
        return 0
    print(f"FAIL  {path}", file=sys.stderr)
    for e in errs:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
