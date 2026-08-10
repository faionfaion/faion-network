#!/usr/bin/env python3
"""Validate a Closed-Set Validation Contract.

Checks the closedness claim, the enforcement policy, the metric set, the scope of
the metric over open fields, and the licence of any fallback groundedness scorer.

Usage:
  validate-closed-set-output-validation.py <contract.yaml|contract.json>
  validate-closed-set-output-validation.py --self-test
  validate-closed-set-output-validation.py --help

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

REQUIRED_KEYS = (
    "system",
    "closed_field",
    "candidate_set_source",
    "closedness_evidence",
    "selection_prompt_shape",
    "membership_check",
    "on_violation",
    "counter",
    "metrics",
    "open_fields",
)
PROMPT_SHAPES = {"set_in_request", "narrowed_set_in_request", "description_only"}
ON_VIOLATION = {"drop", "reject", "repair"}
REQUIRED_METRICS = {"grounding_rate", "empty_result_rate"}
REVIEW_MODES = {"sampling", "scorer", "none"}
SCORERS = {"none", "hhem-2.1-open", "other"}
# Scorers barred outright on licence (r7). CC BY-NC 4.0 against a commercial product.
BARRED_SCORERS = {"bespoke-minicheck", "bespoke-minicheck-7b", "llama-3.1-bespoke-minicheck-7b"}
NON_COMMERCIAL_MARKERS = ("cc by-nc", "by-nc", "non-commercial", "noncommercial")
# Phrases that mean the set is asserted rather than supplied (r1).
NOT_SUPPLIED_MARKERS = (
    "model memory",
    "model's memory",
    "from memory",
    "prior turn",
    "previous turn",
    "earlier model turn",
    "model recall",
    "world knowledge",
)
# `membership_check` values describing observation rather than enforcement (r4).
LOG_ONLY_MARKERS = ("logger.", "log.", "logging.", "console.", "warn only", "log only")
# Below this length a justification field is a UX affordance, not a claim (r6).
SHORT_JUSTIFICATION_CHARS = 500


def violations(c: dict) -> list[str]:
    errs: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in c:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    # r1 — the closedness claim.
    source = str(c["candidate_set_source"]).strip()
    if len(source) < 20:
        errs.append("candidate_set_source must name the artefact and when it is materialised (r1-closedness-test)")
    if any(m in source.lower() for m in NOT_SUPPLIED_MARKERS):
        errs.append(
            f"candidate_set_source {source!r} names asserted rather than supplied values: the field is "
            "not closed (r1-closedness-test)"
        )
    if len(str(c["closedness_evidence"]).strip()) < 40:
        errs.append(
            "closedness_evidence must show all three conditions against real data (r1-closedness-test)"
        )

    # r2 — selection, not authoring.
    shape = c["selection_prompt_shape"]
    if shape not in PROMPT_SHAPES:
        errs.append(f"selection_prompt_shape {shape!r} not in {sorted(PROMPT_SHAPES)}")
    elif shape == "description_only":
        errs.append(
            "selection_prompt_shape is 'description_only': a description of the set is not the set; "
            "supply the candidates (r2-select-do-not-author)"
        )

    # r4 — a policy plus a counter, never a log line.
    if c["on_violation"] not in ON_VIOLATION:
        errs.append(
            f"on_violation must be one of {sorted(ON_VIOLATION)} — logging is not a policy "
            "(r4-count-do-not-log)"
        )
    check = str(c["membership_check"]).strip()
    if len(check) < 10:
        errs.append("membership_check must name the code location performing the test (r4-count-do-not-log)")
    elif any(m in check.lower() for m in LOG_ONLY_MARKERS):
        errs.append(
            f"membership_check {check!r} only logs: a log line is invisible to a test and to the user "
            "(r4-count-do-not-log)"
        )
    if not str(c["counter"]).strip():
        errs.append("counter is required: an uncounted check is an unmeasured defect class (r4-count-do-not-log)")

    # r3 — the metric set.
    metrics = c["metrics"]
    if not isinstance(metrics, list):
        errs.append("metrics must be a list")
        metrics = []
    for missing in sorted(REQUIRED_METRICS - set(map(str, metrics))):
        errs.append(f"metrics missing {missing!r} (r3-membership-is-the-metric)")

    # r4 — thresholds need a baseline.
    if c.get("threshold") is not None and not c.get("baseline_measured"):
        errs.append(
            f"threshold {c['threshold']} is set with no measured baseline: record it as a guess or "
            "measure first (r4-count-do-not-log)"
        )

    # r5 / r6 — scope, and the short-justification anti-pattern.
    open_fields = c["open_fields"]
    if not isinstance(open_fields, list):
        errs.append("open_fields must be a list (may be empty, but the key is required) (r5-scope-the-metric-to-the-closed-field)")
        open_fields = []
    for i, f in enumerate(open_fields):
        if not isinstance(f, dict) or "name" not in f:
            errs.append(f"open_fields[{i}] must be a mapping with a name")
            continue
        review = str(f.get("review", ""))
        if review not in REVIEW_MODES:
            errs.append(f"open_fields[{i}] review must be one of {sorted(REVIEW_MODES)}")
        max_chars = f.get("max_chars")
        if f.get("claim_decompose") is True:
            if isinstance(max_chars, int) and max_chars < SHORT_JUSTIFICATION_CHARS:
                errs.append(
                    f"open_fields[{i}] ({f['name']}) sets claim_decompose on a {max_chars}-char capped "
                    "field: decomposing a one-liner costs judge tokens and measures phrasing "
                    "(r6-no-claim-decomposition-on-short-justifications)"
                )

    # r7 — the licence bar and the triage-not-gate rule.
    scorer = c.get("scorer")
    if scorer is not None:
        if str(scorer).lower() in BARRED_SCORERS:
            errs.append(
                f"scorer {scorer!r} is CC BY-NC 4.0 (non-commercial) and must not be used in or for a "
                "commercial product (r7-fallback-scorer-licence-bar)"
            )
        elif scorer not in SCORERS:
            errs.append(f"scorer {scorer!r} not in {sorted(SCORERS)}")
        elif scorer == "other":
            licence = str(c.get("scorer_licence", "")).strip()
            if not licence:
                errs.append("scorer 'other' requires scorer_licence (r7-fallback-scorer-licence-bar)")
            elif any(m in licence.lower() for m in NON_COMMERCIAL_MARKERS):
                errs.append(
                    f"scorer_licence {licence!r} is non-commercial (r7-fallback-scorer-licence-bar)"
                )
        if scorer != "none" and str(c.get("scorer_role", "")) == "gate":
            errs.append(
                "scorer_role is 'gate': a 64-77%-balanced-accuracy classifier is triage, never pass/fail "
                "(r7-fallback-scorer-licence-bar)"
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


def _base_contract() -> dict:
    return {
        "system": "rank a supplied candidate list of methodologies for a query",
        "closed_field": "hits[].id",
        "candidate_set_source": "the candidate slice built by the local index and sent in the request body",
        "closedness_evidence": (
            "Every legal id is a key of the candidate map we assembled this request; the map is "
            "supplied verbatim in the prompt; an id outside it refers to no document."
        ),
        "selection_prompt_shape": "narrowed_set_in_request",
        "membership_check": "agent.go candByID lookup over the decoded hits",
        "on_violation": "drop",
        "counter": "hallucinated_id_rate",
        "metrics": ["grounding_rate", "empty_result_rate", "hallucinated_id_rate"],
        "open_fields": [
            {"name": "hits[].why", "max_chars": 240, "review": "sampling", "claim_decompose": False}
        ],
        "scorer": "none",
    }


def self_test() -> int:
    ok = _base_contract()

    memory_set = dict(ok, candidate_set_source="ids recalled by the model from world knowledge at answer time")
    description = dict(ok, selection_prompt_shape="description_only")
    log_only = dict(ok, membership_check="logger.Warn on unknown id then continue")
    no_counter = dict(ok, counter="")
    thin_metrics = dict(ok, metrics=["grounding_rate"])
    guess_threshold = dict(ok, threshold=0.02)
    measured_threshold = dict(ok, threshold=0.02, baseline_measured=True)
    decompose_oneliner = json.loads(json.dumps(ok))
    decompose_oneliner["open_fields"][0]["claim_decompose"] = True
    barred = dict(ok, scorer="bespoke-minicheck", scorer_role="triage")
    nc_other = dict(ok, scorer="other", scorer_licence="CC BY-NC 4.0", scorer_role="triage")
    gating = dict(ok, scorer="hhem-2.1-open", scorer_role="gate")

    cases = [
        ("valid closed-set contract", ok, 0),
        ("candidate set from model memory", memory_set, 1),
        ("set described rather than supplied", description, 1),
        ("membership check only logs", log_only, 1),
        ("no counter declared", no_counter, 1),
        ("empty_result_rate missing", thin_metrics, 1),
        ("threshold with no baseline", guess_threshold, 1),
        ("threshold with measured baseline", measured_threshold, 0),
        ("claim decomposition on a 240-char field", decompose_oneliner, 1),
        ("non-commercial scorer", barred, 1),
        ("other scorer with NC licence", nc_other, 1),
        ("scorer used as a gate", gating, 1),
    ]
    failed = 0
    for name, doc, expect in cases:
        errs = violations(doc)
        got = 1 if errs else 0
        status = "ok " if got == expect else "FAIL"
        if got != expect:
            failed += 1
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
