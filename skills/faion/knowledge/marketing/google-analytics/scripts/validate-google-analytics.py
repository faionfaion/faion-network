#!/usr/bin/env python3
"""validate-google-analytics.py

Validate the artefact produced by the google-analytics methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/google-analytics.json',
 'title': 'Google Analytics 4 property config',
 'type': 'object',
 'required': ['property_id',
              'site_domain',
              'data_streams',
              'enhanced_measurement',
              'custom_dimensions',
              'events',
              'key_events',
              'purchase',
              'consent',
              'bigquery_export',
              'data_retention_months',
              'measurement_protocol',
              'traffic_filters'],
 'additionalProperties': False,
 'definitions': {'host': {'type': 'string', 'pattern': '^[a-z0-9.-]+\\.[a-z]{2,}$'},
                 'snake': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]{0,39}$'},
                 'count': {'type': 'integer', 'minimum': 0}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'property_id': {'type': 'string', 'pattern': '^[0-9]{6,12}$'},
                'site_domain': {'$ref': '#/definitions/host'},
                'data_streams': {'type': 'array',
                                 'minItems': 1,
                                 'items': {'type': 'object',
                                           'required': ['name',
                                                        'type',
                                                        'measurement_id',
                                                        'spa',
                                                        'manual_page_view',
                                                        'send_page_view'],
                                           'additionalProperties': False,
                                           'properties': {'name': {'type': 'string',
                                                                   'minLength': 2},
                                                          'type': {'type': 'string',
                                                                   'enum': ['web',
                                                                            'ios',
                                                                            'android']},
                                                          'measurement_id': {'type': 'string',
                                                                             'pattern': '^G-[A-Z0-9]{6,12}$'},
                                                          'spa': {'type': 'boolean'},
                                                          'manual_page_view': {'type': 'boolean'},
                                                          'send_page_view': {'type': 'boolean'}},
                                           'if': {'properties': {'manual_page_view': {'const': True}}},
                                           'then': {'properties': {'send_page_view': {'const': False}}},
                                           'else': {'properties': {'send_page_view': {'const': True}}}}},
                'enhanced_measurement': {'type': 'object',
                                         'required': ['page_views',
                                                      'history_change_page_view',
                                                      'scrolls',
                                                      'outbound_clicks',
                                                      'site_search',
                                                      'video_engagement',
                                                      'file_downloads',
                                                      'form_interactions'],
                                         'additionalProperties': False,
                                         'properties': {'page_views': {'type': 'boolean'},
                                                        'history_change_page_view': {'type': 'boolean'},
                                                        'scrolls': {'type': 'boolean'},
                                                        'outbound_clicks': {'type': 'boolean'},
                                                        'site_search': {'type': 'boolean'},
                                                        'video_engagement': {'type': 'boolean'},
                                                        'file_downloads': {'type': 'boolean'},
                                                        'form_interactions': {'type': 'boolean'}}},
                'custom_dimensions': {'type': 'object',
                                      'required': ['limits', 'registered', 'used'],
                                      'additionalProperties': False,
                                      'properties': {'limits': {'type': 'object',
                                                                'required': ['event',
                                                                             'user',
                                                                             'item',
                                                                             'metrics'],
                                                                'additionalProperties': False,
                                                                'properties': {'event': {'type': 'integer',
                                                                                         'minimum': 1},
                                                                               'user': {'type': 'integer',
                                                                                        'minimum': 1},
                                                                               'item': {'type': 'integer',
                                                                                        'minimum': 1},
                                                                               'metrics': {'type': 'integer',
                                                                                           'minimum': 1}}},
                                                     'registered': {'type': 'array',
                                                                    'items': {'type': 'object',
                                                                              'required': ['name',
                                                                                           'parameter',
                                                                                           'scope',
                                                                                           'kind',
                                                                                           'registered_before_first_send'],
                                                                              'additionalProperties': False,
                                                                              'properties': {'name': {'type': 'string',
                                                                                                      'minLength': 2},
                                                                                             'parameter': {'$ref': '#/definitions/snake'},
                                                                                             'scope': {'type': 'string',
                                                                                                       'enum': ['event',
                                                                                                                'user',
                                                                                                                'item']},
                                                                                             'kind': {'type': 'string',
                                                                                                      'enum': ['dimension',
                                                                                                               'metric']},
                                                                                             'registered_before_first_send': {'const': True}}}},
                                                     'used': {'type': 'object',
                                                              'required': ['event',
                                                                           'user',
                                                                           'item',
                                                                           'metrics'],
                                                              'additionalProperties': False,
                                                              'properties': {'event': {'$ref': '#/definitions/count'},
                                                                             'user': {'$ref': '#/definitions/count'},
                                                                             'item': {'$ref': '#/definitions/count'},
                                                                             'metrics': {'$ref': '#/definitions/count'}}}}},
                'events': {'type': 'array',
                           'minItems': 1,
                           'uniqueItems': True,
                           'items': {'$ref': '#/definitions/snake'}},
                'key_events': {'type': 'array',
                               'minItems': 1,
                               'maxItems': 30,
                               'items': {'type': 'object',
                                         'required': ['event_name', 'counting'],
                                         'additionalProperties': False,
                                         'properties': {'event_name': {'$ref': '#/definitions/snake'},
                                                        'counting': {'type': 'string',
                                                                     'enum': ['once_per_event',
                                                                              'once_per_session']}}}},
                'purchase': {'type': 'object',
                             'required': ['enabled'],
                             'properties': {'enabled': {'type': 'boolean'}},
                             'if': {'properties': {'enabled': {'const': True}}},
                             'then': {'required': ['required_parameters',
                                                   'transaction_id_source',
                                                   'stable_across_retries'],
                                      'additionalProperties': False,
                                      'properties': {'enabled': {'const': True},
                                                     'required_parameters': {'type': 'array',
                                                                             'minItems': 4,
                                                                             'items': {'$ref': '#/definitions/snake'},
                                                                             'allOf': [{'contains': {'const': 'transaction_id'}},
                                                                                       {'contains': {'const': 'value'}},
                                                                                       {'contains': {'const': 'currency'}},
                                                                                       {'contains': {'const': 'items'}}]},
                                                     'transaction_id_source': {'const': 'order_id'},
                                                     'stable_across_retries': {'const': True}}},
                             'else': {'additionalProperties': False,
                                      'properties': {'enabled': {'const': False}}}},
                'consent': {'type': 'object',
                            'required': ['in_scope'],
                            'properties': {'in_scope': {'type': 'boolean'}},
                            'if': {'properties': {'in_scope': {'const': True}}},
                            'then': {'required': ['implementation',
                                                  'defaults_before_config',
                                                  'signals',
                                                  'regions',
                                                  'update_on_choice'],
                                     'additionalProperties': False,
                                     'properties': {'in_scope': {'const': True},
                                                    'implementation': {'type': 'string',
                                                                       'enum': ['basic',
                                                                                'advanced']},
                                                    'defaults_before_config': {'const': True},
                                                    'signals': {'type': 'array',
                                                                'minItems': 4,
                                                                'items': {'type': 'string',
                                                                          'enum': ['ad_storage',
                                                                                   'analytics_storage',
                                                                                   'ad_user_data',
                                                                                   'ad_personalization']},
                                                                'allOf': [{'contains': {'const': 'ad_storage'}},
                                                                          {'contains': {'const': 'analytics_storage'}},
                                                                          {'contains': {'const': 'ad_user_data'}},
                                                                          {'contains': {'const': 'ad_personalization'}}]},
                                                    'regions': {'type': 'array',
                                                                'minItems': 1,
                                                                'items': {'type': 'string',
                                                                          'pattern': '^[A-Z]{2}(-[A-Z0-9]{1,3})?$'}},
                                                    'update_on_choice': {'const': True}}},
                            'else': {'additionalProperties': False,
                                     'properties': {'in_scope': {'const': False}}}},
                'bigquery_export': {'type': 'object',
                                    'required': ['linked',
                                                 'linked_before_launch',
                                                 'linked_at',
                                                 'project',
                                                 'dataset_location',
                                                 'daily',
                                                 'streaming',
                                                 'sampling_threshold_events',
                                                 'decision_reports_source'],
                                    'additionalProperties': False,
                                    'properties': {'linked': {'const': True},
                                                   'linked_before_launch': {'const': True},
                                                   'linked_at': {'type': 'string',
                                                                 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                                                   'project': {'type': 'string', 'minLength': 3},
                                                   'dataset_location': {'type': 'string',
                                                                        'minLength': 2},
                                                   'daily': {'const': True},
                                                   'streaming': {'type': 'boolean'},
                                                   'sampling_threshold_events': {'type': 'integer',
                                                                                 'minimum': 1},
                                                   'decision_reports_source': {'const': 'bigquery'}}},
                'data_retention_months': {'const': 14},
                'measurement_protocol': {'type': 'object',
                                         'required': ['used'],
                                         'properties': {'used': {'type': 'boolean'}},
                                         'if': {'properties': {'used': {'const': True}}},
                                         'then': {'required': ['client_id_source',
                                                               'session_id_included',
                                                               'engagement_time_msec_included',
                                                               'api_secret_storage',
                                                               'fresh_client_id'],
                                                  'additionalProperties': False,
                                                  'properties': {'used': {'const': True},
                                                                 'client_id_source': {'const': '_ga '
                                                                                               'cookie'},
                                                                 'session_id_included': {'const': True},
                                                                 'engagement_time_msec_included': {'const': True},
                                                                 'api_secret_storage': {'const': 'server_only'},
                                                                 'fresh_client_id': {'const': False}}},
                                         'else': {'additionalProperties': False,
                                                  'properties': {'used': {'const': False}}}},
                'traffic_filters': {'type': 'object',
                                    'required': ['internal',
                                                 'checkout_and_auth_domains',
                                                 'unwanted_referrals',
                                                 'cross_domain'],
                                    'additionalProperties': False,
                                    'properties': {'internal': {'type': 'object',
                                                                'required': ['ip_rules', 'state'],
                                                                'additionalProperties': False,
                                                                'properties': {'ip_rules': {'type': 'array',
                                                                                            'minItems': 1,
                                                                                            'items': {'type': 'string',
                                                                                                      'pattern': '^[0-9]{1,3}(\\.[0-9]{1,3}){3}(/[0-9]{1,2})?$'}},
                                                                               'state': {'const': 'active'}}},
                                                   'checkout_and_auth_domains': {'type': 'array',
                                                                                 'items': {'$ref': '#/definitions/host'}},
                                                   'unwanted_referrals': {'type': 'array',
                                                                          'items': {'$ref': '#/definitions/host'}},
                                                   'cross_domain': {'type': 'array',
                                                                    'items': {'$ref': '#/definitions/host'}}}}}}

OK = {'property_id': '123456789',
 'site_domain': 'example.com',
 'data_streams': [{'name': 'example.com web',
                   'type': 'web',
                   'measurement_id': 'G-AB12CD34EF',
                   'spa': True,
                   'manual_page_view': True,
                   'send_page_view': False}],
 'enhanced_measurement': {'page_views': True,
                          'history_change_page_view': False,
                          'scrolls': True,
                          'outbound_clicks': True,
                          'site_search': False,
                          'video_engagement': False,
                          'file_downloads': True,
                          'form_interactions': False},
 'custom_dimensions': {'limits': {'event': 50, 'user': 25, 'item': 10, 'metrics': 50},
                       'registered': [{'name': 'Plan tier',
                                       'parameter': 'plan_tier',
                                       'scope': 'user',
                                       'kind': 'dimension',
                                       'registered_before_first_send': True},
                                      {'name': 'Funnel name',
                                       'parameter': 'funnel_name',
                                       'scope': 'event',
                                       'kind': 'dimension',
                                       'registered_before_first_send': True},
                                      {'name': 'Step number',
                                       'parameter': 'step_number',
                                       'scope': 'event',
                                       'kind': 'dimension',
                                       'registered_before_first_send': True},
                                      {'name': 'Seats',
                                       'parameter': 'seats',
                                       'scope': 'event',
                                       'kind': 'metric',
                                       'registered_before_first_send': True}],
                       'used': {'event': 2, 'user': 1, 'item': 0, 'metrics': 1}},
 'events': ['page_view', 'sign_up', 'generate_lead', 'purchase', 'funnel_step', 'login'],
 'key_events': [{'event_name': 'purchase', 'counting': 'once_per_event'},
                {'event_name': 'generate_lead', 'counting': 'once_per_session'},
                {'event_name': 'sign_up', 'counting': 'once_per_event'}],
 'purchase': {'enabled': True,
              'required_parameters': ['transaction_id', 'value', 'currency', 'items'],
              'transaction_id_source': 'order_id',
              'stable_across_retries': True},
 'consent': {'in_scope': True,
             'implementation': 'advanced',
             'defaults_before_config': True,
             'signals': ['ad_storage', 'analytics_storage', 'ad_user_data', 'ad_personalization'],
             'regions': ['EU', 'GB', 'CH'],
             'update_on_choice': True},
 'bigquery_export': {'linked': True,
                     'linked_before_launch': True,
                     'linked_at': '2026-04-20',
                     'project': 'acme-analytics-prod',
                     'dataset_location': 'EU',
                     'daily': True,
                     'streaming': False,
                     'sampling_threshold_events': 10000000,
                     'decision_reports_source': 'bigquery'},
 'data_retention_months': 14,
 'measurement_protocol': {'used': True,
                          'client_id_source': '_ga cookie',
                          'session_id_included': True,
                          'engagement_time_msec_included': True,
                          'api_secret_storage': 'server_only',
                          'fresh_client_id': False},
 'traffic_filters': {'internal': {'ip_rules': ['203.0.113.0/24', '198.51.100.17'],
                                  'state': 'active'},
                     'checkout_and_auth_domains': ['paypal.com',
                                                   'checkout.stripe.com',
                                                   'auth.example.com'],
                     'unwanted_referrals': ['paypal.com',
                                            'checkout.stripe.com',
                                            'auth.example.com'],
                     'cross_domain': ['example.com', 'shop.example.com']}}

BAD = {'property_id': 'G-AB12CD34EF',
 'site_domain': 'example.com',
 'data_streams': [{'name': 'example.com web',
                   'type': 'web',
                   'measurement_id': '123456789',
                   'spa': True,
                   'manual_page_view': True,
                   'send_page_view': True}],
 'enhanced_measurement': {'page_views': True,
                          'history_change_page_view': True,
                          'scrolls': True,
                          'outbound_clicks': True,
                          'site_search': True,
                          'video_engagement': True,
                          'file_downloads': True,
                          'form_interactions': True},
 'custom_dimensions': {'limits': {'event': 50, 'user': 25, 'item': 10, 'metrics': 50},
                       'registered': [{'name': 'Plan tier',
                                       'parameter': 'plan_tier',
                                       'scope': 'event',
                                       'kind': 'dimension',
                                       'registered_before_first_send': False}],
                       'used': {'event': 52, 'user': 0, 'item': 0, 'metrics': 0}},
 'events': ['page_view', 'sign_up', 'purchase'],
 'key_events': [{'event_name': 'Purchase', 'counting': 'once_per_event'},
                {'event_name': 'lead', 'counting': 'once_per_session'}],
 'purchase': {'enabled': True,
              'required_parameters': ['value', 'currency'],
              'transaction_id_source': 'timestamp',
              'stable_across_retries': False},
 'consent': {'in_scope': True,
             'implementation': 'basic',
             'defaults_before_config': False,
             'signals': ['ad_storage', 'analytics_storage'],
             'regions': ['EU'],
             'update_on_choice': True},
 'bigquery_export': {'linked': False,
                     'linked_before_launch': False,
                     'linked_at': '2026-10-01',
                     'project': 'acme-analytics-prod',
                     'dataset_location': 'EU',
                     'daily': True,
                     'streaming': False,
                     'sampling_threshold_events': 10000000,
                     'decision_reports_source': 'explorations'},
 'data_retention_months': 2,
 'measurement_protocol': {'used': True,
                          'client_id_source': 'uuid4',
                          'session_id_included': False,
                          'engagement_time_msec_included': False,
                          'api_secret_storage': 'browser_bundle',
                          'fresh_client_id': True},
 'traffic_filters': {'internal': {'ip_rules': ['203.0.113.0/24'], 'state': 'testing'},
                     'checkout_and_auth_domains': ['paypal.com', 'auth.example.com'],
                     'unwanted_referrals': [],
                     'cross_domain': []}}


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

def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    em = obj.get("enhanced_measurement") or {}
    for i, s in enumerate(obj.get("data_streams") or []):
        if s.get("type") == "web" and s.get("spa"):
            if s.get("manual_page_view") and em.get("history_change_page_view"):
                errs.append(f"data_streams[{i}]: the app sends page_view manually and history_change_page_view is on; every screen counts twice (r-enhanced-measurement-declared-no-double-page-view)")
            if not s.get("manual_page_view") and not em.get("history_change_page_view"):
                errs.append(f"data_streams[{i}]: SPA stream with neither manual page_view nor history_change_page_view; route changes are not measured (r-enhanced-measurement-declared-no-double-page-view)")
    cd = obj.get("custom_dimensions") or {}
    reg = cd.get("registered") or []
    counts = {"event": 0, "user": 0, "item": 0, "metrics": 0}
    for r in reg:
        if r.get("kind") == "metric":
            counts["metrics"] += 1
        else:
            counts[r.get("scope", "event")] = counts.get(r.get("scope", "event"), 0) + 1
    used, limits = cd.get("used") or {}, cd.get("limits") or {}
    for k in counts:
        if used.get(k) != counts[k]:
            errs.append(f"custom_dimensions.used.{k} is {used.get(k)} but registered[] holds {counts[k]} (r-custom-dimensions-registered-within-limits)")
        if used.get(k, 0) > limits.get(k, 0):
            errs.append(f"custom_dimensions.used.{k} {used.get(k)} exceeds the plan limit {limits.get(k)} (r-custom-dimensions-registered-within-limits)")
    params = {r.get("parameter") for r in reg}
    if len(params) != len(reg):
        errs.append("custom_dimensions.registered has a duplicate parameter (r-custom-dimensions-registered-within-limits)")
    events = set(obj.get("events") or [])
    seen = set()
    for i, k in enumerate(obj.get("key_events") or []):
        n = k.get("event_name")
        if n not in events:
            errs.append(f"key_events[{i}]: {n!r} is not an event in events[]; the key event never fires (r-key-events-declared-by-exact-name)")
        if n in seen:
            errs.append(f"key_events[{i}]: {n!r} is marked twice (r-key-events-declared-by-exact-name)")
        seen.add(n)
    if (obj.get("purchase") or {}).get("enabled") and "purchase" not in events:
        errs.append("purchase is enabled but 'purchase' is not in events[] (r-purchase-transaction-id-dedup)")
    tf = obj.get("traffic_filters") or {}
    refs = set(tf.get("unwanted_referrals") or [])
    for d in tf.get("checkout_and_auth_domains") or []:
        if d not in refs:
            errs.append(f"traffic_filters: checkout or auth domain {d!r} is not in unwanted_referrals; returns from it start a new attributed session (r-internal-traffic-referral-and-cross-domain)")
    site = obj.get("site_domain", "")
    cross = tf.get("cross_domain") or []
    if cross and site not in cross:
        errs.append(f"traffic_filters.cross_domain does not include site_domain {site!r} (r-internal-traffic-referral-and-cross-domain)")
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
        prog="validate-google-analytics.py",
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
