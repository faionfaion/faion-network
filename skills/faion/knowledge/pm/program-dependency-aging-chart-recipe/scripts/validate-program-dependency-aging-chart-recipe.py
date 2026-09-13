#!/usr/bin/env python3
"""validate-program-dependency-aging-chart-recipe.py

Validate the artefact produced by the program-dependency-aging-chart-recipe methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/program-dependency-aging-chart-recipe.json',
 'title': 'Program dependency aging chart',
 'type': 'object',
 'required': ['program',
              'owner',
              'chart_date',
              'checkpoint_weekday',
              'tracker_query',
              'extracted_at',
              'age_bands',
              'bands_adopted_on',
              'edges',
              'action_table',
              'resolved_log',
              'sle'],
 'additionalProperties': False,
 'definitions': {'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'timestamp': {'type': 'string',
                               'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2})?(Z|[+-][0-9]{2}:[0-9]{2})$'},
                 'link_id': {'type': 'string', 'pattern': '^[A-Z][A-Z0-9]+-[0-9]+$'}},
 'properties': {'__faion_header__': {'type': 'object'},
                'program': {'type': 'string', 'minLength': 2},
                'owner': {'$ref': '#/definitions/handle'},
                'chart_date': {'$ref': '#/definitions/date'},
                'checkpoint_weekday': {'type': 'string',
                                       'enum': ['Monday',
                                                'Tuesday',
                                                'Wednesday',
                                                'Thursday',
                                                'Friday',
                                                'Saturday',
                                                'Sunday']},
                'tracker_query': {'type': 'string', 'minLength': 10},
                'extracted_at': {'$ref': '#/definitions/timestamp'},
                'chart_image': {'type': 'string', 'minLength': 3},
                'age_bands': {'type': 'array',
                              'minItems': 3,
                              'items': {'type': 'object',
                                        'required': ['label', 'min_days', 'max_days'],
                                        'additionalProperties': False,
                                        'properties': {'label': {'type': 'string', 'minLength': 1},
                                                       'min_days': {'type': 'integer',
                                                                    'minimum': 0},
                                                       'max_days': {'type': ['integer', 'null'],
                                                                    'minimum': 1}}}},
                'bands_adopted_on': {'$ref': '#/definitions/date'},
                'edges': {'type': 'array',
                          'items': {'type': 'object',
                                    'required': ['link_id',
                                                 'producer_team',
                                                 'consumer_team',
                                                 'dependency_type',
                                                 'opened_at',
                                                 'needed_by',
                                                 'blocked_task_count',
                                                 'age_days',
                                                 'band',
                                                 'slack_days'],
                                    'additionalProperties': False,
                                    'properties': {'link_id': {'$ref': '#/definitions/link_id'},
                                                   'producer_team': {'type': 'string',
                                                                     'minLength': 2},
                                                   'consumer_team': {'type': 'string',
                                                                     'minLength': 2},
                                                   'dependency_type': {'type': 'string',
                                                                       'enum': ['api-contract',
                                                                                'shared-component',
                                                                                'data-feed',
                                                                                'infrastructure',
                                                                                'review-approval',
                                                                                'environment',
                                                                                'other']},
                                                   'opened_at': {'$ref': '#/definitions/date'},
                                                   'needed_by': {'anyOf': [{'$ref': '#/definitions/date'},
                                                                           {'type': 'null'}]},
                                                   'blocked_task_count': {'type': 'integer',
                                                                          'minimum': 0},
                                                   'age_days': {'type': 'integer', 'minimum': 0},
                                                   'band': {'type': 'string', 'minLength': 1},
                                                   'slack_days': {'type': ['integer', 'null']},
                                                   'superseded_from': {'$ref': '#/definitions/link_id'},
                                                   'action': {'type': 'object',
                                                              'required': ['owner',
                                                                           'due_date',
                                                                           'text'],
                                                              'additionalProperties': False,
                                                              'properties': {'owner': {'$ref': '#/definitions/handle'},
                                                                             'due_date': {'$ref': '#/definitions/date'},
                                                                             'text': {'type': 'string',
                                                                                      'minLength': 12,
                                                                                      'pattern': '^(?![Ww]aiting '
                                                                                                 '(on|for))'}}},
                                                   'rebaseline': {'type': 'object',
                                                                  'required': ['decision',
                                                                               'decided_by',
                                                                               'decided_on'],
                                                                  'additionalProperties': False,
                                                                  'properties': {'decision': {'type': 'string',
                                                                                              'enum': ['move-milestone',
                                                                                                       'cut-scope',
                                                                                                       'swap-producer']},
                                                                                 'decided_by': {'$ref': '#/definitions/handle'},
                                                                                 'decided_on': {'$ref': '#/definitions/date'},
                                                                                 'note': {'type': 'string'}}}}}},
                'action_table': {'type': 'array',
                                 'items': {'$ref': '#/definitions/link_id'},
                                 'uniqueItems': True},
                'resolved_log': {'type': 'array',
                                 'items': {'type': 'object',
                                           'required': ['link_id',
                                                        'opened_at',
                                                        'resolved_on',
                                                        'age_days',
                                                        'outcome',
                                                        'needed_by'],
                                           'additionalProperties': False,
                                           'properties': {'link_id': {'$ref': '#/definitions/link_id'},
                                                          'opened_at': {'$ref': '#/definitions/date'},
                                                          'resolved_on': {'$ref': '#/definitions/date'},
                                                          'age_days': {'type': 'integer',
                                                                       'minimum': 0},
                                                          'outcome': {'type': 'string',
                                                                      'enum': ['delivered',
                                                                               'not-needed']},
                                                          'needed_by': {'anyOf': [{'$ref': '#/definitions/date'},
                                                                                  {'type': 'null'}]}},
                                           'if': {'properties': {'outcome': {'const': 'not-needed'}}},
                                           'then': {'properties': {'needed_by': {'$ref': '#/definitions/date'}}}}},
                'sle': {'type': 'object',
                        'required': ['resolved_count_12w', 'status'],
                        'additionalProperties': False,
                        'properties': {'resolved_count_12w': {'type': 'integer', 'minimum': 0},
                                       'status': {'type': 'string',
                                                  'enum': ['line', 'insufficient-data']},
                                       'p85_days': {'type': 'integer', 'minimum': 0}},
                        'if': {'properties': {'status': {'const': 'line'}}},
                        'then': {'required': ['resolved_count_12w', 'status', 'p85_days'],
                                 'properties': {'resolved_count_12w': {'minimum': 10}}},
                        'else': {'properties': {'resolved_count_12w': {'maximum': 9}},
                                 'not': {'required': ['p85_days']}}}}}

OK = {'program': 'checkout-replatform',
 'owner': 'program-pm:olena',
 'chart_date': '2026-09-07',
 'checkpoint_weekday': 'Monday',
 'tracker_query': 'project in (PAY, PLAT, WEB, DATA, SEC) AND issueLinkType = "is blocked by" AND '
                  'resolution = Unresolved',
 'extracted_at': '2026-09-07T07:30:00Z',
 'chart_image': 'charts/checkout-replatform-2026-09-07.png',
 'age_bands': [{'label': '0-7', 'min_days': 0, 'max_days': 7},
               {'label': '8-14', 'min_days': 8, 'max_days': 14},
               {'label': '15-28', 'min_days': 15, 'max_days': 28},
               {'label': 'over 28', 'min_days': 29, 'max_days': None}],
 'bands_adopted_on': '2026-05-04',
 'edges': [{'link_id': 'PLAT-118',
            'producer_team': 'platform',
            'consumer_team': 'payments',
            'dependency_type': 'api-contract',
            'opened_at': '2026-07-21',
            'needed_by': '2026-09-30',
            'blocked_task_count': 6,
            'age_days': 48,
            'band': 'over 28',
            'slack_days': 23,
            'action': {'owner': 'platform-lead:marko',
                       'due_date': '2026-09-11',
                       'text': 'Publish the tokenisation API contract v2 as OpenAPI and freeze it; '
                               'payments builds against the stub from 2026-09-12.'},
            'rebaseline': {'decision': 'cut-scope',
                           'decided_by': 'program-pm:olena',
                           'decided_on': '2026-09-07',
                           'note': 'Drop 3-D Secure fallback from milestone M6; it moves to M7.'}},
           {'link_id': 'WEB-402',
            'producer_team': 'web',
            'consumer_team': 'payments',
            'dependency_type': 'shared-component',
            'opened_at': '2026-08-20',
            'needed_by': '2026-09-04',
            'blocked_task_count': 2,
            'age_days': 18,
            'band': '15-28',
            'slack_days': -3,
            'action': {'owner': 'web-lead:ira',
                       'due_date': '2026-09-09',
                       'text': 'Ship the address form component behind a flag to the payments '
                               'sandbox; M5 acceptance re-run on 2026-09-10.'}},
           {'link_id': 'SEC-9',
            'producer_team': 'security',
            'consumer_team': 'payments',
            'dependency_type': 'review-approval',
            'opened_at': '2026-08-12',
            'needed_by': '2026-09-25',
            'blocked_task_count': 1,
            'age_days': 26,
            'band': '15-28',
            'slack_days': 18,
            'superseded_from': 'SEC-7',
            'action': {'owner': 'security-lead:taras',
                       'due_date': '2026-09-14',
                       'text': 'Complete the PCI scope review of the card vault design; findings '
                               'back to payments in writing.'}},
           {'link_id': 'DATA-77',
            'producer_team': 'data',
            'consumer_team': 'web',
            'dependency_type': 'data-feed',
            'opened_at': '2026-08-26',
            'needed_by': '2026-10-15',
            'blocked_task_count': 1,
            'age_days': 12,
            'band': '8-14',
            'slack_days': 38,
            'action': {'owner': 'data-lead:sofia',
                       'due_date': '2026-09-18',
                       'text': "Expose the order-events topic to the web team's staging consumer "
                               'with the agreed schema v3.'}},
           {'link_id': 'PLAT-131',
            'producer_team': 'platform',
            'consumer_team': 'web',
            'dependency_type': 'environment',
            'opened_at': '2026-09-03',
            'needed_by': None,
            'blocked_task_count': 3,
            'age_days': 4,
            'band': '0-7',
            'slack_days': None}],
 'action_table': ['WEB-402', 'PLAT-118', 'SEC-9', 'DATA-77', 'PLAT-131'],
 'resolved_log': [{'link_id': 'PLAT-101',
                   'opened_at': '2026-06-08',
                   'resolved_on': '2026-06-17',
                   'age_days': 9,
                   'outcome': 'delivered',
                   'needed_by': '2026-06-20'},
                  {'link_id': 'WEB-377',
                   'opened_at': '2026-06-10',
                   'resolved_on': '2026-06-22',
                   'age_days': 12,
                   'outcome': 'delivered',
                   'needed_by': '2026-06-30'},
                  {'link_id': 'DATA-60',
                   'opened_at': '2026-06-12',
                   'resolved_on': '2026-06-26',
                   'age_days': 14,
                   'outcome': 'not-needed',
                   'needed_by': '2026-07-10'},
                  {'link_id': 'PLAT-104',
                   'opened_at': '2026-06-15',
                   'resolved_on': '2026-07-02',
                   'age_days': 17,
                   'outcome': 'delivered',
                   'needed_by': '2026-07-03'},
                  {'link_id': 'SEC-4',
                   'opened_at': '2026-06-20',
                   'resolved_on': '2026-07-09',
                   'age_days': 19,
                   'outcome': 'delivered',
                   'needed_by': '2026-07-15'},
                  {'link_id': 'WEB-381',
                   'opened_at': '2026-06-25',
                   'resolved_on': '2026-07-16',
                   'age_days': 21,
                   'outcome': 'delivered',
                   'needed_by': None},
                  {'link_id': 'PLAT-109',
                   'opened_at': '2026-07-01',
                   'resolved_on': '2026-07-23',
                   'age_days': 22,
                   'outcome': 'delivered',
                   'needed_by': '2026-07-24'},
                  {'link_id': 'DATA-66',
                   'opened_at': '2026-07-06',
                   'resolved_on': '2026-07-31',
                   'age_days': 25,
                   'outcome': 'delivered',
                   'needed_by': '2026-08-01'},
                  {'link_id': 'WEB-390',
                   'opened_at': '2026-07-10',
                   'resolved_on': '2026-08-06',
                   'age_days': 27,
                   'outcome': 'delivered',
                   'needed_by': '2026-08-07'},
                  {'link_id': 'PLAT-112',
                   'opened_at': '2026-07-14',
                   'resolved_on': '2026-08-13',
                   'age_days': 30,
                   'outcome': 'delivered',
                   'needed_by': '2026-08-10'},
                  {'link_id': 'SEC-6',
                   'opened_at': '2026-07-20',
                   'resolved_on': '2026-08-22',
                   'age_days': 33,
                   'outcome': 'delivered',
                   'needed_by': '2026-08-14'},
                  {'link_id': 'DATA-71',
                   'opened_at': '2026-07-22',
                   'resolved_on': '2026-09-01',
                   'age_days': 41,
                   'outcome': 'delivered',
                   'needed_by': '2026-08-21'}],
 'sle': {'resolved_count_12w': 12, 'status': 'line', 'p85_days': 33}}

BAD = {'program': 'checkout-replatform',
 'owner': 'program-pm:olena',
 'chart_date': '2026-09-07',
 'checkpoint_weekday': 'Monday',
 'tracker_query': 'project in (PAY, PLAT, WEB, DATA, SEC) AND issueLinkType = "is blocked by" AND '
                  'resolution = Unresolved',
 'extracted_at': '2026-08-24T07:30:00Z',
 'age_bands': [{'label': '0-7', 'min_days': 0, 'max_days': 7},
               {'label': '8-14', 'min_days': 8, 'max_days': 14},
               {'label': '15-45', 'min_days': 15, 'max_days': 45},
               {'label': 'over 45', 'min_days': 46, 'max_days': None}],
 'bands_adopted_on': '2026-05-04',
 'edges': [{'link_id': 'PLAT-118',
            'producer_team': 'platform',
            'consumer_team': 'payments',
            'dependency_type': 'api-contract',
            'opened_at': '2026-07-21',
            'needed_by': '2026-09-30',
            'blocked_task_count': 6,
            'age_days': 3,
            'band': '0-7',
            'slack_days': 23,
            'action': {'owner': 'platform-lead:marko',
                       'due_date': '2026-09-11',
                       'text': 'Waiting on platform to confirm the contract.'}},
           {'link_id': 'WEB-402',
            'producer_team': 'web',
            'consumer_team': 'payments',
            'dependency_type': 'shared-component',
            'opened_at': '2026-08-20',
            'needed_by': '2026-09-04',
            'blocked_task_count': 2,
            'age_days': 18,
            'band': '15-45',
            'slack_days': -3},
           {'link_id': 'SEC-9',
            'producer_team': 'security',
            'consumer_team': 'payments',
            'dependency_type': 'review-approval',
            'opened_at': '2026-09-02',
            'needed_by': '2026-09-25',
            'blocked_task_count': 1,
            'age_days': 5,
            'band': '0-7',
            'slack_days': 18}],
 'action_table': ['PLAT-118', 'SEC-9', 'WEB-402'],
 'resolved_log': [{'link_id': 'SEC-7',
                   'opened_at': '2026-08-12',
                   'resolved_on': '2026-09-01',
                   'age_days': 20,
                   'outcome': 'delivered',
                   'needed_by': '2026-09-25'},
                  {'link_id': 'PLAT-112',
                   'opened_at': '2026-07-14',
                   'resolved_on': '2026-08-13',
                   'age_days': 30,
                   'outcome': 'delivered',
                   'needed_by': '2026-08-10'}],
 'sle': {'resolved_count_12w': 2, 'status': 'line'}}


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
import math
from datetime import date, timedelta

_WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _d(s):
    try:
        return date.fromisoformat((s or "")[:10])
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    cd = _d(obj.get("chart_date"))
    if cd and _WEEKDAYS[cd.weekday()] != obj.get("checkpoint_weekday"):
        errs.append(f"chart_date {cd} is a {_WEEKDAYS[cd.weekday()]}, not the checkpoint weekday {obj.get('checkpoint_weekday')} (r-weekly-refresh-by-script)")
    ex = _d(obj.get("extracted_at"))
    if cd and ex and not (cd - timedelta(days=7) < ex <= cd):
        errs.append(f"extracted_at {ex} is not within the checkpoint week ending {cd}; regenerate by script before the checkpoint (r-weekly-refresh-by-script)")
    bands = [b for b in obj.get("age_bands") or [] if isinstance(b, dict)]
    if bands:
        if bands[0].get("min_days") != 0:
            errs.append("age_bands[0].min_days must be 0 (r-age-bands-fixed)")
        for i in range(1, len(bands)):
            if bands[i - 1].get("max_days") is None or bands[i].get("min_days") != bands[i - 1].get("max_days") + 1:
                errs.append(f"age_bands[{i}] does not start the day after age_bands[{i - 1}] ends; bands must be contiguous (r-age-bands-fixed)")
        if bands[-1].get("max_days") is not None:
            errs.append("the top age band must be open (max_days null) so nothing ages out of the chart (r-age-bands-fixed)")
    def band_index(age):
        for i, b in enumerate(bands):
            if age >= b.get("min_days", 0) and (b.get("max_days") is None or age <= b["max_days"]):
                return i
        return None
    top = len(bands) - 1
    edges = [e for e in obj.get("edges") or [] if isinstance(e, dict)]
    resolved = [r for r in obj.get("resolved_log") or [] if isinstance(r, dict)]
    resolved_ids = {r.get("link_id") for r in resolved}
    keys = {}
    for i, e in enumerate(edges):
        p = f"edges[{i}] ({e.get('link_id')})"
        op = _d(e.get("opened_at"))
        age = (cd - op).days if cd and op else None
        if age is not None and e.get("age_days") != age:
            errs.append(f"{p}: age_days must be chart_date minus opened_at = {age}, not a last-activity clock (r-age-from-dependency-open-not-task)")
        bi = band_index(e.get("age_days", 0))
        if bi is None or bands[bi].get("label") != e.get("band"):
            errs.append(f"{p}: band must be the adopted band containing {e.get('age_days')} days (r-age-bands-fixed)")
        nb = _d(e.get("needed_by")) if e.get("needed_by") else None
        slack = (nb - cd).days if nb and cd else None
        if e.get("needed_by") is None and e.get("slack_days") is not None:
            errs.append(f"{p}: slack_days must be null on a no-deadline edge (r-milestone-slack-column)")
        elif slack is not None and e.get("slack_days") != slack:
            errs.append(f"{p}: slack_days must be needed_by minus chart_date = {slack} (r-milestone-slack-column)")
        red = e.get("slack_days") is not None and e.get("slack_days") <= 0
        escalate = red or (bi is not None and bi >= 1)
        if escalate and "action" not in e:
            errs.append(f"{p}: in band {e.get('band')} / slack {e.get('slack_days')} and carries no action with owner and due date (r-action-per-escalation-band)")
        if bi is not None and bi == top:
            rb = e.get("rebaseline")
            if not rb:
                errs.append(f"{p}: over the top band boundary and carries no rebaseline decision (r-action-per-escalation-band)")
            elif rb.get("decided_by") != obj.get("owner"):
                errs.append(f"{p}: rebaseline.decided_by must be the program PM {obj.get('owner')} (03 human checkpoint)")
        if e.get("superseded_from") in resolved_ids:
            errs.append(f"{p}: superseded_from {e.get('superseded_from')} is still in resolved_log; a re-ticketed edge is one edge with the original opened_at, not a resolved one plus a new one (r-no-aging-reset)")
        keys[e.get("link_id")] = (0 if red else 1, -(bi if bi is not None else -1), -e.get("blocked_task_count", 0))
    table = obj.get("action_table") or []
    if set(table) != set(keys):
        errs.append("action_table must list every open edge's link_id exactly once (r-count-blocked-tasks-per-edge)")
    else:
        want = sorted(table, key=lambda k: keys[k])
        if [keys[k] for k in table] != [keys[k] for k in want]:
            errs.append(f"action_table order must be non-positive slack first, then band descending, then blocked_task_count descending: {want} (r-milestone-slack-column, r-count-blocked-tasks-per-edge)")
    ages = []
    for i, r in enumerate(resolved):
        op, ro = _d(r.get("opened_at")), _d(r.get("resolved_on"))
        if op and ro and r.get("age_days") != (ro - op).days:
            errs.append(f"resolved_log[{i}] ({r.get('link_id')}): age_days must be resolved_on minus opened_at = {(ro - op).days} (r-closed-edges-feed-sle)")
        if cd and ro and cd - timedelta(weeks=12) <= ro <= cd:
            ages.append(r.get("age_days", 0))
    sle = obj.get("sle") or {}
    if sle.get("resolved_count_12w") != len(ages):
        errs.append(f"sle.resolved_count_12w must be the resolved edges in the trailing 12 weeks = {len(ages)} (r-closed-edges-feed-sle)")
    want_status = "line" if len(ages) >= 10 else "insufficient-data"
    if sle.get("status") != want_status:
        errs.append(f"sle.status must be {want_status} with {len(ages)} resolved edges (r-closed-edges-feed-sle)")
    if want_status == "line" and ages:
        p85 = sorted(ages)[max(0, math.ceil(0.85 * len(ages)) - 1)]
        if sle.get("p85_days") != p85:
            errs.append(f"sle.p85_days must be the 85th percentile of the trailing-12-week resolved ages = {p85} (r-closed-edges-feed-sle)")
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
        prog="validate-program-dependency-aging-chart-recipe.py",
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
