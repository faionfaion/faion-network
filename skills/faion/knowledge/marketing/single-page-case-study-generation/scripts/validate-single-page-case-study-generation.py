#!/usr/bin/env python3
"""validate-single-page-case-study-generation.py

Validate the case-study report produced by the single-page-case-study-generation methodology against the
draft-07 JSON Schema embedded in content/02-output-contract.xml, plus the
cross-field rules from content/01-core-rules.xml the schema cannot express. Stdlib-only;
the schema and both fixtures are inlined because `faion get-content` ships
this file alone.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid + invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (VIOLATION lines on stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/single-page-case-study-generation.json', 'title': 'Single Page Case Study Generation report', 'type': 'object', 'required': ['publication_version', 'dates', 'title', 'slots', 'word_count', 'media_count', 'anonymisation', 'inputs_used', 'cta', 'outcome_review'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'ref': {'type': 'string', 'minLength': 5}}, 'properties': {'__faion_header__': {'type': ['object', 'string']}, 'publication_version': {'type': 'string', 'enum': ['named', 'anonymised', 'internal_log_only']}, 'dates': {'type': 'object', 'required': ['delivery_date', 'draft_date', 'publish_or_park_date', 'status'], 'additionalProperties': False, 'properties': {'delivery_date': {'$ref': '#/definitions/date'}, 'draft_date': {'$ref': '#/definitions/date'}, 'publish_or_park_date': {'$ref': '#/definitions/date'}, 'status': {'type': 'string', 'enum': ['published', 'parked']}, 'park_reason': {'type': 'string', 'minLength': 10}, 'revisit_date': {'$ref': '#/definitions/date'}}, 'if': {'properties': {'status': {'const': 'parked'}}}, 'then': {'required': ['park_reason', 'revisit_date']}}, 'title': {'type': 'string', 'minLength': 20, 'maxLength': 120, 'pattern': '[0-9]', 'not': {'pattern': '^(Backend|Frontend|Fullstack|Full-stack|Consulting|Development|Engineering|Design|Our |We |I |My )'}}, 'slots': {'type': 'object', 'required': ['problem', 'approach', 'outcome', 'numbers', 'pull_quote', 'nda_indicator'], 'additionalProperties': False, 'properties': {'problem': {'type': 'object', 'required': ['text', 'sentences'], 'additionalProperties': False, 'properties': {'text': {'type': 'string', 'minLength': 30}, 'sentences': {'type': 'integer', 'minimum': 1, 'maximum': 2}}}, 'approach': {'type': 'object', 'required': ['text', 'sentences', 'stack_or_method'], 'additionalProperties': False, 'properties': {'text': {'type': 'string', 'minLength': 60}, 'sentences': {'type': 'integer', 'minimum': 2, 'maximum': 3}, 'stack_or_method': {'type': 'string', 'minLength': 3}}}, 'outcome': {'type': 'object', 'required': ['text', 'sentences'], 'additionalProperties': False, 'properties': {'text': {'type': 'string', 'minLength': 20, 'pattern': '[0-9]', 'not': {'pattern': '(?i)significant|dramatic|huge|massive'}}, 'sentences': {'const': 1}}}, 'numbers': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['metric', 'baseline', 'final', 'unit', 'delta_pct', 'window', 'source_system', 'evidence_ref'], 'additionalProperties': False, 'properties': {'metric': {'type': 'string', 'minLength': 3}, 'baseline': {'type': 'number'}, 'final': {'type': 'number'}, 'unit': {'type': 'string', 'minLength': 1}, 'delta_pct': {'type': 'number'}, 'window': {'type': 'string', 'minLength': 8}, 'source_system': {'type': 'string', 'enum': ['stripe_export', 'server_logs', 'ga4_report', 'calendar', 'pnl', 'ticket_tracker', 'other_named_system']}, 'evidence_ref': {'$ref': '#/definitions/ref'}}}}, 'pull_quote': {'type': 'object', 'required': ['text', 'contact_role', 'permission_captured_in', 'permission_ref'], 'additionalProperties': False, 'properties': {'text': {'type': 'string', 'minLength': 20, 'not': {'pattern': '(?i)the client (was|were|is) (very )?(happy|pleased|satisfied)'}}, 'contact_name': {'type': 'string', 'minLength': 3}, 'contact_role': {'type': 'string', 'minLength': 3}, 'company': {'type': 'string', 'minLength': 2}, 'company_descriptor': {'type': 'string', 'minLength': 10}, 'permission_captured_in': {'type': 'string', 'enum': ['email', 'message']}, 'permission_ref': {'$ref': '#/definitions/ref'}}}, 'nda_indicator': {'type': 'string', 'enum': ['named', 'anonymised', 'full_version_on_request']}}}, 'word_count': {'type': 'integer', 'minimum': 1, 'maximum': 500}, 'media_count': {'type': 'integer', 'minimum': 0, 'maximum': 1}, 'anonymisation': {'anyOf': [{'type': 'null'}, {'type': 'object', 'required': ['industry', 'size_band', 'context', 'quoted_role', 'client_consent_ref', 'identifiers_removed'], 'additionalProperties': False, 'properties': {'industry': {'type': 'string', 'minLength': 3}, 'size_band': {'type': 'string', 'minLength': 3}, 'context': {'type': 'string', 'minLength': 3}, 'quoted_role': {'type': 'string', 'minLength': 3}, 'client_consent_ref': {'$ref': '#/definitions/ref'}, 'identifiers_removed': {'const': True}}}]}, 'inputs_used': {'type': 'array', 'minItems': 2, 'items': {'type': 'object', 'required': ['name', 'path'], 'additionalProperties': False, 'properties': {'name': {'$ref': '#/definitions/ref'}, 'path': {'type': 'string', 'minLength': 5}}}}, 'cta': {'type': 'object', 'required': ['count', 'target', 'url'], 'additionalProperties': False, 'properties': {'count': {'const': 1}, 'target': {'const': 'discovery_call'}, 'url': {'type': 'string', 'pattern': '^https?://.*(utm_|[?&]ref=|/r/)'}}}, 'outcome_review': {'type': 'object', 'required': ['due_date', 'findings'], 'additionalProperties': False, 'properties': {'due_date': {'$ref': '#/definitions/date'}, 'findings': {'anyOf': [{'type': 'null'}, {'type': 'object', 'required': ['held_on', 'discovery_calls_attributed', 'included_in_closed_proposal'], 'additionalProperties': False, 'properties': {'held_on': {'$ref': '#/definitions/date'}, 'discovery_calls_attributed': {'type': 'integer', 'minimum': 0}, 'included_in_closed_proposal': {'type': 'boolean'}}}]}}}}, 'allOf': [{'if': {'properties': {'publication_version': {'const': 'named'}}}, 'then': {'properties': {'anonymisation': {'type': 'null'}, 'slots': {'properties': {'pull_quote': {'required': ['contact_name', 'company']}, 'nda_indicator': {'enum': ['named', 'full_version_on_request']}}}}}}, {'if': {'properties': {'publication_version': {'const': 'anonymised'}}}, 'then': {'properties': {'anonymisation': {'type': 'object'}, 'slots': {'properties': {'pull_quote': {'required': ['company_descriptor'], 'not': {'required': ['contact_name']}}, 'nda_indicator': {'const': 'anonymised'}}}}}}]}

OK = {'publication_version': 'named', 'dates': {'delivery_date': '2026-08-28', 'draft_date': '2026-09-02', 'publish_or_park_date': '2026-09-09', 'status': 'published'}, 'title': 'How Kestrel Pay cut checkout latency 62 percent in 3 weeks', 'slots': {'problem': {'text': "Kestrel Pay's hosted checkout took 1.5 seconds at the 95th percentile and merchants were escalating abandoned carts every week. The team had no capacity to profile it between feature releases.", 'sentences': 2}, 'approach': {'text': 'Over three weeks I profiled the checkout path with OpenTelemetry traces and found two serial calls to the risk service. I collapsed them into one batched gRPC call and moved the currency lookup to a Redis cache with a 10-minute TTL. The change shipped behind a feature flag and was rolled out to 100 percent over four days.', 'sentences': 3, 'stack_or_method': 'OpenTelemetry, gRPC batching, Redis cache, feature-flagged rollout'}, 'outcome': {'text': 'p95 checkout latency fell from 1,480 ms to 560 ms, a 62 percent reduction, within three weeks of the first trace.', 'sentences': 1}, 'numbers': [{'metric': 'p95 checkout latency', 'baseline': 1480, 'final': 560, 'unit': 'ms', 'delta_pct': -62.2, 'window': '30 days before vs 30 days after rollout', 'source_system': 'server_logs', 'evidence_ref': 'grafana-p95-export-2026-08.csv'}, {'metric': 'checkout abandonment', 'baseline': 18.4, 'final': 14.1, 'unit': 'percent', 'delta_pct': -23.4, 'window': '30 days before vs 30 days after rollout', 'source_system': 'ga4_report', 'evidence_ref': 'ga4-checkout-funnel-2026-08.csv'}], 'pull_quote': {'text': 'Checkout stopped being the thing we apologised for in every merchant call.', 'contact_name': 'Maria Voss', 'contact_role': 'VP Engineering', 'company': 'Kestrel Pay', 'permission_captured_in': 'email', 'permission_ref': 'permission-voss-2026-09-01.eml'}, 'nda_indicator': 'named'}, 'word_count': 310, 'media_count': 1, 'anonymisation': None, 'inputs_used': [{'name': 'grafana-p95-export-2026-08.csv', 'path': 'evidence/kestrel-pay/grafana-p95-export-2026-08.csv'}, {'name': 'ga4-checkout-funnel-2026-08.csv', 'path': 'evidence/kestrel-pay/ga4-checkout-funnel-2026-08.csv'}, {'name': 'permission-voss-2026-09-01.eml', 'path': 'evidence/kestrel-pay/permission-voss-2026-09-01.eml'}], 'cta': {'count': 1, 'target': 'discovery_call', 'url': 'https://example.com/book?utm_source=case-study&utm_campaign=kestrel-latency'}, 'outcome_review': {'due_date': '2026-12-08', 'findings': None}}

BAD = {'publication_version': 'named', 'dates': {'delivery_date': '2026-03-10', 'draft_date': '2026-08-28', 'publish_or_park_date': '2026-09-30', 'status': 'published'}, 'title': 'Backend consulting for a fintech client', 'slots': {'problem': {'text': 'Checkout was slow and the client wanted it faster, so they hired me to look at it, which I did over a few weeks, and there were many things wrong.', 'sentences': 4}, 'approach': {'text': 'I fixed it.', 'sentences': 1, 'stack_or_method': ''}, 'outcome': {'text': 'A significant improvement in checkout performance.', 'sentences': 1}, 'numbers': [{'metric': 'latency', 'baseline': 0, 'final': 0, 'unit': '', 'delta_pct': -60, 'window': 'later', 'source_system': 'the client told me', 'evidence_ref': 'n/a'}], 'pull_quote': {'text': 'The client was very happy with the result.', 'contact_role': '', 'permission_captured_in': 'verbal', 'permission_ref': 'none'}, 'nda_indicator': 'named'}, 'word_count': 900, 'media_count': 3, 'anonymisation': None, 'inputs_used': [], 'cta': {'count': 3, 'target': 'contact_page', 'url': 'https://example.com/contact'}, 'outcome_review': {'due_date': '2027-06-01', 'findings': None}}


def _is_type(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        return (isinstance(value, int) and not isinstance(value, bool)) or (
            isinstance(value, float) and value.is_integer())
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    return True


def _check(node, schema, path, errs):
    """Draft-07 subset: $ref (local definitions), required, type, enum, const, pattern,
    minimum/maximum, exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems,
    uniqueItems, items, contains, properties, additionalProperties, allOf/anyOf/oneOf/not,
    if/then/else."""
    if schema is True:
        return
    if schema is False:
        errs.append(f"{path}: schema forbids any value here")
        return
    if "$ref" in schema:
        target = SCHEMA
        for part in schema["$ref"].lstrip("#/").split("/"):
            target = target[part]
        _check(node, target, path, errs)
        return
    if "const" in schema and node != schema["const"]:
        errs.append(f"{path}: must equal {schema['const']!r}, got {node!r}")
    if "enum" in schema and node not in schema["enum"]:
        errs.append(f"{path}: {node!r} not in enum {schema['enum']!r}")
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_is_type(node, x) for x in types):
            errs.append(f"{path}: expected {t}, got {type(node).__name__}")
            return
    if isinstance(node, dict):
        for k in schema.get("required", []):
            if k not in node:
                errs.append(f"{path}.{k}: missing required field")
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in node:
                _check(node[k], sub, f"{path}.{k}", errs)
        addl = schema.get("additionalProperties", True)
        for k in node:
            if k not in props:
                if addl is False:
                    errs.append(f"{path}.{k}: additional property not allowed")
                elif isinstance(addl, dict):
                    _check(node[k], addl, f"{path}.{k}", errs)
    if isinstance(node, list):
        mn, mx = schema.get("minItems"), schema.get("maxItems")
        if mn is not None and len(node) < mn:
            errs.append(f"{path}: {len(node)} items, minItems={mn}")
        if mx is not None and len(node) > mx:
            errs.append(f"{path}: {len(node)} items, maxItems={mx}")
        if schema.get("uniqueItems"):
            seen = [json.dumps(x, sort_keys=True) for x in node]
            if len(seen) != len(set(seen)):
                errs.append(f"{path}: items must be unique")
        items = schema.get("items")
        if isinstance(items, dict):
            for i, item in enumerate(node):
                _check(item, items, f"{path}[{i}]", errs)
        if "contains" in schema and not any(not _probe(item, schema["contains"]) for item in node):
            errs.append(f"{path}: no item matches 'contains' {schema['contains']!r}")
    if isinstance(node, str):
        mn, mx = schema.get("minLength"), schema.get("maxLength")
        if mn is not None and len(node) < mn:
            errs.append(f"{path}: length {len(node)} below minLength={mn}")
        if mx is not None and len(node) > mx:
            errs.append(f"{path}: length {len(node)} above maxLength={mx}")
        pat = schema.get("pattern")
        if pat is not None and not re.search(pat, node):
            errs.append(f"{path}: {node!r} does not match pattern {pat!r}")
    if isinstance(node, (int, float)) and not isinstance(node, bool):
        for key, bad in (("minimum", lambda v: node < v), ("maximum", lambda v: node > v),
                         ("exclusiveMinimum", lambda v: node <= v),
                         ("exclusiveMaximum", lambda v: node >= v)):
            if key in schema and bad(schema[key]):
                errs.append(f"{path}: {node!r} violates {key}={schema[key]!r}")
    for sub in schema.get("allOf", []):
        _check(node, sub, path, errs)
    if "anyOf" in schema:
        if not any(not _probe(node, s) for s in schema["anyOf"]):
            errs.append(f"{path}: matches none of anyOf")
    if "oneOf" in schema:
        hits = sum(1 for s in schema["oneOf"] if not _probe(node, s))
        if hits != 1:
            errs.append(f"{path}: matches {hits} of oneOf, need exactly 1")
    if "not" in schema and not _probe(node, schema["not"]):
        errs.append(f"{path}: matches forbidden 'not' schema")
    if "if" in schema:
        branch = "then" if not _probe(node, schema["if"]) else "else"
        if branch in schema:
            _check(node, schema[branch], path, errs)


def _probe(node, schema):
    tmp: list[str] = []
    _check(node, schema, "$", tmp)
    return tmp


from datetime import date as _date


def _d(s):
    try:
        return _date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _sentences(text: str) -> int:
    return len([s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s])


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    d = obj.get("dates") or {}
    dl, dr, pp = _d(d.get("delivery_date")), _d(d.get("draft_date")), _d(d.get("publish_or_park_date"))
    if dl and dr:
        if (dr - dl).days > 30:
            errs.append(f"dates.draft_date is {(dr - dl).days} days after delivery; past 30 days the engagement is logged as missed, not written up (r-seven-day-draft-fourteen-day-publish)")
        elif (dr - dl).days > 7:
            errs.append(f"dates.draft_date is {(dr - dl).days} days after delivery_date; the draft is due within 7 (r-seven-day-draft-fourteen-day-publish)")
        if dr < dl:
            errs.append("dates.draft_date precedes delivery_date (r-seven-day-draft-fourteen-day-publish)")
    if dl and pp and (pp - dl).days > 14:
        errs.append(f"dates.publish_or_park_date is {(pp - dl).days} days after delivery_date; publish or park within 14 (r-seven-day-draft-fourteen-day-publish)")
    if dr and pp and pp < dr:
        errs.append("dates.publish_or_park_date precedes draft_date (r-seven-day-draft-fourteen-day-publish)")
    slots = obj.get("slots") or {}
    words = 0
    for name in ("problem", "approach", "outcome"):
        sl = slots.get(name) or {}
        text = sl.get("text")
        if isinstance(text, str):
            words += len(text.split())
            got = _sentences(text)
            if isinstance(sl.get("sentences"), int) and got != sl["sentences"]:
                errs.append(f"slots.{name}.sentences {sl['sentences']} but the text has {got} sentences (r-six-slots-on-one-page)")
    q = (slots.get("pull_quote") or {}).get("text")
    if isinstance(q, str):
        words += len(q.split())
    wc = obj.get("word_count")
    if isinstance(wc, int) and words > wc:
        errs.append(f"word_count {wc} is below the {words} words already in the slots (r-six-slots-on-one-page)")
    names = {i.get("name") for i in obj.get("inputs_used") or [] if isinstance(i, dict)}
    for n, num in enumerate(slots.get("numbers") or []):
        b, f, dp = num.get("baseline"), num.get("final"), num.get("delta_pct")
        if _num(b) and _num(f) and _num(dp) and b != 0:
            want = (f - b) / b * 100
            if abs(dp - want) > 0.15:
                errs.append(f"slots.numbers[{n}].delta_pct {dp} is not (final - baseline) / baseline = {want:.1f} percent (r-numbers-baseline-final-delta)")
        if _num(b) and b == 0:
            errs.append(f"slots.numbers[{n}].baseline is 0; a delta needs an absolute baseline (r-numbers-baseline-final-delta)")
        if num.get("evidence_ref") not in names:
            errs.append(f"slots.numbers[{n}].evidence_ref {num.get('evidence_ref')!r} is not stored under inputs_used (r-evidence-source-named-and-kept)")
    pr = (slots.get("pull_quote") or {}).get("permission_ref")
    if pr is not None and pr not in names:
        errs.append(f"slots.pull_quote.permission_ref {pr!r} is not stored under inputs_used (r-pull-quote-verbatim-with-written-permission)")
    an = obj.get("anonymisation")
    if isinstance(an, dict) and an.get("client_consent_ref") not in names:
        errs.append(f"anonymisation.client_consent_ref {an.get('client_consent_ref')!r} is not stored under inputs_used (r-nda-fallback-never-drop)")
    due = _d((obj.get("outcome_review") or {}).get("due_date"))
    if pp and due and d.get("status") == "published" and (due - pp).days != 90:
        errs.append(f"outcome_review.due_date is {(due - pp).days} days after publication; the review is at 90 (r-single-cta-tracked-to-discovery-call)")
    return errs


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    _check(obj, SCHEMA, "$", errs)
    if not errs:
        errs.extend(extra(obj))
    return errs


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-single-page-case-study-generation.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run the contract's own examples and exit")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
