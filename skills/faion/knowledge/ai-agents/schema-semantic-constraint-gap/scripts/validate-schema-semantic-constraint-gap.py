#!/usr/bin/env python3
"""Validate a Schema Pair Record against the schema-semantic-constraint-gap contract.

The drop set is COMPUTED, not asserted: the record carries both schemas inline and
this script diffs them, then demands a checker and a counter for every constraint
the wire schema no longer carries.

Usage:
  validate-schema-semantic-constraint-gap.py <spr.yaml|spr.json>
  validate-schema-semantic-constraint-gap.py --self-test
  validate-schema-semantic-constraint-gap.py --help

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

# Keywords that express SEMANTICS rather than shape. These are the ones a
# grammar compiler cannot represent and therefore the ones that go missing.
CONSTRAINT_KEYWORDS = frozenset(
    {
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "multipleOf",
        "minLength",
        "maxLength",
        "pattern",
        "maxItems",
        "minItems",
        "uniqueItems",
    }
)

# Anthropic structured outputs, platform.claude.com docs fetched 2026-08-03.
# `minItems` is the one partial case: 0 and 1 compile, anything else does not.
ANTHROPIC_UNSUPPORTED = frozenset(CONSTRAINT_KEYWORDS)
# Gemini compiles an OpenAPI 3.0 subset that accepts `pattern` and numeric
# ranges (docs fetched 2026-08-03). Anything beyond that must be declared by
# the author through transport `other` + `unsupported_keywords`.
GEMINI_UNSUPPORTED: frozenset[str] = frozenset()

TRANSPORTS = {"anthropic", "gemini", "other"}
ON_VIOLATION = {"drop", "reject", "clamp"}
CITATIONS_PLANS = {"none", "structured_only", "citations_only", "two_call"}
REQUIRED_KEYS = (
    "system",
    "transports",
    "wire_schema_path",
    "validation_schema_path",
    "validation_schema",
    "wire_schema",
    "dropped_keywords",
    "structured_output",
    "citations_enabled",
    "citations_plan",
    "metrics",
    "value_accuracy_review",
)
# `enforced_by` values that describe observation rather than enforcement (r3).
LOG_ONLY_MARKERS = ("logger.", "log.", "logging.", "console.", "warn only", "log only")


def collect(schema: object, pointer: str = "") -> dict[tuple[str, str], object]:
    """Map (json-pointer, keyword) -> value for every constraint keyword found."""
    found: dict[tuple[str, str], object] = {}
    if not isinstance(schema, dict):
        return found
    for key, value in schema.items():
        if key in CONSTRAINT_KEYWORDS:
            found[(pointer or "/", key)] = value
    props = schema.get("properties")
    if isinstance(props, dict):
        for name, sub in props.items():
            found.update(collect(sub, f"{pointer}/{name}"))
    items = schema.get("items")
    if isinstance(items, dict):
        found.update(collect(items, f"{pointer}[]"))
    defs = schema.get("$defs") or schema.get("definitions")
    if isinstance(defs, dict):
        for name, sub in defs.items():
            found.update(collect(sub, f"{pointer}#{name}"))
    for combinator in ("anyOf", "allOf", "oneOf"):
        branch = schema.get(combinator)
        if isinstance(branch, list):
            for i, sub in enumerate(branch):
                found.update(collect(sub, f"{pointer}<{combinator}{i}>"))
    return found


def unsupported_for(transports: list, declared: list) -> set[str]:
    """Union of the drop sets of every declared transport — the strictest level (r4)."""
    out: set[str] = set()
    for t in transports:
        if t == "anthropic":
            out |= set(ANTHROPIC_UNSUPPORTED)
        elif t == "gemini":
            out |= set(GEMINI_UNSUPPORTED)
        elif t == "other":
            out |= {str(k) for k in declared}
    return out


def violations(spr: dict) -> list[str]:
    errs: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in spr:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    transports = spr["transports"]
    if not isinstance(transports, list) or not transports:
        errs.append("transports must be a non-empty list")
        transports = []
    for t in transports:
        if t not in TRANSPORTS:
            errs.append(f"transport {t!r} not in {sorted(TRANSPORTS)}")
    declared = spr.get("unsupported_keywords") or []
    if "other" in transports and not declared:
        errs.append(
            "transports contains 'other' but unsupported_keywords is empty: "
            "name that provider's drop set from its own docs (r4-transport-divergence-is-declared)"
        )

    # r2 — two artefacts, two names.
    if spr["wire_schema_path"] == spr["validation_schema_path"]:
        errs.append(
            "wire_schema_path equals validation_schema_path: one file cannot be both the "
            "wire contract and the validation contract (r2-two-schema-split)"
        )

    # r5 — the citations fork.
    if bool(spr["structured_output"]) and bool(spr["citations_enabled"]):
        errs.append(
            "structured_output and citations_enabled are both true: the API returns 400; "
            "split into two calls (r5-citations-xor-structured-output)"
        )
    plan = spr["citations_plan"]
    if plan not in CITATIONS_PLANS:
        errs.append(f"citations_plan {plan!r} not in {sorted(CITATIONS_PLANS)}")
    if plan == "two_call" and len(str(spr.get("two_call_note", "")).strip()) < 30:
        errs.append(
            "citations_plan is 'two_call' but two_call_note does not describe the split "
            "(r5-citations-xor-structured-output)"
        )

    # The computed drop set: in the validation contract, absent from the wire copy.
    val_keys = collect(spr["validation_schema"])
    wire_keys = collect(spr["wire_schema"])
    dropped = {k for k in val_keys if k not in wire_keys}

    entries = spr["dropped_keywords"]
    if not isinstance(entries, list):
        errs.append("dropped_keywords must be a list")
        entries = []
    booked: set[tuple[str, str]] = set()
    for i, e in enumerate(entries):
        if not isinstance(e, dict) or "keyword" not in e or "field" not in e:
            errs.append(f"dropped_keywords[{i}] must be a mapping with keyword and field")
            continue
        key = (str(e["field"]), str(e["keyword"]))
        booked.add(key)
        if key not in dropped:
            errs.append(
                f"dropped_keywords[{i}] books {e['keyword']!r} at {e['field']!r} but the schema "
                "diff shows no such drop: phantom bookkeeping (r2-two-schema-split)"
            )
        on_violation = str(e.get("on_violation", ""))
        if on_violation not in ON_VIOLATION:
            errs.append(
                f"dropped_keywords[{i}] on_violation must be one of {sorted(ON_VIOLATION)} "
                "(r3-checker-and-counter-per-dropped-keyword)"
            )
        enforced_by = str(e.get("enforced_by", "")).strip()
        if len(enforced_by) < 5:
            errs.append(
                f"dropped_keywords[{i}] ({e['keyword']}) has no enforced_by code location "
                "(r3-checker-and-counter-per-dropped-keyword)"
            )
        elif any(m in enforced_by.lower() for m in LOG_ONLY_MARKERS):
            errs.append(
                f"dropped_keywords[{i}] ({e['keyword']}) enforced_by only logs: a log line is "
                "invisible to a test and to the user (r3-checker-and-counter-per-dropped-keyword)"
            )
        if not str(e.get("counter", "")).strip():
            errs.append(
                f"dropped_keywords[{i}] ({e['keyword']}) has no counter: an uncounted check is "
                "an unmeasured defect class (r3-checker-and-counter-per-dropped-keyword)"
            )

    for field, keyword in sorted(dropped - booked):
        errs.append(
            f"{keyword!r} at {field!r} is in the validation schema and not on the wire, with no "
            "dropped_keywords entry: nothing enforces it (r1-grammar-guarantees-shape-only)"
        )

    # r6 — nothing the declared transports drop may remain on the wire.
    unsupported = unsupported_for(transports, declared)
    for (field, keyword), value in sorted(wire_keys.items()):
        if keyword == "minItems" and value in (0, 1):
            continue  # compiled by Anthropic; the one partial case
        if keyword in unsupported:
            errs.append(
                f"wire_schema keeps {keyword!r} at {field!r}, which no declared transport compiles: "
                "strip it deliberately or risk a 400 (r6-no-hopeful-keywords-on-the-wire)"
            )

    # r7 — compliance is not the metric.
    metrics = spr["metrics"]
    if not isinstance(metrics, list):
        errs.append("metrics must be a list")
        metrics = []
    if "schema_valid_rate" not in metrics:
        errs.append("metrics must include schema_valid_rate (r7-compliance-is-not-value-accuracy)")
    counters = {str(e.get("counter")) for e in entries if isinstance(e, dict)}
    if not (set(map(str, metrics)) & counters):
        errs.append(
            "metrics declares no semantic rate over the dropped keywords: compliance alone is the "
            "already-saturated number (r7-compliance-is-not-value-accuracy)"
        )
    if len(str(spr["value_accuracy_review"]).strip()) < 20:
        errs.append(
            "value_accuracy_review must name where review budget goes now that compliance is not "
            "the bottleneck (r7-compliance-is-not-value-accuracy)"
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


def _base_record() -> dict:
    validation_schema = {
        "type": "object",
        "properties": {
            "hits": {
                "type": "array",
                "maxItems": 20,
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "pattern": "^[a-f0-9]{16}$"},
                        "score": {"type": "number", "minimum": 0, "maximum": 1},
                        "why": {"type": "string", "maxLength": 240},
                    },
                },
            }
        },
    }
    wire_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "hits": {
                "type": "array",
                "minItems": 0,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "score", "why"],
                    "properties": {
                        "id": {"type": "string"},
                        "score": {"type": "number"},
                        "why": {"type": "string"},
                    },
                },
            }
        },
    }
    return {
        "system": "ranking a supplied candidate list into a scored hit list",
        "transports": ["anthropic"],
        "wire_schema_path": "internal/search/schemas/search.wire.json",
        "validation_schema_path": "internal/search/schemas/search.validation.json",
        "validation_schema": validation_schema,
        "wire_schema": wire_schema,
        "dropped_keywords": [
            {
                "keyword": "maxItems",
                "field": "/hits",
                "on_violation": "clamp",
                "enforced_by": "search.Run clamps decoded hits to opts.Top",
                "counter": "overflow_rate",
            },
            {
                "keyword": "pattern",
                "field": "/hits[]/id",
                "on_violation": "drop",
                "enforced_by": "agent.go candByID membership check",
                "counter": "hallucinated_id_rate",
            },
            {
                "keyword": "minimum",
                "field": "/hits[]/score",
                "on_violation": "reject",
                "enforced_by": "search.validateHit range check",
                "counter": "range_violation_rate",
            },
            {
                "keyword": "maximum",
                "field": "/hits[]/score",
                "on_violation": "reject",
                "enforced_by": "search.validateHit range check",
                "counter": "range_violation_rate",
            },
            {
                "keyword": "maxLength",
                "field": "/hits[]/why",
                "on_violation": "clamp",
                "enforced_by": "search.validateHit rune-length check",
                "counter": "why_overflow_rate",
            },
        ],
        "structured_output": True,
        "citations_enabled": False,
        "citations_plan": "structured_only",
        "metrics": [
            "schema_valid_rate",
            "hallucinated_id_rate",
            "range_violation_rate",
            "why_overflow_rate",
            "overflow_rate",
        ],
        "value_accuracy_review": "sampled review of ranking order and why-text truthfulness, 20 queries per release",
    }


def self_test() -> int:
    ok = _base_record()

    missing_entry = json.loads(json.dumps(ok))
    missing_entry["dropped_keywords"] = [
        e for e in missing_entry["dropped_keywords"] if e["keyword"] != "pattern"
    ]

    log_only = json.loads(json.dumps(ok))
    log_only["dropped_keywords"][1]["enforced_by"] = "logger.Warn on unknown id, then continue"

    no_counter = json.loads(json.dumps(ok))
    no_counter["dropped_keywords"][1]["counter"] = ""

    hopeful_wire = json.loads(json.dumps(ok))
    hopeful_wire["wire_schema"]["properties"]["hits"]["items"]["properties"]["id"]["pattern"] = (
        "^[a-f0-9]{16}$"
    )
    hopeful_wire["dropped_keywords"] = [
        e for e in hopeful_wire["dropped_keywords"] if e["keyword"] != "pattern"
    ]

    both_on = json.loads(json.dumps(ok))
    both_on["citations_enabled"] = True

    compliance_only = json.loads(json.dumps(ok))
    compliance_only["metrics"] = ["schema_valid_rate"]

    one_file = json.loads(json.dumps(ok))
    one_file["wire_schema_path"] = one_file["validation_schema_path"]

    phantom = json.loads(json.dumps(ok))
    phantom["dropped_keywords"].append(
        {
            "keyword": "minLength",
            "field": "/hits[]/why",
            "on_violation": "reject",
            "enforced_by": "search.validateHit",
            "counter": "why_underflow_rate",
        }
    )

    two_call = json.loads(json.dumps(ok))
    two_call["citations_plan"] = "two_call"
    two_call["two_call_note"] = "short"

    cases = [
        ("valid single-transport record", ok, 0),
        ("dropped constraint with no entry", missing_entry, 1),
        ("enforced_by only logs", log_only, 1),
        ("check without a counter", no_counter, 1),
        ("unsupported keyword left on the wire", hopeful_wire, 1),
        ("citations and structured output together", both_on, 1),
        ("only schema_valid_rate declared", compliance_only, 1),
        ("one file used as both schemas", one_file, 1),
        ("phantom dropped_keywords entry", phantom, 1),
        ("two_call plan without a note", two_call, 1),
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
