#!/usr/bin/env python3
"""Validate a Gate Failure Contract against the gate-fail-closed-rule contract.

Usage:
  validate-gate-fail-closed-rule.py <gfc.yaml|gfc.json>
  validate-gate-fail-closed-rule.py --self-test
  validate-gate-fail-closed-rule.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

INSTRUMENTS = {"static", "trigger-eval", "judge", "manual"}
CHANNELS = {"exit_code", "findings", "both"}
SEVERITIES = ["low", "medium", "high", "critical"]
KNOWN_MODES = {"parse", "refusal", "truncation", "transport", "empty", "crash", "absent_input"}

# Which non-evaluating modes MUST be enumerated, per instrument (r2).
MANDATORY_MODES = {
    "judge": {"parse", "refusal", "truncation", "transport", "empty"},
    "trigger-eval": {"parse", "truncation", "transport", "empty"},
    "static": {"crash", "absent_input"},
    "manual": {"absent_input", "crash"},
}

# `emits` values that mean "did not actually fail closed" (r1).
FORBIDDEN_EMITS = {"", "pass", "ignore", "warn", "warning", "none", "null", "skip", "exit:0"}

REQUIRED_KEYS = (
    "gate",
    "instrument",
    "invocation",
    "verdict_channel",
    "failure_modes",
    "forbidden_paths",
    "degraded_override",
    "fault_injection_proof",
    "last_proved",
)


def _sev_rank(sev: str) -> int:
    try:
        return SEVERITIES.index(str(sev).strip().lower())
    except ValueError:
        return -1


def _parse_date(value: object) -> date | None:
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value).strip())
    except (ValueError, AttributeError):
        return None


def violations(gfc: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(gfc, dict):
        return ["contract root must be a mapping"]

    for key in REQUIRED_KEYS:
        if key not in gfc:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    instrument = str(gfc["instrument"]).strip()
    if instrument not in INSTRUMENTS:
        errs.append(f"instrument {instrument!r} not in {sorted(INSTRUMENTS)}")
    channel = str(gfc["verdict_channel"]).strip()
    if channel not in CHANNELS:
        errs.append(f"verdict_channel {channel!r} not in {sorted(CHANNELS)}")
    if len(str(gfc["gate"]).strip()) < 3:
        errs.append("gate must name the gate as an operator would say it")
    if len(str(gfc["invocation"]).strip()) < 5:
        errs.append("invocation must be the exact command a runner executes (r5-configured-is-not-invoked)")

    # findings-shaped gates need a blocking severity to emit the synthetic finding at (r3).
    blocking = str(gfc.get("blocking_severity", "")).strip().lower()
    if channel in ("findings", "both"):
        if not blocking:
            errs.append("verdict_channel includes findings so blocking_severity is required (r3-synthetic-finding-not-exception)")
        elif _sev_rank(blocking) < 0:
            errs.append(f"blocking_severity {blocking!r} not in {SEVERITIES}")

    # r2 — every non-evaluating mode mandatory for this instrument, exactly once.
    modes = gfc["failure_modes"]
    seen: list[str] = []
    if not isinstance(modes, list) or not modes:
        errs.append("failure_modes must be a non-empty list (r2-name-the-non-evaluating-modes)")
        modes = []
    for i, entry in enumerate(modes):
        if not isinstance(entry, dict) or "mode" not in entry:
            errs.append(f"failure_modes[{i}] must be a mapping with a mode")
            continue
        mode = str(entry["mode"]).strip().lower()
        seen.append(mode)
        if mode not in KNOWN_MODES:
            errs.append(f"failure_modes[{i}]: unknown mode {mode!r}, expected one of {sorted(KNOWN_MODES)}")
        if not str(entry.get("detect", "")).strip():
            errs.append(f"mode {mode!r} has no detect: name the observable (r2-name-the-non-evaluating-modes)")
        emits = str(entry.get("emits", "")).strip().lower()
        if emits in FORBIDDEN_EMITS:
            errs.append(
                f"mode {mode!r} emits {emits!r}: a gate that cannot evaluate must not report pass "
                "(r1-cannot-evaluate-is-not-pass)"
            )
        sev = str(entry.get("severity", "")).strip().lower()
        if channel in ("findings", "both"):
            if _sev_rank(sev) < 0:
                errs.append(f"mode {mode!r} has no valid severity, expected one of {SEVERITIES}")
            elif blocking and _sev_rank(blocking) >= 0 and _sev_rank(sev) < _sev_rank(blocking):
                errs.append(
                    f"mode {mode!r} emits severity {sev!r} below blocking_severity {blocking!r}: "
                    "the synthetic finding would not trip the gate (r3-synthetic-finding-not-exception)"
                )

    for dup in sorted({m for m in seen if seen.count(m) > 1}):
        errs.append(f"mode {dup!r} declared more than once")
    for missing in sorted(MANDATORY_MODES.get(instrument, set()) - set(seen)):
        errs.append(f"instrument {instrument!r} requires mode {missing!r} (r2-name-the-non-evaluating-modes)")

    # r1 — the audited-out paths, quoted, so a reviewer can grep for their return.
    paths = gfc["forbidden_paths"]
    if not isinstance(paths, list) or not paths:
        errs.append("forbidden_paths must list the audited-out pass paths (r1-cannot-evaluate-is-not-pass)")

    # r6 — the hatch is named, logged and dated, or it does not exist.
    override = gfc["degraded_override"]
    if not isinstance(override, dict) or "allowed" not in override:
        errs.append("degraded_override must be a mapping with an allowed key (r6-override-is-explicit-logged-and-expiring)")
    elif override.get("allowed") is True:
        if not str(override.get("flag", "")).strip():
            errs.append("degraded_override.allowed is true but no flag is named (r6-override-is-explicit-logged-and-expiring)")
        if override.get("logged") is not True:
            errs.append("degraded_override.allowed is true but logged is not true (r6-override-is-explicit-logged-and-expiring)")
        expires = _parse_date(override.get("expires"))
        if expires is None:
            errs.append("degraded_override.allowed is true but expires is not an ISO date (r6-override-is-explicit-logged-and-expiring)")

    # r4 — fail-closed is demonstrated, not asserted.
    if len(str(gfc["fault_injection_proof"]).strip()) < 15:
        errs.append(
            "fault_injection_proof must name the command that breaks the gate on purpose and the exit code "
            "it must then produce (r4-exit-status-must-survive-the-pipeline)"
        )
    proved = _parse_date(gfc["last_proved"])
    if proved is None:
        errs.append("last_proved must be an ISO date (r4-exit-status-must-survive-the-pipeline)")
    else:
        expires = _parse_date(override.get("expires")) if isinstance(override, dict) else None
        if expires is not None and expires < proved:
            errs.append(
                f"degraded_override.expires ({expires}) is before last_proved ({proved}): "
                "the hatch expired before the gate was last proved (r6-override-is-explicit-logged-and-expiring)"
            )

    return errs


def load(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            print("PyYAML required for YAML contracts; install pyyaml or pass JSON", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(raw)
    return json.loads(raw)


def _judge_ok() -> dict:
    return {
        "gate": "uk prose judge",
        "instrument": "judge",
        "invocation": "python3 scripts/llm-judge.py content/uk.mdx --rubric rubrics/uk-quality.yaml --max-high 0",
        "verdict_channel": "both",
        "blocking_severity": "high",
        "failure_modes": [
            {"mode": "parse", "detect": "json.JSONDecodeError on the reply", "emits": "judge-parse-failure", "severity": "high"},
            {"mode": "refusal", "detect": "reply has no '[' and matches a refusal phrase set", "emits": "judge-refusal", "severity": "high"},
            {"mode": "truncation", "detect": "stop_reason == 'max_tokens'", "emits": "judge-truncated", "severity": "high"},
            {"mode": "transport", "detect": "non-2xx, timeout or connection reset after retries", "emits": "judge-unreachable", "severity": "critical"},
            {"mode": "empty", "detect": "schema-valid reply with zero verdict entries", "emits": "judge-empty-verdict", "severity": "high"},
        ],
        "forbidden_paths": ["llm-judge.py:175 `except json.JSONDecodeError: return []`"],
        "degraded_override": {"allowed": True, "flag": "--allow-degraded", "expires": "2026-11-01", "logged": True},
        "fault_injection_proof": "FAION_JUDGE_FORCE=parse-error make judge -> expect exit 1 and one high finding",
        "last_proved": "2026-08-04",
    }


def _static_ok() -> dict:
    return {
        "gate": "corpus validator sweep",
        "instrument": "static",
        "invocation": "bash scripts/f066-validate-all.sh",
        "verdict_channel": "exit_code",
        "failure_modes": [
            {"mode": "crash", "detect": "any sub-validator exits >1 or is killed", "emits": "exit:2", "severity": "high"},
            {"mode": "absent_input", "detect": "target directory or meta.json missing", "emits": "exit:2", "severity": "high"},
        ],
        "forbidden_paths": ["f066-validate-all.sh: run() discards ${PIPESTATUS[0]}; script ends on echo"],
        "degraded_override": {"allowed": False},
        "fault_injection_proof": "corrupt one meta.json, run the sweep -> expect exit 1",
        "last_proved": "2026-08-04",
    }


def self_test() -> int:
    ok_judge = _judge_ok()
    ok_static = _static_ok()

    missing_empty = _judge_ok()
    missing_empty["failure_modes"] = [m for m in missing_empty["failure_modes"] if m["mode"] != "empty"]

    emits_pass = _judge_ok()
    emits_pass["failure_modes"][0]["emits"] = "pass"

    low_sev = _judge_ok()
    low_sev["failure_modes"][0]["severity"] = "medium"

    open_hatch = _judge_ok()
    open_hatch["degraded_override"] = {"allowed": True, "flag": "--allow-degraded", "logged": True}

    no_proof = _static_ok()
    no_proof["fault_injection_proof"] = "todo"

    cases = [
        ("judge gate, all five modes closed", ok_judge, 0),
        ("static gate, crash + absent input", ok_static, 0),
        ("schema-valid-but-empty mode omitted", missing_empty, 1),
        ("mode emits pass", emits_pass, 1),
        ("synthetic finding below blocking severity", low_sev, 1),
        ("override with no expiry", open_hatch, 1),
        ("fault injection proof not stated", no_proof, 1),
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
