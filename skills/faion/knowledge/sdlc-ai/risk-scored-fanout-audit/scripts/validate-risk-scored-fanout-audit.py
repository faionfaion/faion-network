#!/usr/bin/env python3
"""Validate a per-wave audit verdict set, and normalise agent field drift on read.

Input  : a JSON file shaped by content/02-output-contract.xml.
Output : one line per violation, or a single OK line.

Two jobs, both learned the hard way:

  1. Enforce the floors an agent cannot be trusted to enforce for itself — the
     evidence floor on adverse verdicts, no-auto-apply, suspects actually
     refuted, and counts that reconcile.
  2. Read the verdict field defensively. Only the value an agent returns through
     a tool boundary is schema-validated; the JSON the same agent WRITES to disk
     drifts (`judgment`, `decision`, `assessment`). Without normalisation those
     rows vanish from every tally with no error raised anywhere.

`--normalise` rewrites the file with canonical field names and exits 0 if the
result is otherwise valid; without it the script only reports.

Usage:
  validate-risk-scored-fanout-audit.py <wave.json> [--normalise] [--json]
  validate-risk-scored-fanout-audit.py --self-test
  validate-risk-scored-fanout-audit.py --help

Exit codes: 0 valid, 1 violations found, 2 usage or IO failure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VERDICTS = {"CONFIRMED", "INCORRECT", "WEAK", "AMBIGUOUS",
            "OUT_OF_SCOPE", "UNVERIFIABLE", "PARSE_ERROR"}
ADVERSE = {"INCORRECT", "WEAK", "OUT_OF_SCOPE"}
VERDICT_ALIASES = ("verdict", "judgment", "judgement", "decision", "assessment")
REQUIRED_TOP = ("wave", "corpus_total", "count", "applied", "by_verdict", "items")
EMPTY_EVIDENCE = {"", "none", "n/a", "null", "-"}
MIN_CALIBRATION_SAMPLE = 5
MIN_CALIBRATION_PRECISION = 0.8


def normalise_item(item: dict) -> tuple[dict, bool]:
    """Return (item with a canonical `verdict`, drifted?).

    r7: read `verdict || judgment || decision || assessment`, then fall back to
    an explicit PARSE_ERROR sentinel so a lost row is visible rather than absent.
    """
    out = dict(item)
    if isinstance(out.get("verdict"), str) and out["verdict"].strip():
        return out, False
    for alias in VERDICT_ALIASES[1:]:
        value = out.get(alias)
        if isinstance(value, str) and value.strip():
            out["verdict"] = value.strip().upper()
            return out, True
    out["verdict"] = "PARSE_ERROR"
    return out, True


def validate(report: object) -> tuple[list[str], dict]:
    """Return (violations, normalised report)."""
    out: list[str] = []
    if not isinstance(report, dict):
        return ["E000 report root must be a JSON object"], {}

    for key in REQUIRED_TOP:
        if key not in report:
            out.append("E001 missing required key: %s" % key)
    if out:
        return out, {}

    norm = dict(report)
    raw_items = report.get("items")
    if not isinstance(raw_items, list):
        return ["E002 items must be an array"], {}

    items: list[dict] = []
    drift = 0
    for idx, raw in enumerate(raw_items):
        if not isinstance(raw, dict):
            out.append("E002 items[%d] must be an object" % idx)
            continue
        item, drifted = normalise_item(raw)
        drift += 1 if drifted else 0
        items.append(item)
    norm["items"] = items
    norm["field_drift_fallbacks"] = drift

    declared_drift = report.get("field_drift_fallbacks")
    if isinstance(declared_drift, int) and declared_drift != drift:
        out.append("E107 field_drift_fallbacks says %d, found %d"
                   % (declared_drift, drift))

    # f2 — this artefact is a proposal set.
    if report.get("applied") is not False:
        out.append("E102 applied must be false; applying is a separate gated pass")

    seen: dict[str, int] = {}
    for idx, item in enumerate(items):
        where = "items[%d]" % idx
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            out.append("E002 %s missing id" % where)
            item_id = None
        verdict = item.get("verdict")
        evidence = item.get("evidence")
        suspect = item.get("suspect")

        if verdict not in VERDICTS:
            out.append("E002 %s verdict %r not in %s" % (where, verdict, sorted(VERDICTS)))
        if "suspect" not in item:
            out.append("E002 %s missing suspect" % where)
        if "evidence" not in item:
            out.append("E002 %s missing evidence" % where)

        # f6 — later passes override by id; a duplicate means the merge lost one.
        if item_id is not None:
            if item_id in seen:
                out.append("E106 duplicate id %r (also at items[%d])" % (item_id, seen[item_id]))
            else:
                seen[item_id] = idx

        # f1 — the evidence floor, applied as arithmetic and not as a prompt.
        if verdict in ADVERSE:
            text = evidence.strip().lower() if isinstance(evidence, str) else ""
            if text in EMPTY_EVIDENCE:
                out.append("E101 %s (%s) is adverse with no evidence — the aggregator "
                           "should have downgraded it to AMBIGUOUS" % (where, item_id))

        # f3 — every suspect must have been through the refute pass.
        if suspect is True and item.get("verified") is not True and "refuted_by" not in item:
            out.append("E103 %s (%s) is suspect but carries no refute result"
                       % (where, item_id))

        # f5 — a sentinel is a signal to re-run, not a tally line.
        if verdict == "PARSE_ERROR":
            out.append("E105 %s (%s) is PARSE_ERROR — the drift normaliser found no "
                       "usable verdict; re-read or re-run the slice" % (where, item_id))

        # An item that carries an application record contradicts f2.
        if "applied_at" in item:
            out.append("E102 %s records applied_at; this artefact applies nothing" % where)

    # f4 — every number is machine-computed or it is not trusted.
    count = report.get("count")
    if count != len(items):
        out.append("E104 count=%r but there are %d items" % (count, len(items)))
    by_verdict = report.get("by_verdict")
    if not isinstance(by_verdict, dict):
        out.append("E104 by_verdict must be an object")
    else:
        tally: dict[str, int] = {}
        for item in items:
            tally[item["verdict"]] = tally.get(item["verdict"], 0) + 1
        if {k: v for k, v in by_verdict.items() if v} != {k: v for k, v in tally.items() if v}:
            out.append("E104 by_verdict %s does not match the computed tally %s"
                       % (json.dumps(by_verdict, sort_keys=True), json.dumps(tally, sort_keys=True)))
        norm["by_verdict"] = tally
    corpus_total = report.get("corpus_total")
    if isinstance(corpus_total, int) and isinstance(count, int) and count > corpus_total:
        out.append("E104 count %d exceeds corpus_total %d" % (count, corpus_total))

    # f7 — calibration before a wave is called final.
    calib = report.get("calibration")
    if isinstance(calib, dict):
        sampled = calib.get("sampled")
        agreed = calib.get("agreed")
        if not isinstance(sampled, int) or not isinstance(agreed, int):
            out.append("E108 calibration.sampled and .agreed must be integers")
        elif sampled < MIN_CALIBRATION_SAMPLE:
            out.append("E108 calibration sample of %d is below the floor of %d"
                       % (sampled, MIN_CALIBRATION_SAMPLE))
        elif agreed / sampled < MIN_CALIBRATION_PRECISION:
            out.append("E108 calibration precision %.2f is below %.2f — tighten the "
                       "triage prompt and re-run this wave"
                       % (agreed / sampled, MIN_CALIBRATION_PRECISION))

    return out, norm


GOOD = {
    "wave": 1, "corpus_total": 1460, "count": 2, "applied": False,
    "field_drift_fallbacks": 0,
    "by_verdict": {"CONFIRMED": 1, "INCORRECT": 1},
    "calibration": {"sampled": 10, "agreed": 9},
    "items": [
        {"id": "it-0031", "verdict": "CONFIRMED", "suspect": False, "evidence": "src/a.md:'x'"},
        {"id": "it-0114", "verdict": "INCORRECT", "suspect": True, "verified": True,
         "refuted_by": 2, "evidence": "src/a.md:'y'", "issue": "contradicts source",
         "fix": "change to B"},
    ],
}


def self_test() -> int:
    failures = 0

    def expect(name: str, payload: object, codes: set[str]) -> None:
        nonlocal failures
        got = {v.split(" ", 1)[0] for v in validate(payload)[0]}
        if got != codes:
            failures += 1
            print("FAIL %s: expected %s, got %s" % (name, sorted(codes), sorted(got)))
        else:
            print("ok   %s" % name)

    expect("valid wave file", GOOD, set())

    drifted = json.loads(json.dumps(GOOD))
    del drifted["items"][0]["verdict"]
    drifted["items"][0]["judgment"] = "CONFIRMED"
    got_items = validate(drifted)[1]["items"]
    if got_items[0]["verdict"] != "CONFIRMED":
        failures += 1
        print("FAIL drift normaliser did not recover `judgment`")
    else:
        print("ok   drift normaliser recovers `judgment`")
    expect("drift is counted, not swallowed", drifted, {"E107"})

    no_evidence = json.loads(json.dumps(GOOD))
    no_evidence["items"][1]["evidence"] = "none"
    expect("adverse verdict with no evidence", no_evidence, {"E101"})

    unverifiable = json.loads(json.dumps(GOOD))
    unverifiable["items"][1]["verdict"] = "UNVERIFIABLE"
    unverifiable["items"][1]["evidence"] = "none"
    unverifiable["by_verdict"] = {"CONFIRMED": 1, "UNVERIFIABLE": 1}
    expect("UNVERIFIABLE may say evidence:none", unverifiable, set())

    applied = json.loads(json.dumps(GOOD))
    applied["applied"] = True
    expect("applied must be false", applied, {"E102"})

    unrefuted = json.loads(json.dumps(GOOD))
    del unrefuted["items"][1]["verified"]
    del unrefuted["items"][1]["refuted_by"]
    expect("suspect without a refute result", unrefuted, {"E103"})

    dupe = json.loads(json.dumps(GOOD))
    dupe["items"][1]["id"] = "it-0031"
    expect("duplicate id", dupe, {"E106"})

    miscount = json.loads(json.dumps(GOOD))
    miscount["count"] = 7
    expect("count does not reconcile", miscount, {"E104"})

    unusable = json.loads(json.dumps(GOOD))
    del unusable["items"][0]["verdict"]
    unusable["by_verdict"] = {"PARSE_ERROR": 1, "INCORRECT": 1}
    expect("PARSE_ERROR shipped", unusable, {"E105", "E107"})

    bad_calib = json.loads(json.dumps(GOOD))
    bad_calib["calibration"] = {"sampled": 10, "agreed": 5}
    expect("calibration below the precision floor", bad_calib, {"E108"})

    expect("root must be an object", [], {"E000"})

    print("self-test: %s" % ("PASS" if failures == 0 else "%d FAILED" % failures))
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate-risk-scored-fanout-audit.py",
        description="Validate a per-wave audit verdict set (content/02-output-contract.xml).",
    )
    parser.add_argument("wave", nargs="?", help="path to the wave verdict JSON file")
    parser.add_argument("--normalise", action="store_true",
                        help="rewrite the file with canonical field names")
    parser.add_argument("--self-test", action="store_true", help="replay the built-in fixtures")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    ns = parser.parse_args(argv)

    if ns.self_test:
        return self_test()
    if not ns.wave:
        parser.error("provide a wave file or --self-test")

    path = Path(ns.wave)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print("cannot read %s: %s" % (path, exc), file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print("invalid JSON in %s: %s" % (path, exc), file=sys.stderr)
        return 2

    violations, norm = validate(payload)
    if ns.normalise and norm:
        path.write_text(json.dumps(norm, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        violations, _ = validate(norm)

    if ns.json:
        print(json.dumps({"path": str(path), "ok": not violations,
                          "field_drift_fallbacks": norm.get("field_drift_fallbacks", 0),
                          "violations": violations}, indent=2))
    elif violations:
        print("FAIL %s" % path)
        for v in violations:
            print("  " + v)
    else:
        print("OK %s (field drift fallbacks: %d)"
              % (path, norm.get("field_drift_fallbacks", 0)))
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
