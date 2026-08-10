#!/usr/bin/env python3
"""Validate a Context Budget Record against the context-file-cost-budget contract.

Enforces the auto-generation stop (r1), per-line human confirmation (r2), the
line ceiling and its arithmetic (r3), the overview ban (r4), named relocation
targets (r5), preference marking (r6) and the five-run measurement protocol (r7).

Usage:
  validate-context-file-cost-budget.py <context-budget-record.yaml|.json>
  validate-context-file-cost-budget.py --self-test
  validate-context-file-cost-budget.py --help

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

AUTHORS = {"human", "llm", "mixed"}
KINDS = {"instruction", "overview", "preference"}
DECISIONS = {"keep", "cut", "relocate"}
VERDICTS = {"keep", "cut", "relocate", "delete"}

BASE_KEYS = ("file", "authored_by", "current_lines", "ceiling", "blocks",
             "kept_lines", "verdict", "verdict_rationale")
MEASUREMENT_KEYS = ("runs", "cost_usd_baseline", "cost_usd_after",
                    "success_baseline", "success_after")

DEFAULT_CEILING = 200
MIN_RUNS = 5
RANGE_RE = re.compile(r"^(\d+)\s*-\s*(\d+)$")


def _span(spec: object) -> int | None:
    """Line count of a 'A-B' range, or of a single line number."""
    text = str(spec).strip()
    m = RANGE_RE.match(text)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        return hi - lo + 1 if hi >= lo else None
    return 1 if text.isdigit() else None


def violations(rec: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(rec, dict):
        return ["record root must be a mapping"]

    for key in BASE_KEYS:
        if key not in rec:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    author = str(rec["authored_by"]).strip()
    if author not in AUTHORS:
        errs.append(f"authored_by {author!r} not in {sorted(AUTHORS)}")
    verdict = str(rec["verdict"]).strip()
    if verdict not in VERDICTS:
        errs.append(f"verdict {verdict!r} not in {sorted(VERDICTS)}")
    if len(str(rec["verdict_rationale"]).strip()) < 30:
        errs.append("verdict_rationale must be >=30 chars referencing the deltas (r7-five-run-median-before-claiming)")

    blocks = rec["blocks"]
    if not isinstance(blocks, list) or not blocks:
        errs.append("blocks must be a non-empty classification of the whole file (r4-instructions-in-overviews-out)")
        return errs

    kept_span = 0
    confirmed_keeps = 0
    for i, b in enumerate(blocks):
        if not isinstance(b, dict):
            errs.append(f"blocks[{i}] must be a mapping")
            continue
        kind = str(b.get("kind") or "").strip()
        decision = str(b.get("decision") or "").strip()
        if kind not in KINDS:
            errs.append(f"blocks[{i}].kind must be one of {sorted(KINDS)} (r4-instructions-in-overviews-out)")
        if decision not in DECISIONS:
            errs.append(f"blocks[{i}].decision must be one of {sorted(DECISIONS)}")
        span = _span(b.get("lines"))
        if span is None:
            errs.append(f"blocks[{i}].lines must be a line range like '12-30' (r2-stub-confirmed-line-by-line)")

        # r4 — an overview may never be kept.
        if kind == "overview" and decision == "keep":
            errs.append(
                f"blocks[{i}] is an overview kept in the always-loaded file; cut it or "
                "relocate it (r4-instructions-in-overviews-out)"
            )
        # r5 — a relocation must name where to.
        if decision == "relocate" and not str(b.get("relocate_to") or "").strip():
            errs.append(f"blocks[{i}] relocates but names no relocate_to path (r5-path-scoped-relocation)")
        if decision == "keep":
            if span:
                kept_span += span
            # r2 — nothing ships unconfirmed.
            if b.get("confirmed_by_human") is not True:
                errs.append(
                    f"blocks[{i}] is kept without confirmed_by_human: true; unconfirmed "
                    "lines do not ship (r2-stub-confirmed-line-by-line)"
                )
            else:
                confirmed_keeps += 1
            # r6 — a kept preference must say it is one.
            if kind == "preference" and b.get("marked_as_preference") is not True:
                errs.append(
                    f"blocks[{i}] keeps a preference without marked_as_preference: true; "
                    "unmarked soft guidance is enforced as law (r6-preferences-marked-or-cut)"
                )

    # r1 — the stop condition: machine-written and unconfirmed resolves to delete.
    if author == "llm" and confirmed_keeps == 0:
        if verdict != "delete":
            errs.append(
                "authored_by 'llm' with no human-confirmed block must resolve to "
                "verdict 'delete' (r1-never-auto-generate)"
            )
        leaked = [k for k in MEASUREMENT_KEYS if k in rec]
        if leaked:
            errs.append(
                "the delete branch stops before measurement; remove: "
                + ", ".join(sorted(leaked))
                + " (r1-never-auto-generate)"
            )
        return errs

    # r3 — the ceiling and its arithmetic.
    ceiling = int(rec["ceiling"])
    if ceiling > DEFAULT_CEILING and not str(rec.get("ceiling_justification") or "").strip():
        errs.append(
            f"ceiling {ceiling} exceeds the default {DEFAULT_CEILING} with no "
            "ceiling_justification (r3-declared-line-ceiling)"
        )
    kept = int(rec["kept_lines"])
    if kept != kept_span:
        errs.append(
            f"kept_lines is {kept} but the kept blocks span {kept_span} lines "
            "(r3-declared-line-ceiling)"
        )
    if kept > ceiling:
        errs.append(
            f"kept_lines {kept} exceeds ceiling {ceiling}: relocate or cut further, "
            "do not raise the ceiling (r3-declared-line-ceiling)"
        )

    # r7 — the measurement protocol.
    for key in MEASUREMENT_KEYS:
        if key not in rec:
            errs.append(f"missing required measurement key: {key} (r7-five-run-median-before-claiming)")
    if errs:
        return errs

    runs = int(rec["runs"])
    if runs < MIN_RUNS:
        errs.append(
            f"runs is {runs}; at least {MIN_RUNS} per arm are required before any claim "
            "(r7-five-run-median-before-claiming)"
        )
    cost_before = float(rec["cost_usd_baseline"])
    cost_after = float(rec["cost_usd_after"])
    succ_before = float(rec["success_baseline"])
    succ_after = float(rec["success_after"])

    if cost_after > cost_before and not str(rec.get("cost_accepted_because") or "").strip():
        errs.append(
            f"cost rose from {cost_before} to {cost_usd(cost_after)} per run with no "
            "cost_accepted_because (r7-five-run-median-before-claiming)"
        )
    if succ_after <= succ_before and cost_after > cost_before and verdict == "keep":
        errs.append(
            "the file costs more per run and returns no measured success gain, so "
            "'keep' is not available; cut or delete (r7-five-run-median-before-claiming)"
        )
    return errs


def cost_usd(v: float) -> str:
    return f"{v:.2f}"


def load(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            print("PyYAML required for YAML records; install pyyaml or pass JSON", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(raw)
    return json.loads(raw)


def _ok_full() -> dict:
    return {
        "file": "AGENTS.md",
        "authored_by": "mixed",
        "current_lines": 318,
        "ceiling": 200,
        "blocks": [
            {"lines": "1-14", "kind": "instruction", "decision": "keep", "confirmed_by_human": True},
            {"lines": "15-96", "kind": "overview", "decision": "cut"},
            {"lines": "97-140", "kind": "overview", "decision": "relocate",
             "relocate_to": "docs/architecture.md"},
            {"lines": "141-188", "kind": "instruction", "decision": "keep", "confirmed_by_human": True},
            {"lines": "189-244", "kind": "instruction", "decision": "relocate",
             "relocate_to": ".claude/rules/frontend.md"},
            {"lines": "245-286", "kind": "preference", "decision": "keep",
             "confirmed_by_human": True, "marked_as_preference": True},
            {"lines": "287-318", "kind": "overview", "decision": "cut"},
        ],
        "kept_lines": 104,
        "runs": 5,
        "cost_usd_baseline": 0.94,
        "cost_usd_after": 1.07,
        "cost_accepted_because": "13 cents per run buys a measured 5-point success gain on the same task set",
        "success_baseline": 0.61,
        "success_after": 0.66,
        "verdict": "cut",
        "verdict_rationale": "318 lines to 104; overviews cut, frontend rules scoped, success 61% to 66%.",
    }


def _ok_delete() -> dict:
    return {
        "file": "packages/ingest/AGENTS.md",
        "authored_by": "llm",
        "current_lines": 212,
        "ceiling": 200,
        "blocks": [{"lines": "1-212", "kind": "overview", "decision": "cut"}],
        "kept_lines": 0,
        "verdict": "delete",
        "verdict_rationale": "Bootstrap-generated 2026-07-11, never read, pure module summary. Deleted, not audited.",
    }


def self_test() -> int:
    delete_measured = dict(_ok_delete(), runs=5, cost_usd_baseline=0.9, cost_usd_after=1.1,
                           success_baseline=0.6, success_after=0.6)
    delete_kept = dict(_ok_delete(), verdict="keep")

    kept_overview = _ok_full()
    kept_overview["blocks"] = list(kept_overview["blocks"])
    kept_overview["blocks"][1] = {"lines": "15-96", "kind": "overview", "decision": "keep",
                                  "confirmed_by_human": True}
    kept_overview["kept_lines"] = 186

    unconfirmed = _ok_full()
    unconfirmed["blocks"] = list(unconfirmed["blocks"])
    unconfirmed["blocks"][0] = {"lines": "1-14", "kind": "instruction", "decision": "keep"}

    bad_math = dict(_ok_full(), kept_lines=90)
    over_ceiling = dict(_ok_full(), ceiling=60)
    one_run = dict(_ok_full(), runs=1)
    no_relocate_target = _ok_full()
    no_relocate_target["blocks"] = list(no_relocate_target["blocks"])
    no_relocate_target["blocks"][2] = {"lines": "97-140", "kind": "overview", "decision": "relocate"}

    unmarked_pref = _ok_full()
    unmarked_pref["blocks"] = list(unmarked_pref["blocks"])
    unmarked_pref["blocks"][5] = {"lines": "245-286", "kind": "preference", "decision": "keep",
                                  "confirmed_by_human": True}

    keep_without_gain = dict(_ok_full(), verdict="keep", success_after=0.61)
    raised_ceiling = dict(_ok_full(), ceiling=400)
    unexplained_cost = _ok_full()
    unexplained_cost.pop("cost_accepted_because")

    cases = [
        ("full valid cut record", _ok_full(), 0),
        ("llm-generated unconfirmed -> delete", _ok_delete(), 0),
        ("delete branch leaked measurement keys", delete_measured, 1),
        ("llm-generated unconfirmed kept anyway", delete_kept, 1),
        ("overview block kept", kept_overview, 1),
        ("kept block without human confirmation", unconfirmed, 1),
        ("kept_lines arithmetic wrong", bad_math, 1),
        ("kept_lines over ceiling", over_ceiling, 1),
        ("single run per arm", one_run, 1),
        ("relocate without destination", no_relocate_target, 1),
        ("kept preference not marked as one", unmarked_pref, 1),
        ("keep on cost rise with no success gain", keep_without_gain, 1),
        ("ceiling raised without justification", raised_ceiling, 1),
        ("cost rise with no acceptance stated", unexplained_cost, 1),
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
