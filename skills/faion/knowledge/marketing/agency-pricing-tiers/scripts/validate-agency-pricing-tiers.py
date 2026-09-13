#!/usr/bin/env python3
"""validate-agency-pricing-tiers.py

Validate the artefact produced by the agency-pricing-tiers methodology against the JSON Schema
(draft-07) embedded in content/02-output-contract.xml, plus the cross-field rules from
content/01-core-rules.xml the schema cannot express. Stdlib-only, self-contained.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid + invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#',
 '$id': 'https://faion.net/schemas/agency-pricing-tiers.json',
 'title': 'Agency Pricing Tiers playbook step',
 'type': 'object',
 'required': ['currency',
              'tiers',
              'fence',
              'default_recommendation',
              'presentation',
              'scope_up',
              'concessions',
              'steps'],
 'additionalProperties': False,
 'definitions': {'money': {'type': 'number', 'minimum': 0},
                 'deliverable': {'type': 'object',
                                 'required': ['name', 'quantity', 'turnaround_days'],
                                 'additionalProperties': False,
                                 'properties': {'name': {'type': 'string', 'minLength': 3},
                                                'quantity': {'type': 'integer', 'minimum': 1},
                                                'turnaround_days': {'type': 'integer',
                                                                    'minimum': 1}}}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'currency': {'type': 'string', 'pattern': '^[A-Z]{3}$'},
                'tiers': {'type': 'array',
                          'minItems': 3,
                          'maxItems': 3,
                          'items': [{'properties': {'name': {'const': 'good'}}},
                                    {'properties': {'name': {'const': 'better'}}},
                                    {'properties': {'name': {'const': 'best'}}}],
                          'allOf': [{'items': {'type': 'object',
                                               'required': ['name',
                                                            'price',
                                                            'delivery_cost',
                                                            'gross_margin_abs',
                                                            'gross_margin_pct',
                                                            'deliverables'],
                                               'additionalProperties': False,
                                               'properties': {'name': {'type': 'string',
                                                                       'enum': ['good',
                                                                                'better',
                                                                                'best']},
                                                              'price': {'type': 'number',
                                                                        'exclusiveMinimum': 0},
                                                              'delivery_cost': {'type': 'object',
                                                                                'required': ['hours',
                                                                                             'loaded_hourly_cost',
                                                                                             'pass_through'],
                                                                                'additionalProperties': False,
                                                                                'properties': {'hours': {'type': 'number',
                                                                                                         'exclusiveMinimum': 0},
                                                                                               'loaded_hourly_cost': {'type': 'number',
                                                                                                                      'exclusiveMinimum': 0},
                                                                                               'pass_through': {'$ref': '#/definitions/money'}}},
                                                              'gross_margin_abs': {'type': 'number'},
                                                              'gross_margin_pct': {'type': 'number',
                                                                                   'maximum': 1},
                                                              'deliverables': {'type': 'array',
                                                                               'minItems': 1,
                                                                               'items': {'$ref': '#/definitions/deliverable'}}}}}]},
                'gap_justification': {'type': 'object',
                                      'required': ['scope_difference'],
                                      'additionalProperties': False,
                                      'properties': {'scope_difference': {'type': 'string',
                                                                          'minLength': 10}}},
                'fence': {'type': 'object',
                          'required': ['omitted_deliverable', 'needed_for', 'named_on_rate_sheet'],
                          'additionalProperties': False,
                          'properties': {'omitted_deliverable': {'type': 'string', 'minLength': 3},
                                         'needed_for': {'type': 'string', 'minLength': 10},
                                         'named_on_rate_sheet': {'const': True}}},
                'default_recommendation': {'const': 'better'},
                'presentation': {'type': 'object',
                                 'required': ['order', 'prices_visible'],
                                 'additionalProperties': False,
                                 'properties': {'order': {'type': 'array',
                                                          'minItems': 3,
                                                          'maxItems': 3,
                                                          'items': [{'const': 'best'},
                                                                    {'const': 'better'},
                                                                    {'const': 'good'}]},
                                                'prices_visible': {'const': True}}},
                'scope_up': {'type': 'object',
                             'required': ['trigger',
                                          'price_rule',
                                          'approver',
                                          'written_confirmation_required',
                                          'free_goodwill_allowed'],
                             'additionalProperties': False,
                             'properties': {'trigger': {'type': 'string', 'minLength': 10},
                                            'price_rule': {'const': 'difference between the two '
                                                                    'tier prices pro-rated to the '
                                                                    'remaining term'},
                                            'approver': {'type': 'string', 'minLength': 3},
                                            'written_confirmation_required': {'const': True},
                                            'free_goodwill_allowed': {'const': False}}},
                'concessions': {'type': 'object',
                                'required': ['method', 'published_prices_vary_by_client'],
                                'additionalProperties': False,
                                'properties': {'method': {'const': 'remove_named_deliverable_or_quantity'},
                                               'published_prices_vary_by_client': {'const': False}}},
                'steps': {'type': 'array',
                          'minItems': 1,
                          'items': {'type': 'object',
                                    'required': ['id', 'name', 'exit_criterion', 'output_location'],
                                    'additionalProperties': False,
                                    'properties': {'id': {'type': 'string', 'pattern': '^s[0-9]+$'},
                                                   'name': {'type': 'string', 'minLength': 3},
                                                   'exit_criterion': {'type': 'string',
                                                                      'minLength': 10,
                                                                      'not': {'pattern': '^(?i:shipped|reviewed|signoff|done)$'}},
                                                   'output_location': {'type': 'string',
                                                                       'minLength': 3}}}}}}

OK = {'currency': 'EUR',
 'tiers': [{'name': 'good',
            'price': 3000,
            'delivery_cost': {'hours': 20, 'loaded_hourly_cost': 90, 'pass_through': 200},
            'gross_margin_abs': 1000,
            'gross_margin_pct': 0.333,
            'deliverables': [{'name': 'paid search campaigns managed',
                              'quantity': 2,
                              'turnaround_days': 5},
                             {'name': 'monthly performance report',
                              'quantity': 1,
                              'turnaround_days': 3}]},
           {'name': 'better',
            'price': 5000,
            'delivery_cost': {'hours': 28, 'loaded_hourly_cost': 90, 'pass_through': 300},
            'gross_margin_abs': 2180,
            'gross_margin_pct': 0.436,
            'deliverables': [{'name': 'paid search campaigns managed',
                              'quantity': 4,
                              'turnaround_days': 3},
                             {'name': 'monthly performance report',
                              'quantity': 1,
                              'turnaround_days': 2},
                             {'name': 'conversion tracking setup',
                              'quantity': 1,
                              'turnaround_days': 10},
                             {'name': 'weekly optimisation call',
                              'quantity': 4,
                              'turnaround_days': 7}]},
           {'name': 'best',
            'price': 8000,
            'delivery_cost': {'hours': 36, 'loaded_hourly_cost': 90, 'pass_through': 400},
            'gross_margin_abs': 4360,
            'gross_margin_pct': 0.545,
            'deliverables': [{'name': 'paid search campaigns managed',
                              'quantity': 8,
                              'turnaround_days': 2},
                             {'name': 'monthly performance report',
                              'quantity': 1,
                              'turnaround_days': 1},
                             {'name': 'conversion tracking setup',
                              'quantity': 1,
                              'turnaround_days': 5},
                             {'name': 'weekly optimisation call',
                              'quantity': 4,
                              'turnaround_days': 7},
                             {'name': 'landing page A/B test',
                              'quantity': 2,
                              'turnaround_days': 14}]}],
 'fence': {'omitted_deliverable': 'conversion tracking setup',
           'needed_for': 'an e-commerce ICP cannot report ROAS without conversion tracking',
           'named_on_rate_sheet': True},
 'default_recommendation': 'better',
 'presentation': {'order': ['best', 'better', 'good'], 'prices_visible': True},
 'scope_up': {'trigger': "client requests a deliverable or quantity outside the current tier's "
                         'list',
              'price_rule': 'difference between the two tier prices pro-rated to the remaining '
                            'term',
              'approver': 'account director',
              'written_confirmation_required': True,
              'free_goodwill_allowed': False},
 'concessions': {'method': 'remove_named_deliverable_or_quantity',
                 'published_prices_vary_by_client': False},
 'steps': [{'id': 's1',
            'name': 'cost every tier',
            'exit_criterion': 'best gross margin is the highest in EUR and percent: 4360 / 54.5 '
                              'percent against 2180 / 43.6 and 1000 / 33.3',
            'output_location': 'pricing/2026-05-rate-sheet.md'},
           {'id': 's2',
            'name': 'publish best-first rate sheet',
            'exit_criterion': 'rate sheet lists best, better, good with prices visible and the '
                              'fence named under good',
            'output_location': 'pricing/2026-05-rate-sheet.md'},
           {'id': 's3',
            'name': 'brief account managers on scope-up',
            'exit_criterion': 'every account manager can state trigger, price rule and approver; '
                              'first scope-up logged with written confirmation',
            'output_location': 'pricing/scope-up-log.md'}]}

BAD = {'currency': 'EUR',
 'tiers': [{'name': 'good',
            'price': 5000,
            'delivery_cost': {'hours': 30, 'loaded_hourly_cost': 90, 'pass_through': 200},
            'gross_margin_abs': 2100,
            'gross_margin_pct': 0.42,
            'deliverables': [{'name': 'paid search campaigns managed',
                              'quantity': 2,
                              'turnaround_days': 5},
                             {'name': 'conversion tracking setup',
                              'quantity': 1,
                              'turnaround_days': 10},
                             {'name': 'monthly performance report',
                              'quantity': 1,
                              'turnaround_days': 3}]},
           {'name': 'better',
            'price': 10000,
            'delivery_cost': {'hours': 70, 'loaded_hourly_cost': 90, 'pass_through': 300},
            'gross_margin_abs': 3400,
            'gross_margin_pct': 0.34,
            'deliverables': [{'name': 'paid search campaigns managed',
                              'quantity': 4,
                              'turnaround_days': 3},
                             {'name': 'social campaigns managed',
                              'quantity': 2,
                              'turnaround_days': 3},
                             {'name': 'monthly performance report',
                              'quantity': 1,
                              'turnaround_days': 2}]},
           {'name': 'best',
            'price': 15000,
            'delivery_cost': {'hours': 140, 'loaded_hourly_cost': 90, 'pass_through': 400},
            'gross_margin_abs': 2000,
            'gross_margin_pct': 0.133,
            'deliverables': [{'name': 'paid search campaigns managed',
                              'quantity': 8,
                              'turnaround_days': 2},
                             {'name': 'monthly performance report',
                              'quantity': 1,
                              'turnaround_days': 1},
                             {'name': 'landing page A/B test',
                              'quantity': 4,
                              'turnaround_days': 14},
                             {'name': 'creative production',
                              'quantity': 6,
                              'turnaround_days': 10}]}],
 'fence': {'omitted_deliverable': 'conversion tracking setup',
           'needed_for': 'an e-commerce ICP cannot report ROAS without conversion tracking',
           'named_on_rate_sheet': True},
 'default_recommendation': 'better',
 'presentation': {'order': ['good', 'better', 'best'], 'prices_visible': False},
 'scope_up': {'trigger': 'client asks for something extra',
              'price_rule': 'difference between the two tier prices pro-rated to the remaining '
                            'term',
              'approver': 'account manager',
              'written_confirmation_required': True,
              'free_goodwill_allowed': True},
 'concessions': {'method': 'remove_named_deliverable_or_quantity',
                 'published_prices_vary_by_client': True},
 'steps': [{'id': 's1',
            'name': 'publish rate sheet',
            'exit_criterion': 'shipped',
            'output_location': 'pricing/rate-sheet.md'}]}


# --------------------------------------------------------------------------
# draft-07 subset: required, type, enum, const, pattern, minimum/maximum,
# exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems,
# minProperties/maxProperties, uniqueItems, items, contains, properties,
# additionalProperties, allOf/anyOf/oneOf/not, if/then/else, local $ref
# (#/definitions/...). Enough for every constraint the contract declares.
# --------------------------------------------------------------------------

_TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def _check(schema: dict, value, path: str, errs: list[str]) -> None:
    if schema is True or schema == {}:
        return
    if schema is False:
        errs.append(f"{path or '$'}: schema forbids any value")
        return
    if "$ref" in schema:
        node = SCHEMA
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node[part]
        merged = dict(node)
        merged.update({k: v for k, v in schema.items() if k != "$ref"})
        schema = merged
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_TYPES[x](value) for x in types):
            errs.append(f"{path or '$'}: expected type {'/'.join(types)}, got {type(value).__name__}")
            return
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path or '$'}: {value!r} not in {schema['enum']!r}")
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path or '$'}: must equal {schema['const']!r}, got {value!r}")
    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{path or '$'}: {value!r} does not match /{schema['pattern']}/")
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append(f"{path or '$'}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append(f"{path or '$'}: longer than maxLength {schema['maxLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{path or '$'}: {value} below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{path or '$'}: {value} above maximum {schema['maximum']}")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errs.append(f"{path or '$'}: {value} not above exclusiveMinimum {schema['exclusiveMinimum']}")
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            errs.append(f"{path or '$'}: {value} not below exclusiveMaximum {schema['exclusiveMaximum']}")
        if "multipleOf" in schema and abs(round(value / schema["multipleOf"]) * schema["multipleOf"] - value) > 1e-9:
            errs.append(f"{path or '$'}: {value} is not a multiple of {schema['multipleOf']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path or '$'}: fewer than minItems {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{path or '$'}: more than maxItems {schema['maxItems']}")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errs.append(f"{path or '$'}: items are not unique")
        if "items" in schema:
            if isinstance(schema["items"], list):
                for i, (sub, item) in enumerate(zip(schema["items"], value)):
                    _check(sub, item, f"{path}[{i}]", errs)
            else:
                for i, item in enumerate(value):
                    _check(schema["items"], item, f"{path}[{i}]", errs)
        if "contains" in schema:
            if not any(_ok(schema["contains"], item) for item in value):
                errs.append(f"{path or '$'}: no element satisfies `contains`")
    if isinstance(value, dict):
        for k in schema.get("required", []):
            if k not in value:
                errs.append(f"{path or '$'}: missing required field {k!r}")
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            errs.append(f"{path or '$'}: fewer than minProperties {schema['minProperties']}")
        if "maxProperties" in schema and len(value) > schema["maxProperties"]:
            errs.append(f"{path or '$'}: more than maxProperties {schema['maxProperties']}")
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in value:
                _check(sub, value[k], f"{path}.{k}" if path else k, errs)
        ap = schema.get("additionalProperties", True)
        if ap is False:
            for k in value:
                if k not in props:
                    errs.append(f"{path or '$'}: additional property {k!r} not allowed")
        elif isinstance(ap, dict):
            for k in value:
                if k not in props:
                    _check(ap, value[k], f"{path}.{k}" if path else k, errs)
    for sub in schema.get("allOf", []):
        _check(sub, value, path, errs)
    if "anyOf" in schema and not any(_ok(s, value) for s in schema["anyOf"]):
        errs.append(f"{path or '$'}: matches none of anyOf")
    if "oneOf" in schema and sum(_ok(s, value) for s in schema["oneOf"]) != 1:
        errs.append(f"{path or '$'}: must match exactly one of oneOf")
    if "not" in schema and _ok(schema["not"], value):
        errs.append(f"{path or '$'}: matches forbidden `not` schema")
    if "if" in schema:
        branch = "then" if _ok(schema["if"], value) else "else"
        if branch in schema:
            _check(schema[branch], value, path, errs)


def _ok(schema, value) -> bool:
    tmp: list[str] = []
    _check(schema, value, "", tmp)
    return not tmp

_BAND = {("good", "better"): (1.67 * 0.85, 1.67 * 1.15), ("better", "best"): (1.6 * 0.85, 1.6 * 1.15)}


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    tiers = [t for t in obj.get("tiers") or [] if isinstance(t, dict)]
    by = {t.get("name"): t for t in tiers}
    if [t.get("name") for t in tiers] != ["good", "better", "best"]:
        errs.append("tiers must be exactly good, better, best in that order (r-exactly-three-priced-tiers)")
        return errs
    for t in tiers:
        dc = t.get("delivery_cost") or {}
        cost = dc.get("hours", 0) * dc.get("loaded_hourly_cost", 0) + dc.get("pass_through", 0)
        want_abs = round(t.get("price", 0) - cost, 2)
        if abs(want_abs - t.get("gross_margin_abs", -1e9)) > 0.01:
            errs.append(f"tiers[{t['name']}]: gross_margin_abs must be price - (hours x loaded_hourly_cost + pass_through) = {want_abs} (r-best-tier-highest-margin)")
        if t.get("price"):
            want_pct = round(want_abs / t["price"], 3)
            if abs(want_pct - t.get("gross_margin_pct", -1)) > 0.0015:
                errs.append(f"tiers[{t['name']}]: gross_margin_pct must be gross_margin_abs / price = {want_pct} (r-best-tier-highest-margin)")
    best = by["best"]
    for other in ("good", "better"):
        if by[other].get("gross_margin_abs", 0) >= best.get("gross_margin_abs", 0) or by[other].get("gross_margin_pct", 0) >= best.get("gross_margin_pct", 0):
            errs.append(f"tiers: best margin ({best.get('gross_margin_abs')} / {best.get('gross_margin_pct')}) does not exceed {other} ({by[other].get('gross_margin_abs')} / {by[other].get('gross_margin_pct')}) (r-best-tier-highest-margin)")
    just = (obj.get("gap_justification") or {}).get("scope_difference")
    echoed = just and any(just in str(s.get("exit_criterion", "")) for s in obj.get("steps") or [] if isinstance(s, dict))
    for (lo, hi), (bmin, bmax) in _BAND.items():
        if by[lo].get("price"):
            ratio = by[hi]["price"] / by[lo]["price"]
            if not (bmin <= ratio <= bmax) and not echoed:
                errs.append(f"tiers: {hi} / {lo} price ratio {round(ratio, 2)} is outside {round(bmin, 2)}-{round(bmax, 2)} (3 / 5 / 8 within 15 percent) and no gap_justification is echoed in a step's exit_criterion (r-price-gaps-follow-3-5-8)")
    for lo, hi in (("good", "better"), ("better", "best")):
        upper = {d.get("name"): d for d in by[hi].get("deliverables") or []}
        for d in by[lo].get("deliverables") or []:
            u = upper.get(d.get("name"))
            if u is None:
                errs.append(f"tiers: deliverable {d.get('name')!r} in {lo} is missing from {hi} (r-tiers-are-strict-supersets)")
            elif u.get("quantity", 0) < d.get("quantity", 0) or u.get("turnaround_days", 0) > d.get("turnaround_days", 0):
                errs.append(f"tiers: deliverable {d.get('name')!r} in {hi} has lower quantity or slower turnaround than in {lo} (r-tiers-are-strict-supersets)")
    fence = (obj.get("fence") or {}).get("omitted_deliverable")
    if fence:
        if fence in {d.get("name") for d in by["good"].get("deliverables") or []}:
            errs.append(f"fence: {fence!r} is present in the good tier, so it does not fence it (r-good-tier-fenced-middle-tier-complete)")
        if fence not in {d.get("name") for d in by["better"].get("deliverables") or []}:
            errs.append(f"fence: {fence!r} is not in the better tier; the middle tier must be complete (r-good-tier-fenced-middle-tier-complete)")
    return errs


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    _check(SCHEMA, obj, "", errs)
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
        prog="validate-agency-pricing-tiers.py",
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
