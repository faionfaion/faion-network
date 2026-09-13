#!/usr/bin/env python3
"""validate-evolutionary-architecture-fitness-functions.py

Validate a fitness-function suite spec against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the evolutionary-architecture-fitness-functions methodology, plus the
cross-field rules the schema cannot express. Stdlib-only, self-contained.

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
 '$id': 'https://faion.net/schemas/evolutionary-architecture-fitness-functions.json',
 'title': 'Fitness-function suite spec',
 'type': 'object',
 'required': ['suite_id',
              'system',
              'owner',
              'dependency_graph',
              'results_store',
              'review',
              'functions'],
 'additionalProperties': False,
 'properties': {'__faion_header__': {'type': 'object'},
                'suite_id': {'type': 'string', 'pattern': '^ff-[a-z0-9]+(-[a-z0-9]+)*$'},
                'system': {'type': 'string', 'minLength': 2},
                'owner': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                'dependency_graph': {'type': 'object',
                                     'required': ['layers', 'allowed_edges'],
                                     'additionalProperties': False,
                                     'properties': {'layers': {'type': 'array',
                                                               'minItems': 2,
                                                               'items': {'type': 'string',
                                                                         'minLength': 1}},
                                                    'allowed_edges': {'type': 'array',
                                                                      'minItems': 1,
                                                                      'items': {'type': 'object',
                                                                                'required': ['from',
                                                                                             'to'],
                                                                                'additionalProperties': False,
                                                                                'properties': {'from': {'type': 'string',
                                                                                                        'minLength': 1},
                                                                                               'to': {'type': 'string',
                                                                                                      'minLength': 1}}}}}},
                'results_store': {'type': 'object',
                                  'required': ['location', 'keyed_by', 'retention_days'],
                                  'additionalProperties': False,
                                  'properties': {'location': {'type': 'string', 'minLength': 3},
                                                 'keyed_by': {'type': 'array',
                                                              'const': ['function_id', 'commit']},
                                                 'retention_days': {'type': 'integer',
                                                                    'minimum': 30}}},
                'review': {'type': 'object',
                           'required': ['cadence', 'last_reviewed_at', 'next_review_at'],
                           'additionalProperties': False,
                           'properties': {'cadence': {'type': 'string',
                                                      'enum': ['monthly', 'quarterly']},
                                          'last_reviewed_at': {'type': 'string',
                                                               'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                                          'next_review_at': {'type': 'string',
                                                             'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}}},
                'functions': {'type': 'array',
                              'minItems': 1,
                              'contains': {'type': 'object',
                                           'properties': {'kind': {'const': 'structural'}},
                                           'required': ['kind']},
                              'items': {'type': 'object',
                                        'required': ['id',
                                                     'characteristic',
                                                     'metric',
                                                     'unit',
                                                     'kind',
                                                     'mode',
                                                     'tool',
                                                     'threshold',
                                                     'baseline',
                                                     'threshold_mode',
                                                     'consequence',
                                                     'trigger',
                                                     'scope',
                                                     'owner',
                                                     'consecutive_red_reviews'],
                                        'additionalProperties': False,
                                        'properties': {'id': {'type': 'string',
                                                              'pattern': '^[a-z0-9]+(-[a-z0-9]+)*$'},
                                                       'characteristic': {'type': 'string',
                                                                          'minLength': 3,
                                                                          'pattern': '^(?![Mm]aintainab|[Ss]calab|[Mm]odular|[Cc]lean|[Qq]uality|[Rr]obust|[Ff]lexib|[Rr]eliab).*$'},
                                                       'metric': {'type': 'string', 'minLength': 3},
                                                       'unit': {'type': 'string', 'minLength': 1},
                                                       'kind': {'type': 'string',
                                                                'enum': ['structural',
                                                                         'complexity',
                                                                         'performance',
                                                                         'coverage',
                                                                         'delivery',
                                                                         'security',
                                                                         'operability']},
                                                       'mode': {'type': 'string',
                                                                'enum': ['automated', 'manual']},
                                                       'tool': {'type': 'string', 'minLength': 2},
                                                       'command': {'type': 'string',
                                                                   'minLength': 4},
                                                       'review_cadence': {'type': 'string',
                                                                          'enum': ['monthly',
                                                                                   'quarterly']},
                                                       'threshold': {'type': 'object',
                                                                     'required': ['operator',
                                                                                  'value'],
                                                                     'additionalProperties': False,
                                                                     'properties': {'operator': {'type': 'string',
                                                                                                 'enum': ['<',
                                                                                                          '<=',
                                                                                                          '>',
                                                                                                          '>=',
                                                                                                          '==']},
                                                                                    'value': {'type': 'number'}}},
                                                       'baseline': {'type': 'object',
                                                                    'required': ['value',
                                                                                 'measured_at'],
                                                                    'additionalProperties': False,
                                                                    'properties': {'value': {'type': 'number'},
                                                                                   'measured_at': {'type': 'string',
                                                                                                   'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}}},
                                                       'threshold_mode': {'type': 'string',
                                                                          'enum': ['absolute',
                                                                                   'ratchet']},
                                                       'absolute_from': {'type': 'string',
                                                                         'minLength': 4},
                                                       'consequence': {'type': 'string',
                                                                       'enum': ['blocking',
                                                                                'informational']},
                                                       'trigger': {'type': 'string',
                                                                   'enum': ['triggered',
                                                                            'continual']},
                                                       'scope': {'type': 'string',
                                                                 'enum': ['atomic', 'holistic']},
                                                       'owner': {'type': 'string',
                                                                 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                                                       'consecutive_red_reviews': {'type': 'integer',
                                                                                   'minimum': 0},
                                                       'action': {'type': 'string',
                                                                  'enum': ['fix',
                                                                           'rebaseline',
                                                                           'delete']}},
                                        'allOf': [{'if': {'properties': {'mode': {'const': 'automated'}}},
                                                   'then': {'required': ['command']}},
                                                  {'if': {'properties': {'mode': {'const': 'manual'}}},
                                                   'then': {'required': ['review_cadence']}},
                                                  {'if': {'properties': {'threshold_mode': {'const': 'ratchet'}}},
                                                   'then': {'required': ['absolute_from']}},
                                                  {'if': {'properties': {'scope': {'const': 'holistic'}}},
                                                   'then': {'properties': {'trigger': {'const': 'continual'}}}},
                                                  {'if': {'properties': {'consecutive_red_reviews': {'minimum': 2}}},
                                                   'then': {'required': ['action']}}]}}}}

OK = {'suite_id': 'ff-billing-service',
 'system': 'billing-service',
 'owner': 'arch:alice',
 'dependency_graph': {'layers': ['api', 'domain', 'persistence'],
                      'allowed_edges': [{'from': 'api', 'to': 'domain'},
                                        {'from': 'domain', 'to': 'persistence'}]},
 'results_store': {'location': 'prometheus://ci-metrics/fitness_function_value',
                   'keyed_by': ['function_id', 'commit'],
                   'retention_days': 180},
 'review': {'cadence': 'quarterly',
            'last_reviewed_at': '2026-09-01',
            'next_review_at': '2026-12-01'},
 'functions': [{'id': 'layer-direction',
                'characteristic': 'dependency direction between api, domain and persistence',
                'metric': 'count of imports violating the allowed edges or forming a cycle',
                'unit': 'violations',
                'kind': 'structural',
                'mode': 'automated',
                'tool': 'ArchUnit',
                'command': './gradlew test --tests com.acme.billing.arch.LayerRulesTest',
                'threshold': {'operator': '==', 'value': 0},
                'baseline': {'value': 0, 'measured_at': '2026-09-01'},
                'threshold_mode': 'absolute',
                'consequence': 'blocking',
                'trigger': 'triggered',
                'scope': 'atomic',
                'owner': 'arch:alice',
                'consecutive_red_reviews': 0},
               {'id': 'core-cyclomatic-complexity',
                'characteristic': 'cyclomatic complexity of billing.core functions',
                'metric': 'count of functions with cyclomatic complexity above 10',
                'unit': 'functions',
                'kind': 'complexity',
                'mode': 'automated',
                'tool': 'lizard',
                'command': 'lizard -C 10 -w src/billing/core',
                'threshold': {'operator': '==', 'value': 0},
                'baseline': {'value': 37, 'measured_at': '2026-09-01'},
                'threshold_mode': 'ratchet',
                'absolute_from': '2027-01-01',
                'consequence': 'blocking',
                'trigger': 'triggered',
                'scope': 'atomic',
                'owner': 'swe:bob',
                'consecutive_red_reviews': 0},
               {'id': 'checkout-p95-latency',
                'characteristic': 'p95 latency of POST /checkout at 200 rps',
                'metric': 'http_req_duration p(95)',
                'unit': 'ms',
                'kind': 'performance',
                'mode': 'automated',
                'tool': 'k6',
                'command': 'k6 run --vus 50 --duration 10m perf/checkout.js',
                'threshold': {'operator': '<', 'value': 400},
                'baseline': {'value': 310, 'measured_at': '2026-09-01'},
                'threshold_mode': 'absolute',
                'consequence': 'informational',
                'trigger': 'continual',
                'scope': 'holistic',
                'owner': 'sre:carol',
                'consecutive_red_reviews': 0}]}

BAD = {'suite_id': 'ff-billing-service',
 'system': 'billing-service',
 'owner': 'arch:alice',
 'dependency_graph': {'layers': ['api', 'domain', 'persistence'],
                      'allowed_edges': [{'from': 'api', 'to': 'domain'},
                                        {'from': 'domain', 'to': 'persistence'}]},
 'results_store': {'location': 'prometheus://ci-metrics/fitness_function_value',
                   'keyed_by': ['function_id', 'commit'],
                   'retention_days': 180},
 'review': {'cadence': 'quarterly',
            'last_reviewed_at': '2026-09-01',
            'next_review_at': '2026-12-01'},
 'functions': [{'id': 'maintainability',
                'characteristic': 'maintainability stays high',
                'metric': 'quality score',
                'unit': 'points',
                'kind': 'complexity',
                'mode': 'manual',
                'tool': 'architecture sync',
                'threshold': {'operator': '>', 'value': 8},
                'baseline': {'value': 7, 'measured_at': '2026-09-01'},
                'threshold_mode': 'absolute',
                'consequence': 'blocking',
                'trigger': 'triggered',
                'scope': 'holistic',
                'owner': 'arch:alice',
                'consecutive_red_reviews': 3}]}


# --------------------------------------------------------------------------
# draft-07 subset: required, type, enum, const, pattern, minimum/maximum,
# exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems, items,
# contains, properties, additionalProperties, allOf/anyOf/oneOf/not,
# if/then/else. Enough for every constraint the contract declares.
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
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path or '$'}: fewer than minItems {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{path or '$'}: more than maxItems {schema['maxItems']}")
        if "items" in schema:
            for i, item in enumerate(value):
                _check(schema["items"], item, f"{path}[{i}]", errs)
        if "contains" in schema:
            if not any(_ok(schema["contains"], item) for item in value):
                errs.append(f"{path or '$'}: no element satisfies `contains`")
    if isinstance(value, dict):
        for k in schema.get("required", []):
            if k not in value:
                errs.append(f"{path or '$'}: missing required field {k!r}")
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


_OPS = {"<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b, "==": lambda a, b: a == b}


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    fns = obj.get("functions") or []
    manual = [f for f in fns if f.get("mode") == "manual"]
    if fns and len(manual) * 5 > len(fns):
        errs.append(f"functions: {len(manual)} of {len(fns)} are manual; r-ff-executable-in-ci caps manual at one fifth of the suite")
    for i, f in enumerate(fns):
        th, bl = f.get("threshold") or {}, f.get("baseline") or {}
        op = _OPS.get(th.get("operator"))
        if op and f.get("threshold_mode") == "absolute" and not op(bl.get("value", 0), th.get("value", 0)):
            errs.append(f"functions[{i}]: baseline {bl.get('value')} fails absolute threshold {th.get('operator')} {th.get('value')} today; introduce in ratchet mode with absolute_from (r-ff-threshold-with-baseline-ratchet)")
    horizon = {"monthly": 30, "quarterly": 90}.get((obj.get("review") or {}).get("cadence"), 30)
    days = (obj.get("results_store") or {}).get("retention_days", 0)
    if days < horizon:
        errs.append(f"results_store.retention_days {days} below the {horizon}-day review horizon (r-ff-results-trended)")
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
        prog="validate-evolutionary-architecture-fitness-functions.py",
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
