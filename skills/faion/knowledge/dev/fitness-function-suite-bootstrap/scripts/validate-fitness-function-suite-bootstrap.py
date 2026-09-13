#!/usr/bin/env python3
"""validate-fitness-function-suite-bootstrap.py

Validate a starter fitness-function suite spec against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the fitness-function-suite-bootstrap methodology, plus the
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
 '$id': 'https://faion.net/schemas/fitness-function-suite-bootstrap.json',
 'title': 'Starter fitness-function suite spec',
 'type': 'object',
 'required': ['suite_id',
              'system',
              'owner',
              'dependency_graph',
              'launch_date',
              'weekly_reviews',
              'cadence_after_week_four',
              'functions'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'}},
 'properties': {'__faion_header__': {'type': 'object'},
                'suite_id': {'type': 'string', 'pattern': '^ffsb-[a-z0-9]+(-[a-z0-9]+)*$'},
                'system': {'type': 'string', 'minLength': 2},
                'owner': {'$ref': '#/definitions/handle'},
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
                'launch_date': {'$ref': '#/definitions/date'},
                'weekly_reviews': {'type': 'array',
                                   'minItems': 4,
                                   'maxItems': 4,
                                   'items': {'type': 'object',
                                             'required': ['date',
                                                          'reviewed_by',
                                                          'red_functions',
                                                          'actions'],
                                             'additionalProperties': False,
                                             'properties': {'date': {'$ref': '#/definitions/date'},
                                                            'reviewed_by': {'$ref': '#/definitions/handle'},
                                                            'red_functions': {'type': 'array',
                                                                              'items': {'type': 'string'}},
                                                            'actions': {'type': 'array',
                                                                        'items': {'type': 'string',
                                                                                  'minLength': 4}}}}},
                'cadence_after_week_four': {'type': 'string', 'enum': ['monthly', 'quarterly']},
                'functions': {'type': 'array',
                              'minItems': 5,
                              'maxItems': 8,
                              'allOf': [{'contains': {'properties': {'category': {'const': 'performance'}}}},
                                        {'contains': {'properties': {'category': {'const': 'deployability'}}}},
                                        {'contains': {'properties': {'category': {'const': 'dependency'}}}},
                                        {'contains': {'properties': {'category': {'const': 'complexity'}}}},
                                        {'contains': {'properties': {'category': {'const': 'contract'}}}}],
                              'items': {'type': 'object',
                                        'required': ['id',
                                                     'category',
                                                     'tool',
                                                     'command',
                                                     'threshold',
                                                     'baseline',
                                                     'mode',
                                                     'runs_on',
                                                     'owner',
                                                     'consecutive_red_reviews'],
                                        'additionalProperties': False,
                                        'properties': {'id': {'type': 'string',
                                                              'pattern': '^[a-z0-9]+(-[a-z0-9]+)*$'},
                                                       'category': {'type': 'string',
                                                                    'enum': ['performance',
                                                                             'deployability',
                                                                             'dependency',
                                                                             'complexity',
                                                                             'contract']},
                                                       'tool': {'type': 'string', 'minLength': 2},
                                                       'command': {'type': 'string',
                                                                   'minLength': 4},
                                                       'threshold': {'type': 'object',
                                                                     'required': ['operator',
                                                                                  'value',
                                                                                  'unit'],
                                                                     'additionalProperties': False,
                                                                     'properties': {'operator': {'type': 'string',
                                                                                                 'enum': ['<',
                                                                                                          '<=',
                                                                                                          '>',
                                                                                                          '>=',
                                                                                                          '==']},
                                                                                    'value': {'type': 'number'},
                                                                                    'unit': {'type': 'string',
                                                                                             'minLength': 1}}},
                                                       'baseline': {'type': 'object',
                                                                    'required': ['value',
                                                                                 'measured_at'],
                                                                    'additionalProperties': False,
                                                                    'properties': {'value': {'type': 'number'},
                                                                                   'measured_at': {'$ref': '#/definitions/date'}}},
                                                       'mode': {'type': 'string',
                                                                'enum': ['informational',
                                                                         'ratchet',
                                                                         'blocking']},
                                                       'runs_on': {'type': 'string',
                                                                   'enum': ['pull_request',
                                                                            'post_merge',
                                                                            'nightly']},
                                                       'owner': {'$ref': '#/definitions/handle'},
                                                       'consecutive_red_reviews': {'type': 'integer',
                                                                                   'minimum': 0},
                                                       'action': {'type': 'string',
                                                                  'enum': ['fix',
                                                                           'rebaseline',
                                                                           'remove']},
                                                       'promotion': {'type': 'object',
                                                                     'required': ['green_runs_on_main',
                                                                                  'approved_by',
                                                                                  'review_date',
                                                                                  'promoted_at'],
                                                                     'additionalProperties': False,
                                                                     'properties': {'green_runs_on_main': {'type': 'integer',
                                                                                                           'minimum': 5},
                                                                                    'approved_by': {'$ref': '#/definitions/handle'},
                                                                                    'review_date': {'$ref': '#/definitions/date'},
                                                                                    'promoted_at': {'$ref': '#/definitions/date'}}},
                                                       'endpoint': {'type': 'string',
                                                                    'minLength': 2},
                                                       'load_profile': {'type': 'string',
                                                                        'minLength': 4},
                                                       'runner_kind': {'type': 'string',
                                                                       'enum': ['dedicated-runner',
                                                                                'dedicated-environment']},
                                                       'metric': {'type': 'string',
                                                                  'enum': ['pipeline_duration',
                                                                           'merge_to_production_lead_time']},
                                                       'script_path': {'type': 'string',
                                                                       'minLength': 4},
                                                       'per_function_limit': {'type': 'integer',
                                                                              'minimum': 1,
                                                                              'default': 10},
                                                       'baseline_file': {'type': 'string',
                                                                         'minLength': 4},
                                                       'method': {'type': 'string',
                                                                  'enum': ['pact', 'schema-diff']},
                                                       'consumers': {'type': 'array',
                                                                     'minItems': 1,
                                                                     'items': {'type': 'string',
                                                                               'minLength': 1}},
                                                       'released_schema_ref': {'type': 'string',
                                                                               'minLength': 4}},
                                        'allOf': [{'if': {'properties': {'mode': {'const': 'blocking'}}},
                                                   'then': {'required': ['promotion']}},
                                                  {'if': {'properties': {'consecutive_red_reviews': {'minimum': 2}}},
                                                   'then': {'required': ['action']}},
                                                  {'if': {'properties': {'category': {'const': 'performance'}}},
                                                   'then': {'required': ['endpoint',
                                                                         'load_profile',
                                                                         'runner_kind'],
                                                            'properties': {'runs_on': {'enum': ['post_merge',
                                                                                                'nightly']}}}},
                                                  {'if': {'properties': {'category': {'const': 'deployability'}}},
                                                   'then': {'required': ['metric', 'script_path'],
                                                            'properties': {'threshold': {'properties': {'unit': {'const': 'minutes'}}}}}},
                                                  {'if': {'properties': {'category': {'const': 'dependency'}}},
                                                   'then': {'properties': {'tool': {'enum': ['ArchUnit',
                                                                                             'NetArchTest',
                                                                                             'dependency-cruiser',
                                                                                             'import-linter']},
                                                                           'runs_on': {'const': 'pull_request'}}}},
                                                  {'if': {'properties': {'category': {'const': 'complexity'}}},
                                                   'then': {'required': ['per_function_limit',
                                                                         'baseline_file'],
                                                            'properties': {'tool': {'enum': ['radon',
                                                                                             'lizard',
                                                                                             'eslint-complexity',
                                                                                             'SonarQube']}}}},
                                                  {'if': {'properties': {'category': {'const': 'contract'}}},
                                                   'then': {'required': ['method'],
                                                            'properties': {'tool': {'enum': ['Pact',
                                                                                             'oasdiff',
                                                                                             'openapi-diff',
                                                                                             'buf']}},
                                                            'anyOf': [{'required': ['consumers']},
                                                                      {'required': ['released_schema_ref']}]}}]}}}}

OK = {'suite_id': 'ffsb-orders-api',
 'system': 'orders-api',
 'owner': 'arch:alice',
 'dependency_graph': {'layers': ['http', 'application', 'domain', 'infrastructure'],
                      'allowed_edges': [{'from': 'http', 'to': 'application'},
                                        {'from': 'application', 'to': 'domain'},
                                        {'from': 'application', 'to': 'infrastructure'},
                                        {'from': 'infrastructure', 'to': 'domain'}]},
 'launch_date': '2026-09-07',
 'weekly_reviews': [{'date': '2026-09-14',
                     'reviewed_by': 'arch:alice',
                     'red_functions': ['checkout-p95'],
                     'actions': ['raise k6 VUs to match prod profile v2']},
                    {'date': '2026-09-21',
                     'reviewed_by': 'arch:alice',
                     'red_functions': [],
                     'actions': ['promote layer-direction to blocking']},
                    {'date': '2026-09-28',
                     'reviewed_by': 'arch:alice',
                     'red_functions': [],
                     'actions': []},
                    {'date': '2026-10-05',
                     'reviewed_by': 'arch:alice',
                     'red_functions': [],
                     'actions': ['set cadence to monthly']}],
 'cadence_after_week_four': 'monthly',
 'functions': [{'id': 'checkout-p95',
                'category': 'performance',
                'tool': 'k6',
                'command': 'k6 run --config perf/profiles/checkout-v2.json perf/checkout.js',
                'endpoint': 'POST /v1/checkout',
                'load_profile': 'perf/profiles/checkout-v2.json',
                'runner_kind': 'dedicated-runner',
                'threshold': {'operator': '<', 'value': 400, 'unit': 'ms'},
                'baseline': {'value': 340, 'measured_at': '2026-09-04'},
                'mode': 'informational',
                'runs_on': 'nightly',
                'owner': 'sre:carol',
                'consecutive_red_reviews': 0},
               {'id': 'pipeline-duration',
                'category': 'deployability',
                'tool': 'gh',
                'command': 'python3 ci/pipeline_duration.py --last 20',
                'metric': 'pipeline_duration',
                'script_path': 'ci/pipeline_duration.py',
                'threshold': {'operator': '<=', 'value': 15, 'unit': 'minutes'},
                'baseline': {'value': 12, 'measured_at': '2026-09-04'},
                'mode': 'informational',
                'runs_on': 'post_merge',
                'owner': 'platform:dan',
                'consecutive_red_reviews': 0},
               {'id': 'layer-direction',
                'category': 'dependency',
                'tool': 'import-linter',
                'command': 'lint-imports --config .importlinter',
                'threshold': {'operator': '==', 'value': 0, 'unit': 'violations'},
                'baseline': {'value': 0, 'measured_at': '2026-09-04'},
                'mode': 'blocking',
                'runs_on': 'pull_request',
                'owner': 'arch:alice',
                'consecutive_red_reviews': 0,
                'promotion': {'green_runs_on_main': 9,
                              'approved_by': 'arch:alice',
                              'review_date': '2026-09-21',
                              'promoted_at': '2026-09-22'}},
               {'id': 'cyclomatic-complexity',
                'category': 'complexity',
                'tool': 'lizard',
                'command': 'lizard -C 10 -w src/orders --ignore_warnings 173',
                'per_function_limit': 10,
                'baseline_file': 'quality/complexity-baseline.txt',
                'threshold': {'operator': '==', 'value': 0, 'unit': 'new violations'},
                'baseline': {'value': 173, 'measured_at': '2026-09-04'},
                'mode': 'ratchet',
                'runs_on': 'pull_request',
                'owner': 'swe:bob',
                'consecutive_red_reviews': 0},
               {'id': 'openapi-breaking-diff',
                'category': 'contract',
                'tool': 'oasdiff',
                'command': 'oasdiff breaking https://api.example.com/openapi/v1.12.0.yaml '
                           'openapi.yaml --fail-on ERR',
                'method': 'schema-diff',
                'released_schema_ref': 'https://api.example.com/openapi/v1.12.0.yaml',
                'threshold': {'operator': '==', 'value': 0, 'unit': 'breaking changes'},
                'baseline': {'value': 0, 'measured_at': '2026-09-04'},
                'mode': 'ratchet',
                'runs_on': 'pull_request',
                'owner': 'swe:erin',
                'consecutive_red_reviews': 0}]}

BAD = {'suite_id': 'ffsb-orders-api',
 'system': 'orders-api',
 'owner': 'arch:alice',
 'dependency_graph': {'layers': ['http', 'application', 'domain'],
                      'allowed_edges': [{'from': 'http', 'to': 'application'},
                                        {'from': 'application', 'to': 'domain'}]},
 'launch_date': '2026-09-07',
 'weekly_reviews': [{'date': '2026-09-14',
                     'reviewed_by': 'arch:alice',
                     'red_functions': [],
                     'actions': []},
                    {'date': '2026-09-21',
                     'reviewed_by': 'arch:alice',
                     'red_functions': [],
                     'actions': []},
                    {'date': '2026-09-28',
                     'reviewed_by': 'arch:alice',
                     'red_functions': [],
                     'actions': []},
                    {'date': '2026-10-05',
                     'reviewed_by': 'arch:alice',
                     'red_functions': [],
                     'actions': []}],
 'cadence_after_week_four': 'monthly',
 'functions': [{'id': 'checkout-p95',
                'category': 'performance',
                'tool': 'k6',
                'command': 'k6 run perf/checkout.js',
                'endpoint': 'POST /v1/checkout',
                'load_profile': 'perf/profiles/checkout-v2.json',
                'runner_kind': 'dedicated-runner',
                'threshold': {'operator': '<', 'value': 400, 'unit': 'ms'},
                'baseline': {'value': 340, 'measured_at': '2026-09-04'},
                'mode': 'blocking',
                'runs_on': 'pull_request',
                'owner': 'sre:carol',
                'consecutive_red_reviews': 0},
               {'id': 'layer-direction',
                'category': 'dependency',
                'tool': 'import-linter',
                'command': 'lint-imports --config .importlinter',
                'threshold': {'operator': '==', 'value': 0, 'unit': 'violations'},
                'baseline': {'value': 0, 'measured_at': '2026-09-04'},
                'mode': 'blocking',
                'runs_on': 'pull_request',
                'owner': 'arch:alice',
                'consecutive_red_reviews': 0},
               {'id': 'cyclomatic-complexity',
                'category': 'complexity',
                'tool': 'lizard',
                'command': 'lizard -C 10 -w src/orders',
                'per_function_limit': 10,
                'threshold': {'operator': '==', 'value': 0, 'unit': 'violations'},
                'baseline': {'value': 173, 'measured_at': '2026-09-04'},
                'mode': 'blocking',
                'runs_on': 'pull_request',
                'owner': 'swe:bob',
                'consecutive_red_reviews': 0}]}


# --------------------------------------------------------------------------
# draft-07 subset: required, type, enum, const, pattern, minimum/maximum,
# exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems, items,
# contains, properties, additionalProperties, allOf/anyOf/oneOf/not,
# if/then/else, local $ref (#/definitions/...). Enough for every constraint the contract declares.
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
    for i, f in enumerate(obj.get("functions") or []):
        th, bl = f.get("threshold") or {}, f.get("baseline") or {}
        op = _OPS.get(th.get("operator"))
        if op and f.get("mode") == "blocking" and not op(bl.get("value", 0), th.get("value", 0)):
            errs.append(f"functions[{i}]: blocking while baseline {bl.get('value')} fails threshold {th.get('operator')} {th.get('value')}; run informational or ratchet first (r-ffsb-ratchet-first-then-block)")
        if f.get("mode") == "blocking":
            promo = f.get("promotion") or {}
            if promo.get("promoted_at", "") < promo.get("review_date", ""):
                errs.append(f"functions[{i}]: promoted_at precedes the review that approved it (r-ffsb-ratchet-first-then-block)")
    launch = obj.get("launch_date", "")
    for j, r in enumerate(obj.get("weekly_reviews") or []):
        if r.get("date", "") <= launch:
            errs.append(f"weekly_reviews[{j}]: dated on or before launch_date (r-ffsb-owner-and-weekly-review)")
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
        prog="validate-fitness-function-suite-bootstrap.py",
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
