#!/usr/bin/env python3
"""validate-rfc-template-product-dev-team.py

Validate a product-dev RFC against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the rfc-template-product-dev-team methodology, plus the
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
 '$id': 'https://faion.net/schemas/rfc-template-product-dev-team.json',
 'title': 'Product-dev RFC',
 'type': 'object',
 'required': ['rfc', 'owner', 'inputs', 'decision', 'supersession', 'evidence', 'review'],
 'additionalProperties': False,
 'definitions': {'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'url': {'type': 'string', 'pattern': '^https://'},
                 'text': {'type': 'string', 'minLength': 8}},
 'properties': {'__faion_header__': {'type': 'object'},
                'rfc': {'type': 'object',
                        'required': ['id', 'title', 'author', 'shared_on'],
                        'additionalProperties': False,
                        'properties': {'id': {'type': 'string', 'pattern': '^RFC-[0-9]{3,}$'},
                                       'title': {'type': 'string', 'minLength': 8},
                                       'author': {'$ref': '#/definitions/handle'},
                                       'shared_on': {'$ref': '#/definitions/date'}}},
                'owner': {'$ref': '#/definitions/handle'},
                'inputs': {'type': 'array',
                           'minItems': 9,
                           'allOf': [{'contains': {'properties': {'name': {'const': 'problem'}}}},
                                     {'contains': {'properties': {'name': {'const': 'options'}}}},
                                     {'contains': {'properties': {'name': {'const': 'blast_radius'}}}},
                                     {'contains': {'properties': {'name': {'const': 'rollback'}}}},
                                     {'contains': {'properties': {'name': {'const': 'milestones'}}}},
                                     {'contains': {'properties': {'name': {'const': 'status'}}}},
                                     {'contains': {'properties': {'name': {'const': 'decided_on'}}}},
                                     {'contains': {'properties': {'name': {'const': 'reviewers'}}}},
                                     {'contains': {'properties': {'name': {'const': 'comment_deadline'}}}}],
                           'items': {'type': 'object',
                                     'required': ['name', 'value'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'type': 'string',
                                                             'enum': ['problem',
                                                                      'options',
                                                                      'blast_radius',
                                                                      'rollback',
                                                                      'milestones',
                                                                      'status',
                                                                      'decided_on',
                                                                      'reviewers',
                                                                      'comment_deadline']},
                                                    'value': {}},
                                     'allOf': [{'if': {'properties': {'name': {'const': 'problem'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['metric',
                                                                                               'current_value',
                                                                                               'target_value',
                                                                                               'by_date',
                                                                                               'statement'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'metric': {'$ref': '#/definitions/text'},
                                                                                                 'current_value': {'type': 'string',
                                                                                                                   'minLength': 1,
                                                                                                                   'pattern': '[0-9]'},
                                                                                                 'target_value': {'type': 'string',
                                                                                                                  'minLength': 1,
                                                                                                                  'pattern': '[0-9]'},
                                                                                                 'by_date': {'$ref': '#/definitions/date'},
                                                                                                 'statement': {'type': 'string',
                                                                                                               'minLength': 20,
                                                                                                               'pattern': '^(?![\\s\\S]*([Mm]igrate '
                                                                                                                          'to|[Aa]dopt '
                                                                                                                          '|[Ss]witch '
                                                                                                                          'to|[Mm]ove '
                                                                                                                          'to|[Nn]eed '
                                                                                                                          'to '
                                                                                                                          'use|[Rr]ewrite '
                                                                                                                          'in))'}}}}}},
                                               {'if': {'properties': {'name': {'const': 'options'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'minItems': 2,
                                                                                  'contains': {'properties': {'chosen': {'const': True}}},
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['name',
                                                                                                         'chosen'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'name': {'type': 'string',
                                                                                                                    'minLength': 4},
                                                                                                           'chosen': {'type': 'boolean'},
                                                                                                           'rejection_reason': {'$ref': '#/definitions/text'}},
                                                                                            'if': {'properties': {'chosen': {'const': False}}},
                                                                                            'then': {'required': ['rejection_reason']}}}}}},
                                               {'if': {'properties': {'name': {'const': 'blast_radius'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['items',
                                                                                               'schema_change',
                                                                                               'public_api_change',
                                                                                               'data_backfill',
                                                                                               'third_party_change'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'items': {'type': 'array',
                                                                                                           'minItems': 1,
                                                                                                           'items': {'type': 'object',
                                                                                                                     'required': ['kind',
                                                                                                                                  'name',
                                                                                                                                  'owner'],
                                                                                                                     'additionalProperties': False,
                                                                                                                     'properties': {'kind': {'type': 'string',
                                                                                                                                             'enum': ['service',
                                                                                                                                                      'data-store',
                                                                                                                                                      'api',
                                                                                                                                                      'scheduled-job',
                                                                                                                                                      'user-segment']},
                                                                                                                                    'name': {'type': 'string',
                                                                                                                                             'minLength': 2},
                                                                                                                                    'owner': {'$ref': '#/definitions/handle'},
                                                                                                                                    'count': {'type': 'string',
                                                                                                                                              'minLength': 1,
                                                                                                                                              'pattern': '[0-9]'}},
                                                                                                                     'if': {'properties': {'kind': {'enum': ['api',
                                                                                                                                                             'user-segment']}}},
                                                                                                                     'then': {'required': ['count']}}},
                                                                                                 'schema_change': {'type': 'boolean'},
                                                                                                 'public_api_change': {'type': 'boolean'},
                                                                                                 'data_backfill': {'type': 'boolean'},
                                                                                                 'third_party_change': {'type': 'boolean'}}}}}},
                                               {'if': {'properties': {'name': {'const': 'rollback'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['mechanism',
                                                                                               'execute_minutes',
                                                                                               'executor',
                                                                                               'staging_run',
                                                                                               'points_of_no_return'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'mechanism': {'type': 'string',
                                                                                                               'enum': ['feature-flag-off',
                                                                                                                        'revert-pr',
                                                                                                                        'down-migration',
                                                                                                                        'config-revert']},
                                                                                                 'execute_minutes': {'type': 'number',
                                                                                                                     'minimum': 0},
                                                                                                 'executor': {'$ref': '#/definitions/handle'},
                                                                                                 'staging_run': {'type': 'object',
                                                                                                                 'required': ['exercised'],
                                                                                                                 'additionalProperties': False,
                                                                                                                 'properties': {'exercised': {'type': 'boolean'},
                                                                                                                                'url': {'$ref': '#/definitions/url'},
                                                                                                                                'reason': {'$ref': '#/definitions/text'}},
                                                                                                                 'if': {'properties': {'exercised': {'const': True}}},
                                                                                                                 'then': {'required': ['url']},
                                                                                                                 'else': {'required': ['reason']}},
                                                                                                 'points_of_no_return': {'type': 'array',
                                                                                                                         'items': {'type': 'object',
                                                                                                                                   'required': ['step',
                                                                                                                                                'pre_check'],
                                                                                                                                   'additionalProperties': False,
                                                                                                                                   'properties': {'step': {'$ref': '#/definitions/text'},
                                                                                                                                                  'pre_check': {'$ref': '#/definitions/text'}}}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'milestones'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'minItems': 2,
                                                                                  'contains': {'properties': {'ship': {'const': True}}},
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['date',
                                                                                                         'increment',
                                                                                                         'ship'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'date': {'$ref': '#/definitions/date'},
                                                                                                           'increment': {'type': 'string',
                                                                                                                         'minLength': 12,
                                                                                                                         'pattern': '^(?!(design|implementation|build|testing|test|launch|done|qa)$)'},
                                                                                                           'ship': {'type': 'boolean'}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'status'}}},
                                                'then': {'properties': {'value': {'type': 'string',
                                                                                  'enum': ['proposed',
                                                                                           'accepted',
                                                                                           'rejected',
                                                                                           'superseded']}}}},
                                               {'if': {'properties': {'name': {'const': 'decided_on'}}},
                                                'then': {'properties': {'value': {'$ref': '#/definitions/date'}}}},
                                               {'if': {'properties': {'name': {'const': 'reviewers'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'minItems': 1,
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['handle',
                                                                                                         'commented'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'handle': {'type': 'string',
                                                                                                                      'pattern': '^(?!(team|channel|everyone|all)[:@])[a-z-]+:[a-z0-9._-]+$'},
                                                                                                           'commented': {'type': 'boolean'}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'comment_deadline'}}},
                                                'then': {'properties': {'value': {'$ref': '#/definitions/date'}}}}]}},
                'decision': {'type': 'string', 'minLength': 20, 'pattern': '^[^.!?]+[.]?$'},
                'supersession': {'type': 'object',
                                 'required': ['superseded_by', 'supersedes'],
                                 'additionalProperties': False,
                                 'properties': {'superseded_by': {'type': ['string', 'null'],
                                                                  'pattern': '^https://'},
                                                'supersedes': {'type': ['string', 'null'],
                                                               'pattern': '^https://'}}},
                'evidence': {'type': 'array',
                             'minItems': 1,
                             'items': {'$ref': '#/definitions/url'}},
                'review': {'type': 'object',
                           'required': ['next_review_at', 'outcome'],
                           'additionalProperties': False,
                           'properties': {'next_review_at': {'$ref': '#/definitions/date'},
                                          'outcome': {'oneOf': [{'type': 'null'},
                                                                {'type': 'object',
                                                                 'required': ['remeasured_value',
                                                                              'same_method',
                                                                              'result',
                                                                              'url',
                                                                              'reviewed_on'],
                                                                 'additionalProperties': False,
                                                                 'properties': {'remeasured_value': {'type': 'string',
                                                                                                     'minLength': 1,
                                                                                                     'pattern': '[0-9]'},
                                                                                'same_method': {'type': 'boolean',
                                                                                                'const': True},
                                                                                'result': {'type': 'string',
                                                                                           'enum': ['met',
                                                                                                    'partially-met',
                                                                                                    'not-met']},
                                                                                'url': {'$ref': '#/definitions/url'},
                                                                                'reviewed_on': {'$ref': '#/definitions/date'}}}]}}}}}

OK = {'rfc': {'id': 'RFC-118',
         'title': 'Checkout p95 latency under 1.2 s',
         'author': 'swe:alice',
         'shared_on': '2026-05-29'},
 'owner': 'swe:alice',
 'inputs': [{'name': 'problem',
             'value': {'metric': 'checkout p95 latency (Grafana checkout-overview, 7-day window)',
                       'current_value': '2.4 s',
                       'target_value': '1.2 s',
                       'by_date': '2026-07-15',
                       'statement': 'Checkout p95 is 2.4 s over the last 7 days against a 1.2 s '
                                    'target; 18 percent of mobile sessions abandon on the payment '
                                    'step, and the abandonment correlates with latency above 2 '
                                    's.'}},
            {'name': 'options',
             'value': [{'name': 'precompute cart totals into the orders table (checkout_v2 behind '
                                'a flag)',
                        'chosen': True},
                       {'name': 'cache the pricing service responses in Redis for 60 s',
                        'chosen': False,
                        'rejection_reason': 'cuts p95 to about 1.8 s in the spike test, short of '
                                            'the 1.2 s target; stale prices during promotions'},
                       {'name': 'do nothing / keep current behaviour',
                        'chosen': False,
                        'rejection_reason': 'abandonment cost estimated at 40k per month at '
                                            'current traffic'}]},
            {'name': 'blast_radius',
             'value': {'items': [{'kind': 'service',
                                  'name': 'checkout-service',
                                  'owner': 'swe:alice'},
                                 {'kind': 'data-store',
                                  'name': 'orders table (shared with billing-job)',
                                  'owner': 'swe:olena'},
                                 {'kind': 'api',
                                  'name': 'mobile checkout API v3',
                                  'owner': 'mobile:dmytro',
                                  'count': '18 percent of traffic, 2 API consumers'},
                                 {'kind': 'scheduled-job',
                                  'name': 'billing-job nightly reconciliation',
                                  'owner': 'swe:olena'},
                                 {'kind': 'user-segment',
                                  'name': 'mobile checkout users',
                                  'owner': 'product:maria',
                                  'count': '18 percent of sessions'}],
                       'schema_change': True,
                       'public_api_change': False,
                       'data_backfill': True,
                       'third_party_change': False}},
            {'name': 'rollback',
             'value': {'mechanism': 'feature-flag-off',
                       'execute_minutes': 1,
                       'executor': 'oncall:checkout',
                       'staging_run': {'exercised': True,
                                       'url': 'https://ci.example.com/runs/88412'},
                       'points_of_no_return': [{'step': 'backfill of orders.total_cents for '
                                                        'historical rows',
                                                'pre_check': 'row count of orders with NULL '
                                                             'total_cents equals the count from '
                                                             'the dry run within 0.1 percent'}]}},
            {'name': 'milestones',
             'value': [{'date': '2026-06-12',
                        'increment': 'orders.total_cents column added and backfilled in staging; '
                                     'query proves parity with computed totals',
                        'ship': False},
                       {'date': '2026-06-26',
                        'increment': 'checkout_v2 flag on for internal users; p95 visible on the '
                                     'dashboard',
                        'ship': False},
                       {'date': '2026-07-03',
                        'increment': 'flag on for 100 percent of mobile traffic; abandonment panel '
                                     'updated',
                        'ship': True}]},
            {'name': 'status', 'value': 'accepted'},
            {'name': 'decided_on', 'value': '2026-06-05'},
            {'name': 'reviewers',
             'value': [{'handle': 'swe:olena', 'commented': True},
                       {'handle': 'mobile:dmytro', 'commented': True},
                       {'handle': 'product:maria', 'commented': False}]},
            {'name': 'comment_deadline', 'value': '2026-06-04'}],
 'decision': 'Precompute cart totals into the orders table behind the checkout_v2 flag and ship to '
             'mobile by 2026-07-03.',
 'supersession': {'superseded_by': None, 'supersedes': None},
 'evidence': ['https://grafana.example.com/d/checkout-overview?from=now-7d&to=now',
              'https://ci.example.com/runs/88412',
              'https://github.com/acme/checkout/pull/2210'],
 'review': {'next_review_at': '2026-08-07',
            'outcome': {'remeasured_value': '1.1 s',
                        'same_method': True,
                        'result': 'met',
                        'url': 'https://grafana.example.com/d/checkout-overview?from=1785024000000&to=1785628800000',
                        'reviewed_on': '2026-08-06'}}}

BAD = {'rfc': {'id': 'RFC-119',
         'title': 'Move checkout to GraphQL',
         'author': 'swe:bob',
         'shared_on': '2026-05-29'},
 'owner': 'swe:bob',
 'inputs': [{'name': 'problem',
             'value': {'metric': 'checkout latency',
                       'current_value': 'slow',
                       'target_value': 'fast',
                       'by_date': '2026-07-15',
                       'statement': 'We need to migrate to GraphQL so the mobile checkout stops '
                                    'being slow.'}},
            {'name': 'options', 'value': [{'name': 'move checkout to GraphQL', 'chosen': True}]},
            {'name': 'blast_radius',
             'value': {'items': [{'kind': 'service',
                                  'name': 'checkout-service',
                                  'owner': 'swe:bob'}],
                       'schema_change': True,
                       'public_api_change': True,
                       'data_backfill': True,
                       'third_party_change': False}},
            {'name': 'rollback',
             'value': {'mechanism': 'revert-pr',
                       'execute_minutes': 5,
                       'executor': 'swe:bob',
                       'staging_run': {'exercised': False, 'reason': 'revert is trivial'},
                       'points_of_no_return': []}},
            {'name': 'milestones',
             'value': [{'date': '2026-09-30', 'increment': 'launch', 'ship': True}]},
            {'name': 'status', 'value': 'accepted'},
            {'name': 'decided_on', 'value': '2026-05-31'},
            {'name': 'reviewers', 'value': [{'handle': 'team:backend', 'commented': False}]},
            {'name': 'comment_deadline', 'value': '2026-05-30'}],
 'decision': 'Move to GraphQL. It will be faster and cleaner.',
 'supersession': {'superseded_by': None, 'supersedes': None},
 'evidence': ['https://notion.example.com/rfc-119'],
 'review': {'next_review_at': '2027-01-15', 'outcome': None}}


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


from datetime import date, timedelta


def _d(s):
    try:
        return date.fromisoformat(str(s))
    except (ValueError, TypeError):
        return None


def _working_days(a: date, b: date) -> int:
    n, cur = 0, a
    while cur < b:
        cur += timedelta(days=1)
        if cur.weekday() < 5:
            n += 1
    return n


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    inputs = {i.get("name"): i.get("value") for i in obj.get("inputs") or [] if isinstance(i, dict)}
    opts = inputs.get("options") or []
    if sum(1 for o in opts if o.get("chosen")) != 1:
        errs.append("options: exactly one option must be chosen (r-two-options-with-rejection-reasons)")
    real_alt = [o for o in opts if not o.get("chosen") and not re.search(r"do nothing|keep current", o.get("name", ""), re.I)]
    if not real_alt:
        errs.append("options: no real alternative besides the chosen one and do-nothing (r-two-options-with-rejection-reasons)")
    chosen = next((o.get("name", "") for o in opts if o.get("chosen")), "")
    dec = obj.get("decision", "")
    if chosen and not any(w in dec.lower() for w in chosen.lower().split()[:3]):
        errs.append("decision does not name the chosen option (r-decision-has-status-and-supersession)")
    br = inputs.get("blast_radius") or {}
    reviewers = {r.get("handle") for r in inputs.get("reviewers") or []}
    author = (obj.get("rfc") or {}).get("author")
    for it in br.get("items") or []:
        if it.get("owner") != author and it.get("owner") not in reviewers:
            errs.append(f"blast_radius owner {it.get('owner')} of {it.get('name')} is not in reviewers (r-reviewers-named-with-comment-deadline)")
    rb = inputs.get("rollback") or {}
    if (br.get("data_backfill") or br.get("schema_change")) and not rb.get("points_of_no_return"):
        errs.append("data_backfill or schema_change is true with no points_of_no_return (r-rollback-named-timed-and-tested)")
    ms = inputs.get("milestones") or []
    dates = [d for d in (_d(m.get("date")) for m in ms) if d]
    if dates and (max(dates) - min(dates)).days > 42:
        errs.append(f"milestones span {(max(dates) - min(dates)).days} days, above 42 (r-scope-fits-one-cycle-with-milestones)")
    if ms and not ms[-1].get("ship"):
        errs.append("last milestone is not the ship milestone (r-scope-fits-one-cycle-with-milestones)")
    shared, deadline = _d((obj.get("rfc") or {}).get("shared_on")), _d(inputs.get("comment_deadline"))
    if shared and deadline and _working_days(shared, deadline) < 3:
        errs.append("comment_deadline is fewer than 3 working days after shared_on (r-reviewers-named-with-comment-deadline)")
    decided = _d(inputs.get("decided_on"))
    if inputs.get("status") == "accepted":
        all_commented = all(r.get("commented") for r in inputs.get("reviewers") or [])
        if not all_commented and decided and deadline and decided <= deadline:
            errs.append("status accepted before every reviewer commented and before comment_deadline passed (r-reviewers-named-with-comment-deadline)")
    sup = obj.get("supersession") or {}
    ev = obj.get("evidence") or []
    if inputs.get("status") == "superseded" and not sup.get("superseded_by"):
        errs.append("status superseded with supersession.superseded_by null (r-decision-has-status-and-supersession)")
    for k in ("superseded_by", "supersedes"):
        if sup.get(k) and sup[k] not in ev:
            errs.append(f"supersession.{k} is not in evidence[] (r-decision-has-status-and-supersession)")
    ship = next((_d(m.get("date")) for m in ms if m.get("ship")), None)
    nxt = _d((obj.get("review") or {}).get("next_review_at"))
    if ship and nxt and (nxt - ship).days > 42:
        errs.append(f"review.next_review_at is {(nxt - ship).days} days after ship, above 42 (r-outcome-review-remeasures-problem-metric)")
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
        prog="validate-rfc-template-product-dev-team.py",
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
