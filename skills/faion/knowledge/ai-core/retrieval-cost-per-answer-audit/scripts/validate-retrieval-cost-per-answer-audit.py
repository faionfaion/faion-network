#!/usr/bin/env python3
"""Validate a Retrieval Cost Ledger against the retrieval-cost-per-answer-audit contract.

The validator does not trust the summary block: it recomputes every derived
number from the rows and fails the ledger on mismatch (02-output-contract.xml).

Rounding conventions, used identically here and in the template:
  median  — middle value; mean of the two middle values for an even count,
            then rounded half-up to an integer.
  p90     — nearest-rank: the value at index ceil(0.9 * n) - 1 of the sorted list.
  ratio   — median of the per-row (index + candidate) / body ratios, 1 decimal.

Usage:
  validate-retrieval-cost-per-answer-audit.py <ledger.yaml|ledger.json>
  validate-retrieval-cost-per-answer-audit.py --self-test
  validate-retrieval-cost-per-answer-audit.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

STRUCTURES = {"flat", "tree", "graph", "hybrid"}
SHAPES = {"fact", "multi_hop"}
VERDICTS = {"leave_alone", "compress", "restructure"}
MIN_ROWS = 10
LEAVE_ALONE_RATIO_CEILING = 5.0

REQUIRED_KEYS = (
    "system",
    "structure",
    "measured_on",
    "model",
    "sampling",
    "queries",
    "median_tokens_per_lookup",
    "p90_tokens_per_lookup",
    "p90_query_id",
    "overhead_ratio",
    "tokens_per_correct_answer",
    "index_build_tokens",
    "corpus_change_frequency",
    "verdict",
)
ROW_INT_FIELDS = ("index_tokens", "candidate_tokens", "body_tokens")


def round_half_up(value: float) -> int:
    return int(math.floor(value + 0.5))


def median(values: list[float]) -> float:
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def p90(values: list[int]) -> int:
    ordered = sorted(values)
    rank = math.ceil(0.9 * len(ordered)) - 1
    return ordered[rank]


def violations(led: dict) -> list[str]:
    errs: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in led:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    if len(str(led["system"]).strip()) < 12:
        errs.append("system must describe what is retrieved over (>=12 chars)")
    if led["structure"] not in STRUCTURES:
        errs.append(f"structure must be one of {sorted(STRUCTURES)}")
    if len(str(led["sampling"]).strip()) < 20:
        errs.append("sampling must state how queries were drawn from real traffic (r2-ten-real-queries)")
    if led["verdict"] not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    if int(led["index_build_tokens"]) < 0:
        errs.append("index_build_tokens must be >= 0 (use 0 when there is no build step)")

    rows = led["queries"]
    if not isinstance(rows, list):
        errs.append("queries must be a list of ledger rows")
        return errs

    real: list[dict] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errs.append(f"queries[{i}] must be a mapping")
            continue
        if not row.get("id"):
            errs.append(f"queries[{i}] has no id")
        shape = row.get("shape")
        if shape not in SHAPES:
            errs.append(f"queries[{i}] shape must be one of {sorted(SHAPES)} (r2-ten-real-queries)")
        bad_field = False
        for f in ROW_INT_FIELDS:
            v = row.get(f)
            if not isinstance(v, int) or isinstance(v, bool) or v < 0:
                errs.append(f"queries[{i}].{f} must be a non-negative integer (r3-four-columns-not-one-total)")
                bad_field = True
        if not bad_field and row["body_tokens"] <= 0:
            errs.append(
                f"queries[{i}].body_tokens is 0: a lookup that delivered nothing is a retrieval "
                "failure, not a cost measurement (r3-four-columns-not-one-total)"
            )
            bad_field = True
        if not isinstance(row.get("correct"), bool):
            errs.append(f"queries[{i}].correct must be a boolean (r3-four-columns-not-one-total)")
            bad_field = True
        if not bad_field and not row.get("synthetic"):
            real.append(row)

    if errs:
        return errs

    if len(real) < MIN_ROWS:
        errs.append(
            f"ledger has {len(real)} non-synthetic rows, needs >= {MIN_ROWS} (r2-ten-real-queries)"
        )
        return errs
    shapes = {r["shape"] for r in real}
    for missing in sorted(SHAPES - shapes):
        errs.append(f"no row with shape {missing!r}; the mix must span both (r2-ten-real-queries)")

    ids = [r["id"] for r in real]
    if len(set(ids)) != len(ids):
        errs.append("query ids must be unique")
    if led["p90_query_id"] not in ids:
        errs.append(
            f"p90_query_id {led['p90_query_id']!r} does not resolve to a non-synthetic row "
            "(r4-median-and-p90-never-mean)"
        )

    totals = [r["index_tokens"] + r["candidate_tokens"] + r["body_tokens"] for r in real]
    ratios = [(r["index_tokens"] + r["candidate_tokens"]) / r["body_tokens"] for r in real]

    want_median = round_half_up(median([float(t) for t in totals]))
    if int(led["median_tokens_per_lookup"]) != want_median:
        errs.append(
            f"median_tokens_per_lookup states {led['median_tokens_per_lookup']} but the rows give "
            f"{want_median} (r5-overhead-ratio-decides)"
        )

    want_p90 = p90(totals)
    if int(led["p90_tokens_per_lookup"]) != want_p90:
        errs.append(
            f"p90_tokens_per_lookup states {led['p90_tokens_per_lookup']} but the rows give "
            f"{want_p90} (r4-median-and-p90-never-mean)"
        )
    p90_row = next((r for r in real if r["id"] == led["p90_query_id"]), None)
    if p90_row is not None:
        got = p90_row["index_tokens"] + p90_row["candidate_tokens"] + p90_row["body_tokens"]
        if got != want_p90:
            errs.append(
                f"p90_query_id points at a row totalling {got}, not the p90 value {want_p90} "
                "(r4-median-and-p90-never-mean)"
            )

    want_ratio = round(median(ratios), 1)
    if abs(float(led["overhead_ratio"]) - want_ratio) > 0.05:
        errs.append(
            f"overhead_ratio states {led['overhead_ratio']} but the rows give {want_ratio} "
            "(r5-overhead-ratio-decides)"
        )

    n_correct = sum(1 for r in real if r["correct"])
    if n_correct == 0:
        errs.append("no row is correct: this is an eval failure, not a cost ledger (r3-four-columns-not-one-total)")
    else:
        want_tpca = round_half_up(sum(totals) / n_correct)
        if int(led["tokens_per_correct_answer"]) != want_tpca:
            errs.append(
                f"tokens_per_correct_answer states {led['tokens_per_correct_answer']} but the rows "
                f"give {want_tpca} (r3-four-columns-not-one-total)"
            )

    # The verdict must be consistent with the number that produced it.
    if float(led["overhead_ratio"]) >= LEAVE_ALONE_RATIO_CEILING and led["verdict"] == "leave_alone":
        errs.append(
            f"overhead_ratio {led['overhead_ratio']} >= {LEAVE_ALONE_RATIO_CEILING} cannot record "
            "verdict 'leave_alone' (06-decision-tree)"
        )

    return errs


def load(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            print("PyYAML required for YAML ledgers; install pyyaml or pass JSON", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(raw)
    return json.loads(raw)


def _rows() -> list[dict]:
    """Ten rows mirroring the shipped template."""
    spec = [
        ("q01", "fact", 30000, 2400, 3200, True),
        ("q02", "fact", 28000, 1800, 2600, True),
        ("q03", "multi_hop", 44000, 9000, 6100, True),
        ("q04", "fact", 12000, 1500, 1400, True),
        ("q05", "multi_hop", 44000, 11000, 7400, False),
        ("q06", "fact", 18000, 2100, 2000, True),
        ("q07", "fact", 28000, 2000, 3400, True),
        ("q08", "multi_hop", 36000, 6400, 5200, True),
        ("q09", "fact", 12000, 1200, 1150, False),
        ("q10", "fact", 18000, 1700, 1800, True),
    ]
    return [
        {
            "id": i,
            "text": f"real query {i}",
            "shape": s,
            "index_tokens": ix,
            "candidate_tokens": ca,
            "body_tokens": bo,
            "correct": ok,
        }
        for i, s, ix, ca, bo, ok in spec
    ]


def _ledger(**over: object) -> dict:
    rows = _rows()
    totals = [r["index_tokens"] + r["candidate_tokens"] + r["body_tokens"] for r in rows]
    ratios = [(r["index_tokens"] + r["candidate_tokens"]) / r["body_tokens"] for r in rows]
    base = {
        "system": "methodology retrieval over a 2600-document corpus",
        "structure": "tree",
        "measured_on": "2026-08-04",
        "model": "claude-opus, provider usage field",
        "sampling": "ten consecutive real lookups from the orchestrator task log",
        "queries": rows,
        "median_tokens_per_lookup": round_half_up(median([float(t) for t in totals])),
        "p90_tokens_per_lookup": p90(totals),
        "p90_query_id": next(r["id"] for r in rows if sum(
            (r["index_tokens"], r["candidate_tokens"], r["body_tokens"])) == p90(totals)),
        "overhead_ratio": round(median(ratios), 1),
        "tokens_per_correct_answer": round_half_up(sum(totals) / sum(1 for r in rows if r["correct"])),
        "index_build_tokens": 0,
        "corpus_change_frequency": "per merge to main",
        "verdict": "compress",
    }
    base.update(over)
    return base


def self_test() -> int:
    ok = _ledger()

    short = _ledger()
    short["queries"] = short["queries"][:6]

    wrong_median = _ledger(median_tokens_per_lookup=1234)
    wrong_ratio = _ledger(overhead_ratio=1.0)
    bad_verdict = _ledger(verdict="leave_alone")

    empty_body = _ledger()
    empty_body["queries"] = [dict(r) for r in empty_body["queries"]]
    empty_body["queries"][0]["body_tokens"] = 0

    one_shape = _ledger()
    one_shape["queries"] = [dict(r, shape="fact") for r in one_shape["queries"]]

    bad_p90 = _ledger(p90_query_id="q01")

    cases = [
        ("valid ledger, verdict compress", ok, 0),
        ("fewer than ten real rows", short, 1),
        ("stated median disagrees with rows", wrong_median, 1),
        ("stated overhead_ratio disagrees with rows", wrong_ratio, 1),
        ("high overhead but verdict leave_alone", bad_verdict, 1),
        ("row delivered zero body tokens", empty_body, 1),
        ("query mix missing multi_hop", one_shape, 1),
        ("p90_query_id names the wrong row", bad_p90, 1),
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
