#!/usr/bin/env python3
"""validate-content-refresh-sop.py

Validate the artefact produced by the content-refresh-sop methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/content-refresh-sop.json',
 'title': 'Content Refresh SOP playbook step',
 'type': 'object',
 'required': ['thresholds', 'window', 'urls', 'decision_branches'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'url': {'type': 'string', 'pattern': '^https://[^\\s/]+/'},
                 'count': {'type': 'integer', 'minimum': 0},
                 'gsc': {'type': 'object',
                         'required': ['clicks', 'impressions', 'avg_position'],
                         'additionalProperties': False,
                         'properties': {'clicks': {'$ref': '#/definitions/count'},
                                        'impressions': {'$ref': '#/definitions/count'},
                                        'avg_position': {'type': 'number', 'minimum': 1}}},
                 'ga4': {'type': 'object',
                         'required': ['sessions', 'key_events'],
                         'additionalProperties': False,
                         'properties': {'sessions': {'$ref': '#/definitions/count'},
                                        'key_events': {'$ref': '#/definitions/count'}}},
                 'rank': {'type': 'object',
                          'required': ['target_query', 'position'],
                          'additionalProperties': False,
                          'properties': {'target_query': {'type': 'string', 'minLength': 3},
                                         'position': {'type': 'number', 'minimum': 1}}},
                 'baseline': {'type': 'object',
                              'required': ['published_at',
                                           'days',
                                           'clicks',
                                           'impressions',
                                           'avg_position',
                                           'sessions',
                                           'key_events'],
                              'additionalProperties': False,
                              'properties': {'published_at': {'$ref': '#/definitions/date'},
                                             'days': {'const': 28},
                                             'clicks': {'$ref': '#/definitions/count'},
                                             'impressions': {'$ref': '#/definitions/count'},
                                             'avg_position': {'type': 'number', 'minimum': 1},
                                             'sessions': {'$ref': '#/definitions/count'},
                                             'key_events': {'$ref': '#/definitions/count'}}}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'thresholds': {'type': 'object',
                               'required': ['impressions_trend_pct',
                                            'position_decay_positions',
                                            'intent_shift_query_mix_pct'],
                               'additionalProperties': False,
                               'properties': {'impressions_trend_pct': {'type': 'number',
                                                                        'maximum': 0},
                                              'position_decay_positions': {'type': 'number',
                                                                           'exclusiveMinimum': 0},
                                              'intent_shift_query_mix_pct': {'type': 'number',
                                                                             'exclusiveMinimum': 0}}},
                'window': {'type': 'object',
                           'required': ['trailing_days', 'prior_days', 'span_months', 'source'],
                           'additionalProperties': False,
                           'properties': {'trailing_days': {'type': 'integer', 'minimum': 28},
                                          'prior_days': {'type': 'integer', 'minimum': 28},
                                          'span_months': {'type': 'integer', 'minimum': 1},
                                          'source': {'type': 'string',
                                                     'enum': ['persisted_export',
                                                              'search_console_ui']}},
                           'if': {'properties': {'span_months': {'minimum': 17}}},
                           'then': {'properties': {'source': {'const': 'persisted_export'}}}},
                'urls': {'type': 'array',
                         'minItems': 1,
                         'items': {'type': 'object',
                                   'required': ['url',
                                                'evergreen',
                                                'url_age_months',
                                                'dataset',
                                                'signals',
                                                'verdict'],
                                   'additionalProperties': False,
                                   'properties': {'url': {'$ref': '#/definitions/url'},
                                                  'evergreen': {'const': True},
                                                  'url_age_months': {'type': 'integer',
                                                                     'minimum': 12},
                                                  'dataset': {'type': 'object',
                                                              'required': ['trailing', 'prior'],
                                                              'additionalProperties': False,
                                                              'properties': {'trailing': {'type': 'object',
                                                                                          'required': ['gsc',
                                                                                                       'ga4',
                                                                                                       'rank'],
                                                                                          'additionalProperties': False,
                                                                                          'properties': {'gsc': {'$ref': '#/definitions/gsc'},
                                                                                                         'ga4': {'$ref': '#/definitions/ga4'},
                                                                                                         'rank': {'$ref': '#/definitions/rank'}}},
                                                                             'prior': {'type': 'object',
                                                                                       'required': ['gsc',
                                                                                                    'ga4',
                                                                                                    'rank'],
                                                                                       'additionalProperties': False,
                                                                                       'properties': {'gsc': {'$ref': '#/definitions/gsc'},
                                                                                                      'ga4': {'$ref': '#/definitions/ga4'},
                                                                                                      'rank': {'$ref': '#/definitions/rank'}}}}},
                                                  'signals': {'type': 'object',
                                                              'required': ['impressions_trend_pct',
                                                                           'position_decay_positions',
                                                                           'intent_shift',
                                                                           'intent_shift_note'],
                                                              'additionalProperties': False,
                                                              'properties': {'impressions_trend_pct': {'type': 'number'},
                                                                             'position_decay_positions': {'type': 'number'},
                                                                             'intent_shift': {'type': 'boolean'},
                                                                             'intent_shift_note': {'type': 'string',
                                                                                                   'minLength': 10}}},
                                                  'verdict': {'type': 'string',
                                                              'enum': ['refresh',
                                                                       'consolidate',
                                                                       'kill',
                                                                       'leave']},
                                                  'refresh': {'type': 'object',
                                                              'required': ['url_unchanged',
                                                                           'substantive_change',
                                                                           'date_modified_updated',
                                                                           'title_changed_for_intent',
                                                                           'checklist',
                                                                           'baseline',
                                                                           'reevaluation_at'],
                                                              'additionalProperties': False,
                                                              'properties': {'url_unchanged': {'const': True},
                                                                             'substantive_change': {'type': 'boolean'},
                                                                             'date_modified_updated': {'type': 'boolean'},
                                                                             'title_changed_for_intent': {'type': 'boolean'},
                                                                             'checklist': {'type': 'array',
                                                                                           'minItems': 9,
                                                                                           'maxItems': 9,
                                                                                           'items': {'type': 'object',
                                                                                                     'required': ['step',
                                                                                                                  'name',
                                                                                                                  'exit_criterion',
                                                                                                                  'done'],
                                                                                                     'additionalProperties': False,
                                                                                                     'properties': {'step': {'type': 'integer',
                                                                                                                             'minimum': 1,
                                                                                                                             'maximum': 9},
                                                                                                                    'name': {'type': 'string',
                                                                                                                             'minLength': 5},
                                                                                                                    'exit_criterion': {'type': 'string',
                                                                                                                                       'minLength': 15},
                                                                                                                    'done': {'type': 'boolean'},
                                                                                                                    'skipped_reason': {'type': 'string',
                                                                                                                                       'minLength': 10}},
                                                                                                     'if': {'properties': {'done': {'const': False}}},
                                                                                                     'then': {'required': ['skipped_reason']}}},
                                                                             'baseline': {'$ref': '#/definitions/baseline'},
                                                                             'reevaluation_at': {'$ref': '#/definitions/date'}},
                                                              'if': {'properties': {'date_modified_updated': {'const': True}}},
                                                              'then': {'properties': {'substantive_change': {'const': True}}}},
                                                  'consolidate': {'type': 'object',
                                                                  'required': ['survivor_url',
                                                                               'merged_urls',
                                                                               'redirects',
                                                                               'internal_links_rewritten',
                                                                               'baseline',
                                                                               'reevaluation_at'],
                                                                  'additionalProperties': False,
                                                                  'properties': {'survivor_url': {'$ref': '#/definitions/url'},
                                                                                 'merged_urls': {'type': 'array',
                                                                                                 'minItems': 1,
                                                                                                 'items': {'$ref': '#/definitions/url'}},
                                                                                 'redirects': {'type': 'array',
                                                                                               'minItems': 1,
                                                                                               'items': {'type': 'object',
                                                                                                         'required': ['from',
                                                                                                                      'to',
                                                                                                                      'status'],
                                                                                                         'additionalProperties': False,
                                                                                                         'properties': {'from': {'$ref': '#/definitions/url'},
                                                                                                                        'to': {'$ref': '#/definitions/url'},
                                                                                                                        'status': {'type': 'integer',
                                                                                                                                   'enum': [301,
                                                                                                                                            308]}}}},
                                                                                 'internal_links_rewritten': {'const': True},
                                                                                 'baseline': {'$ref': '#/definitions/baseline'},
                                                                                 'reevaluation_at': {'$ref': '#/definitions/date'}}},
                                                  'kill': {'type': 'object',
                                                           'required': ['http_status',
                                                                        'removed_from_sitemap',
                                                                        'removed_from_navigation',
                                                                        'internal_links_dropped',
                                                                        'redirect_target'],
                                                           'additionalProperties': False,
                                                           'properties': {'http_status': {'type': 'integer',
                                                                                          'enum': [410,
                                                                                                   404]},
                                                                          'removed_from_sitemap': {'const': True},
                                                                          'removed_from_navigation': {'const': True},
                                                                          'internal_links_dropped': {'const': True},
                                                                          'redirect_target': {'type': 'null'}}},
                                                  'leave': {'type': 'object',
                                                            'required': ['reason',
                                                                         'next_review_at'],
                                                            'additionalProperties': False,
                                                            'properties': {'reason': {'type': 'string',
                                                                                      'minLength': 15},
                                                                           'next_review_at': {'$ref': '#/definitions/date'}}}},
                                   'allOf': [{'if': {'properties': {'verdict': {'const': 'refresh'}}},
                                              'then': {'required': ['refresh']}},
                                             {'if': {'properties': {'verdict': {'const': 'consolidate'}}},
                                              'then': {'required': ['consolidate']}},
                                             {'if': {'properties': {'verdict': {'const': 'kill'}}},
                                              'then': {'required': ['kill']}},
                                             {'if': {'properties': {'verdict': {'const': 'leave'}}},
                                              'then': {'required': ['leave']}}]}},
                'decision_branches': {'type': 'array',
                                      'minItems': 3,
                                      'allOf': [{'contains': {'properties': {'signal': {'const': 'impressions_trend'}}}},
                                                {'contains': {'properties': {'signal': {'const': 'top_position_decay'}}}},
                                                {'contains': {'properties': {'signal': {'const': 'intent_shift'}}}}],
                                      'items': {'type': 'object',
                                                'required': ['signal', 'when', 'then'],
                                                'additionalProperties': False,
                                                'properties': {'signal': {'type': 'string',
                                                                          'enum': ['impressions_trend',
                                                                                   'top_position_decay',
                                                                                   'intent_shift']},
                                                               'when': {'type': 'string',
                                                                        'minLength': 10,
                                                                        'pattern': '[0-9]'},
                                                               'then': {'type': 'string',
                                                                        'enum': ['refresh',
                                                                                 'consolidate',
                                                                                 'kill',
                                                                                 'leave']}}}}}}

OK = {'thresholds': {'impressions_trend_pct': -20,
                'position_decay_positions': 2,
                'intent_shift_query_mix_pct': 30},
 'window': {'trailing_days': 90, 'prior_days': 90, 'span_months': 6, 'source': 'persisted_export'},
 'urls': [{'url': 'https://example.com/blog/content-refresh-checklist',
           'evergreen': True,
           'url_age_months': 19,
           'dataset': {'trailing': {'gsc': {'clicks': 1240,
                                            'impressions': 38400,
                                            'avg_position': 7.8},
                                    'ga4': {'sessions': 1180, 'key_events': 41},
                                    'rank': {'target_query': 'content refresh checklist',
                                             'position': 8}},
                       'prior': {'gsc': {'clicks': 2010, 'impressions': 56500, 'avg_position': 4.7},
                                 'ga4': {'sessions': 1950, 'key_events': 77},
                                 'rank': {'target_query': 'content refresh checklist',
                                          'position': 5}}},
           'signals': {'impressions_trend_pct': -32.0,
                       'position_decay_positions': 3.1,
                       'intent_shift': False,
                       'intent_shift_note': 'top 10 still how-to guides; query mix change 9 '
                                            'percent, under the 30 percent threshold'},
           'verdict': 'refresh',
           'refresh': {'url_unchanged': True,
                       'substantive_change': True,
                       'date_modified_updated': True,
                       'title_changed_for_intent': False,
                       'checklist': [{'step': 1,
                                      'name': 're-run query and intent research',
                                      'exit_criterion': "top 10 SERP captured for 'content refresh "
                                                        "checklist' on 2026-04-28; intent still "
                                                        'how-to',
                                      'done': True},
                                     {'step': 2,
                                      'name': 'update facts, statistics, prices, dates',
                                      'exit_criterion': '11 statistics replaced with 2025-2026 '
                                                        'sources, each linked and dated',
                                      'done': True},
                                     {'step': 3,
                                      'name': 'rewrite title, meta description, intro',
                                      'exit_criterion': 'intro rewritten to the current intent; '
                                                        'meta description under 155 characters',
                                      'done': True},
                                     {'step': 4,
                                      'name': 'add sections top-ranking pages cover',
                                      'exit_criterion': 'sections added for AI Overview impact and '
                                                        'Core Web Vitals; gap list from step 1 '
                                                        'closed',
                                      'done': True},
                                     {'step': 5,
                                      'name': 'refresh screenshots, media, examples',
                                      'exit_criterion': '6 screenshots retaken on the 2026 Search '
                                                        'Console UI',
                                      'done': True},
                                     {'step': 6,
                                      'name': 'update internal links in and out',
                                      'exit_criterion': '4 newer posts now link to the page; 3 '
                                                        'dead outbound links replaced',
                                      'done': True},
                                     {'step': 7,
                                      'name': 'fix technical issues on the URL',
                                      'exit_criterion': '2 broken links fixed, alt text on all '
                                                        'images, structured data validates, LCP '
                                                        'under 2.5 s',
                                      'done': True},
                                     {'step': 8,
                                      'name': 'update dateModified and append changelog',
                                      'exit_criterion': 'dateModified 2026-05-06; changelog entry '
                                                        'lists steps 2, 4, 5, 6',
                                      'done': True},
                                     {'step': 9,
                                      'name': 'request re-indexing and record baseline',
                                      'exit_criterion': 'URL inspection re-index requested; 28-day '
                                                        'baseline stored',
                                      'done': True}],
                       'baseline': {'published_at': '2026-05-06',
                                    'days': 28,
                                    'clicks': 380,
                                    'impressions': 11900,
                                    'avg_position': 7.9,
                                    'sessions': 360,
                                    'key_events': 12},
                       'reevaluation_at': '2026-08-04'}},
          {'url': 'https://example.com/blog/what-is-a-content-audit',
           'evergreen': True,
           'url_age_months': 31,
           'dataset': {'trailing': {'gsc': {'clicks': 860,
                                            'impressions': 21000,
                                            'avg_position': 3.2},
                                    'ga4': {'sessions': 820, 'key_events': 33},
                                    'rank': {'target_query': 'what is a content audit',
                                             'position': 3}},
                       'prior': {'gsc': {'clicks': 910, 'impressions': 22600, 'avg_position': 3.0},
                                 'ga4': {'sessions': 870, 'key_events': 35},
                                 'rank': {'target_query': 'what is a content audit',
                                          'position': 3}}},
           'signals': {'impressions_trend_pct': -7.1,
                       'position_decay_positions': 0.2,
                       'intent_shift': False,
                       'intent_shift_note': 'query mix change 4 percent; SERP features unchanged'},
           'verdict': 'leave',
           'leave': {'reason': 'all three signals inside thresholds: -7.1 percent impressions, 0.2 '
                               'positions, no intent shift',
                     'next_review_at': '2026-11-04'}}],
 'decision_branches': [{'signal': 'intent_shift',
                        'when': 'query mix changed by more than 30 percent or the SERP turned to a '
                                'different result type',
                        'then': 'kill'},
                       {'signal': 'impressions_trend',
                        'when': 'impressions down more than 20 percent period over period with no '
                                'intent shift',
                        'then': 'refresh'},
                       {'signal': 'top_position_decay',
                        'when': 'average position worse by more than 2 positions with no intent '
                                'shift',
                        'then': 'refresh'},
                       {'signal': 'impressions_trend',
                        'when': 'impressions within 20 percent and position within 2 positions',
                        'then': 'leave'}]}

BAD = {'thresholds': {'impressions_trend_pct': -20,
                'position_decay_positions': 2,
                'intent_shift_query_mix_pct': 30},
 'window': {'trailing_days': 365,
            'prior_days': 120,
            'span_months': 24,
            'source': 'search_console_ui'},
 'urls': [{'url': 'https://example.com/blog/content-refresh-checklist',
           'evergreen': True,
           'url_age_months': 8,
           'dataset': {'trailing': {'gsc': {'clicks': 1240,
                                            'impressions': 38400,
                                            'avg_position': 7.8},
                                    'ga4': {'sessions': 1180, 'key_events': 41},
                                    'rank': {'target_query': 'content refresh checklist',
                                             'position': 8}},
                       'prior': {'gsc': {'clicks': 2010, 'impressions': 56500, 'avg_position': 4.7},
                                 'ga4': {'sessions': 1950, 'key_events': 77},
                                 'rank': {'target_query': 'content refresh checklist',
                                          'position': 5}}},
           'signals': {'impressions_trend_pct': -12.0,
                       'position_decay_positions': 1.0,
                       'intent_shift': False,
                       'intent_shift_note': 'not checked this cycle'},
           'verdict': 'refresh',
           'refresh': {'url_unchanged': False,
                       'substantive_change': False,
                       'date_modified_updated': True,
                       'title_changed_for_intent': True,
                       'checklist': [{'step': 3,
                                      'name': 'rewrite title, meta description, intro',
                                      'exit_criterion': 'new title and intro published under the '
                                                        'new slug',
                                      'done': True},
                                     {'step': 8,
                                      'name': 'update dateModified and append changelog',
                                      'exit_criterion': 'dateModified set to publication day',
                                      'done': True}],
                       'baseline': {'published_at': '2026-05-06',
                                    'days': 7,
                                    'clicks': 90,
                                    'impressions': 2900,
                                    'avg_position': 8.1,
                                    'sessions': 85,
                                    'key_events': 3},
                       'reevaluation_at': '2026-05-20'}},
          {'url': 'https://example.com/blog/content-audit-tools-2021',
           'evergreen': True,
           'url_age_months': 40,
           'dataset': {'trailing': {'gsc': {'clicks': 40,
                                            'impressions': 3100,
                                            'avg_position': 18.2},
                                    'ga4': {'sessions': 38, 'key_events': 0},
                                    'rank': {'target_query': 'content audit tools',
                                             'position': 19}},
                       'prior': {'gsc': {'clicks': 210, 'impressions': 9800, 'avg_position': 9.4},
                                 'ga4': {'sessions': 200, 'key_events': 4},
                                 'rank': {'target_query': 'content audit tools', 'position': 9}}},
           'signals': {'impressions_trend_pct': -68.4,
                       'position_decay_positions': 8.8,
                       'intent_shift': True,
                       'intent_shift_note': 'SERP now product listings and comparison tables'},
           'verdict': 'kill',
           'kill': {'http_status': 301,
                    'removed_from_sitemap': False,
                    'removed_from_navigation': True,
                    'internal_links_dropped': False,
                    'redirect_target': 'https://example.com/'}}],
 'decision_branches': [{'signal': 'impressions_trend',
                        'when': 'impressions look weak',
                        'then': 'refresh'}]}


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

from datetime import date, timedelta


def _d(s):
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    w = obj.get("window") or {}
    if w.get("trailing_days") != w.get("prior_days"):
        errs.append(f"window: prior_days {w.get('prior_days')} must equal trailing_days {w.get('trailing_days')} (r-one-dataset-gsc-ga4-rank)")
    for i, u in enumerate(obj.get("urls") or []):
        ds = u.get("dataset") or {}
        t, p = ds.get("trailing") or {}, ds.get("prior") or {}
        sg = u.get("signals") or {}
        tg, pg = t.get("gsc") or {}, p.get("gsc") or {}
        if pg.get("impressions"):
            want = round((tg.get("impressions", 0) - pg["impressions"]) / pg["impressions"] * 100, 1)
            if abs(want - sg.get("impressions_trend_pct", 1e9)) > 0.15:
                errs.append(f"urls[{i}]: signals.impressions_trend_pct must be (trailing - prior) / prior x 100 = {want} (r-three-signals-with-thresholds)")
        if tg.get("avg_position") is not None and pg.get("avg_position") is not None:
            want = round(tg["avg_position"] - pg["avg_position"], 1)
            if abs(want - sg.get("position_decay_positions", 1e9)) > 0.15:
                errs.append(f"urls[{i}]: signals.position_decay_positions must be trailing avg_position - prior avg_position = {want} (r-three-signals-with-thresholds)")
        if (t.get("rank") or {}).get("target_query") != (p.get("rank") or {}).get("target_query"):
            errs.append(f"urls[{i}]: rank.target_query differs between windows (r-one-dataset-gsc-ga4-rank)")
        for kind in ("refresh", "consolidate"):
            blk = u.get(kind)
            if not blk:
                continue
            pub, re_at = _d((blk.get("baseline") or {}).get("published_at", "")), _d(blk.get("reevaluation_at", ""))
            if pub and re_at and re_at != pub + timedelta(days=90):
                errs.append(f"urls[{i}].{kind}: reevaluation_at must be baseline.published_at + 90 days = {pub + timedelta(days=90)} (r-baseline-and-90-day-reevaluation)")
        rf = u.get("refresh")
        if rf:
            steps = sorted(c.get("step") for c in rf.get("checklist") or [])
            if steps != list(range(1, 10)):
                errs.append(f"urls[{i}].refresh: checklist must contain steps 1-9 exactly once, got {steps} (r-nine-step-checklist-complete)")
            done = {c.get("step") for c in rf.get("checklist") or [] if c.get("done")}
            if rf.get("substantive_change") and not {2, 4, 6} <= done:
                errs.append(f"urls[{i}].refresh: substantive_change requires steps 2, 4 and 6 done (r-nine-step-checklist-complete, r-refresh-keeps-url-honest-date)")
        cs = u.get("consolidate")
        if cs:
            targets = {r.get("from"): r for r in cs.get("redirects") or []}
            for m in cs.get("merged_urls") or []:
                r = targets.get(m)
                if r is None:
                    errs.append(f"urls[{i}].consolidate: merged URL {m} has no redirect (r-consolidate-301-to-survivor)")
                elif r.get("to") != cs.get("survivor_url"):
                    errs.append(f"urls[{i}].consolidate: redirect from {m} does not point at the survivor (r-consolidate-301-to-survivor)")
            if cs.get("survivor_url") in (cs.get("merged_urls") or []):
                errs.append(f"urls[{i}].consolidate: survivor_url is listed among merged_urls (r-consolidate-301-to-survivor)")
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
        prog="validate-content-refresh-sop.py",
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
