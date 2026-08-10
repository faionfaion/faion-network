#!/usr/bin/env python3
"""Validate a Rung Placement Record against the verification-rung-placement-rule contract.

Usage:
  validate-verification-rung-placement-rule.py <rpr.yaml|rpr.json>
  validate-verification-rung-placement-rule.py --self-test
  validate-verification-rung-placement-rule.py --help

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

# Q1/Q2/Q3 answer -> the rung it forces (r1-cheapest-instrument-first).
ANSWER_TO_RUNG = {"bytes": "1", "mechanical": "2", "judgement": "3", "none": "H"}
RUNGS = {"1", "2", "3", "H"}
ACTIONS = {"block", "flag"}
CADENCES = {"pre-commit", "ci", "nightly", "on-change", "pre-release", "on-demand"}

RUNG3_HARD_CAP = 15
# Below this share of rung-1 checks, a record of non-trivial size is inflated.
RUNG1_MIN_SHARE = 0.5
MIX_APPLIES_FROM = 8


def _rung(check: dict) -> str:
    """Normalise the rung value; YAML may give int 1 or string '1'/'h'/'H'."""
    raw = str(check.get("rung", "")).strip()
    return "H" if raw.lower() == "h" else raw


def violations(rpr: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(rpr, dict):
        return ["record root must be a mapping"]

    for key in ("system", "rung3_budget", "checks"):
        if key not in rpr:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    if len(str(rpr["system"]).strip()) < 8:
        errs.append("system must say what is being verified in one line")

    try:
        budget = int(rpr["rung3_budget"])
    except (TypeError, ValueError):
        errs.append("rung3_budget must be an integer")
        budget = RUNG3_HARD_CAP
    if budget > RUNG3_HARD_CAP:
        errs.append(
            f"rung3_budget {budget} exceeds the hard cap of {RUNG3_HARD_CAP}: beyond that you have a slow "
            "rung-2 suite with a random number generator in it (r4-rung-3-is-pairwise-and-budgeted)"
        )
    if budget < 0:
        errs.append("rung3_budget must be >= 0")

    checks = rpr["checks"]
    if not isinstance(checks, list) or not checks:
        return errs + ["checks must be a non-empty list"]

    seen_ids: list[str] = []
    counts = {"1": 0, "2": 0, "3": 0, "H": 0}
    has_h = False

    for i, c in enumerate(checks):
        if not isinstance(c, dict) or not str(c.get("id", "")).strip():
            errs.append(f"checks[{i}] must be a mapping with an id")
            continue
        cid = str(c["id"]).strip()
        seen_ids.append(cid)

        if len(str(c.get("defect", "")).strip()) < 15:
            errs.append(f"{cid}: defect must describe the observable defect, not the check")
        if len(str(c.get("instrument", "")).strip()) < 4:
            errs.append(f"{cid}: instrument must name the concrete validator, case, scenario or reviewer")

        answer = str(c.get("answers", "")).strip().lower()
        if answer not in ANSWER_TO_RUNG:
            errs.append(f"{cid}: answers must be one of {sorted(ANSWER_TO_RUNG)} (r1-cheapest-instrument-first)")
            continue
        rung = _rung(c)
        if rung not in RUNGS:
            errs.append(f"{cid}: rung must be one of {sorted(RUNGS)}")
            continue
        expected = ANSWER_TO_RUNG[answer]
        if rung != expected:
            errs.append(
                f"{cid}: answers={answer!r} forces rung {expected} but rung is {rung} "
                "(r1-cheapest-instrument-first)"
            )
            continue
        counts[rung] += 1

        # r2 — anything above rung 1 justifies itself against the rung below.
        if rung != "1":
            reason = str(c.get("cannot_live_below", "")).strip()
            if len(reason) < 20:
                errs.append(
                    f"{cid}: rung {rung} requires cannot_live_below — state in one line why the rung below "
                    "cannot decide this (r2-cannot-live-on-the-rung-below)"
                )
            elif "easier to write" in reason.lower():
                errs.append(
                    f"{cid}: 'easier to write' is not a reason — a model is never easier to maintain "
                    "(r2-cannot-live-on-the-rung-below)"
                )

        # r3 — exact rules may block, heuristics may only flag.
        if rung == "1":
            if "exact" not in c:
                errs.append(f"{cid}: rung 1 must declare exact: true|false (r3-exact-rules-block-heuristics-flag)")
            action = str(c.get("action", "")).strip().lower()
            if action not in ACTIONS:
                errs.append(f"{cid}: rung 1 must declare action: block|flag (r3-exact-rules-block-heuristics-flag)")
            elif c.get("exact") is False and action != "flag":
                errs.append(
                    f"{cid}: exact is false so action must be flag — a heuristic that blocks trains the "
                    "operator to bypass the gate (r3-exact-rules-block-heuristics-flag)"
                )

        # r4 — rung 3 is pairwise or it is not a rung-3 check.
        if rung == "3" and c.get("pairwise") is not True:
            errs.append(
                f"{cid}: rung 3 requires pairwise: true — an absolute judge score at kappa 0.549 is not a gate "
                "(r4-rung-3-is-pairwise-and-budgeted)"
            )

        if rung == "H":
            has_h = True

        # r6 — cadence follows rung.
        cadence = str(c.get("cadence", "")).strip().lower()
        if cadence not in CADENCES:
            errs.append(f"{cid}: cadence must be one of {sorted(CADENCES)} (r6-cadence-follows-rung)")
        elif cadence == "pre-commit" and rung in ("2", "3"):
            errs.append(
                f"{cid}: rung {rung} must not run in a pre-commit hook — it costs money and minutes per commit "
                "and gets disabled within a week (r6-cadence-follows-rung)"
            )

    for dup in sorted({i for i in seen_ids if seen_ids.count(i) > 1}):
        errs.append(f"duplicate check id: {dup!r}")

    if counts["3"] > budget:
        errs.append(
            f"{counts['3']} rung-3 checks exceed the declared rung3_budget of {budget} "
            "(r4-rung-3-is-pairwise-and-budgeted)"
        )

    # r5 — manual review must compound, not repeat.
    log = rpr.get("manual_review_log")
    if has_h:
        if not isinstance(log, list) or not log:
            errs.append(
                "a rung-H check exists so manual_review_log must be present and non-empty — log what was caught "
                "and which rung it was pushed down to (r5-rung-h-is-a-gate-but-not-deterministic)"
            )
        else:
            for j, entry in enumerate(log):
                if not isinstance(entry, dict) or not str(entry.get("found", "")).strip():
                    errs.append(f"manual_review_log[{j}] must record what was found")
                elif not str(entry.get("pushed_down_to", "")).strip():
                    errs.append(
                        f"manual_review_log[{j}] must record pushed_down_to — a check id, or 'accepted-risk' "
                        "with a reason (r5-rung-h-is-a-gate-but-not-deterministic)"
                    )

    # r2 mix check — rung inflation is visible in the counts once the record is non-trivial.
    total = sum(counts.values())
    if total >= MIX_APPLIES_FROM:
        share = counts["1"] / total
        if share < RUNG1_MIN_SHARE:
            errs.append(
                f"rung-1 checks are {counts['1']}/{total} ({share:.0%}) of the record; a healthy mix is nearer "
                "85% by count and anything under 50% is rung inflation (r2-cannot-live-on-the-rung-below)"
            )

    return errs


def load(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            print("PyYAML required for YAML records; install pyyaml or pass JSON", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(raw)
    return json.loads(raw)


def _base() -> dict:
    return {
        "system": "faion knowledge corpus and the search CLI over it",
        "rung3_budget": 5,
        "checks": [
            {
                "id": "refs-resolve",
                "defect": "a methodology_refs entry points at a slug that does not exist",
                "answers": "bytes",
                "rung": "1",
                "instrument": "scripts/validate-refs.py",
                "exact": True,
                "action": "block",
                "cadence": "pre-commit",
            },
            {
                "id": "description-length",
                "defect": "frontmatter description falls outside the 140-160 char window",
                "answers": "bytes",
                "rung": "1",
                "instrument": "scripts/check-structural.py",
                "exact": True,
                "action": "block",
                "cadence": "pre-commit",
            },
            {
                "id": "em-dash-density",
                "defect": "prose reads as machine-written because punctuation density is off",
                "answers": "bytes",
                "rung": "1",
                "instrument": "scripts/check-ai-tells.py",
                "exact": False,
                "action": "flag",
                "cadence": "ci",
            },
            {
                "id": "retrieval-recall",
                "defect": "a prompt edit drops the correct methodology out of the top 5",
                "answers": "mechanical",
                "rung": "2",
                "instrument": "evals/queries.yaml q001-q030",
                "cannot_live_below": "the ranking only exists after the real system runs; bytes cannot produce it",
                "cadence": "nightly",
            },
            {
                "id": "why-still-explanatory",
                "defect": "the why field degrades into tautology after a prompt refactor",
                "answers": "judgement",
                "rung": "3",
                "instrument": "champion-challenger scenario S1",
                "cannot_live_below": "no mechanical ground truth exists for whether an explanation explains",
                "pairwise": True,
                "cadence": "pre-release",
            },
            {
                "id": "new-domain-sanity",
                "defect": "a newly added domain reads as plausible but is subtly wrong on its own subject",
                "answers": "none",
                "rung": "H",
                "instrument": "operator read-through",
                "cannot_live_below": "nobody has enumerated what would be wrong, so no check can be written yet",
                "cadence": "on-demand",
            },
        ],
        "manual_review_log": [
            {"found": "phantom methodology slugs invented by writers", "pushed_down_to": "refs-resolve"},
        ],
    }


def self_test() -> int:
    ok = _base()

    # answers stays 'bytes' (Q1 said yes) while the rung claims 3 — the inflation case.
    inflated = _base()
    inflated["checks"][0]["rung"] = "3"

    unjustified = _base()
    del unjustified["checks"][3]["cannot_live_below"]

    heuristic_blocks = _base()
    heuristic_blocks["checks"][2]["action"] = "block"

    absolute_judge = _base()
    absolute_judge["checks"][4]["pairwise"] = False

    hook_too_expensive = _base()
    hook_too_expensive["checks"][3]["cadence"] = "pre-commit"

    no_log = _base()
    del no_log["manual_review_log"]

    over_budget = _base()
    over_budget["rung3_budget"] = 40

    cases = [
        ("well-placed record", ok, 0),
        ("bytes-decidable check placed on rung 3", inflated, 1),
        ("rung 2 with no reason the rung below fails", unjustified, 1),
        ("heuristic given blocking power", heuristic_blocks, 1),
        ("rung 3 scored absolutely", absolute_judge, 1),
        ("rung 2 wired into the pre-commit hook", hook_too_expensive, 1),
        ("rung H with no manual review log", no_log, 1),
        ("rung3_budget above the hard cap", over_budget, 1),
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
