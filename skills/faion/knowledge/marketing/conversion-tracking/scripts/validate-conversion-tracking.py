#!/usr/bin/env python3
"""validate-conversion-tracking.py

Validate the artefact produced by the conversion-tracking methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/conversion-tracking.json',
 'title': 'Conversion Tracking config',
 'type': 'object',
 'required': ['site_domain', 'destinations', 'registry', 'consent', 'server_side', 'events', 'qa'],
 'additionalProperties': False,
 'definitions': {'host': {'type': 'string', 'pattern': '^[a-z0-9.-]+\\.[a-z]{2,}$'},
                 'destination': {'type': 'string',
                                 'enum': ['ga4', 'google_ads', 'meta', 'plausible']},
                 'snake40': {'type': 'string',
                             'pattern': '^[a-z][a-z0-9_]{0,39}$',
                             'not': {'pattern': '^(google_|ga_|firebase_|_)'}},
                 'consent_value': {'type': 'string', 'enum': ['denied', 'granted']}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'site_domain': {'$ref': '#/definitions/host'},
                'destinations': {'type': 'array',
                                 'minItems': 1,
                                 'uniqueItems': True,
                                 'items': {'$ref': '#/definitions/destination'}},
                'registry': {'type': 'object',
                             'required': ['file', 'ci_validator', 'enforced_in_ci'],
                             'additionalProperties': False,
                             'properties': {'file': {'const': 'events.yml'},
                                            'ci_validator': {'const': 'validate-events.py'},
                                            'enforced_in_ci': {'const': True}}},
                'consent': {'type': 'object',
                            'required': ['mode',
                                         'defaults_before_config',
                                         'signals',
                                         'regional_defaults',
                                         'server_honours_consent'],
                            'additionalProperties': False,
                            'properties': {'mode': {'const': 'v2'},
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
                                           'regional_defaults': {'type': 'array',
                                                                 'minItems': 1,
                                                                 'items': {'type': 'object',
                                                                           'required': ['region',
                                                                                        'ad_storage',
                                                                                        'analytics_storage',
                                                                                        'ad_user_data',
                                                                                        'ad_personalization'],
                                                                           'additionalProperties': False,
                                                                           'properties': {'region': {'type': 'string',
                                                                                                     'pattern': '^[A-Z]{2}(-[A-Z0-9]{1,3})?$|^default$'},
                                                                                          'ad_storage': {'$ref': '#/definitions/consent_value'},
                                                                                          'analytics_storage': {'$ref': '#/definitions/consent_value'},
                                                                                          'ad_user_data': {'$ref': '#/definitions/consent_value'},
                                                                                          'ad_personalization': {'$ref': '#/definitions/consent_value'}}}},
                                           'server_honours_consent': {'const': True}}},
                'server_side': {'type': 'object',
                                'required': ['enabled'],
                                'properties': {'enabled': {'type': 'boolean'}},
                                'if': {'properties': {'enabled': {'const': True}}},
                                'then': {'required': ['endpoint',
                                                      'cookies_http_only',
                                                      'forwards',
                                                      'client_id_source',
                                                      'fresh_ids_generated'],
                                         'additionalProperties': False,
                                         'properties': {'enabled': {'const': True},
                                                        'endpoint': {'$ref': '#/definitions/host'},
                                                        'cookies_http_only': {'const': True},
                                                        'forwards': {'type': 'array',
                                                                     'minItems': 2,
                                                                     'items': {'type': 'string',
                                                                               'enum': ['_fbp',
                                                                                        '_fbc',
                                                                                        'client_id',
                                                                                        'session_id']},
                                                                     'allOf': [{'contains': {'const': 'client_id'}},
                                                                               {'contains': {'const': 'session_id'}}]},
                                                        'client_id_source': {'const': '_ga cookie'},
                                                        'fresh_ids_generated': {'const': False}}},
                                'else': {'additionalProperties': False,
                                         'properties': {'enabled': {'const': False}}}},
                'events': {'type': 'array',
                           'minItems': 1,
                           'items': {'type': 'object',
                                     'required': ['name',
                                                  'recommended',
                                                  'parameters',
                                                  'conversion_role',
                                                  'monetary',
                                                  'sent_from'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'$ref': '#/definitions/snake40'},
                                                    'recommended': {'type': 'boolean'},
                                                    'parameters': {'type': 'array',
                                                                   'maxItems': 25,
                                                                   'items': {'type': 'object',
                                                                             'required': ['name',
                                                                                          'type',
                                                                                          'pii'],
                                                                             'additionalProperties': False,
                                                                             'properties': {'name': {'$ref': '#/definitions/snake40'},
                                                                                            'type': {'type': 'string',
                                                                                                     'enum': ['string',
                                                                                                              'number',
                                                                                                              'currency',
                                                                                                              'boolean',
                                                                                                              'array']},
                                                                                            'max_string_length': {'type': 'integer',
                                                                                                                  'minimum': 1,
                                                                                                                  'maximum': 100},
                                                                                            'pii': {'const': False},
                                                                                            'hashed': {'type': 'boolean'}}}},
                                                    'conversion_role': {'type': 'object',
                                                                        'additionalProperties': False,
                                                                        'properties': {'ga4': {'type': ['string',
                                                                                                        'null'],
                                                                                               'enum': ['key_event',
                                                                                                        'event',
                                                                                                        None]},
                                                                                       'google_ads': {'type': ['string',
                                                                                                               'null'],
                                                                                                      'enum': ['primary',
                                                                                                               'secondary',
                                                                                                               None]},
                                                                                       'meta': {'type': ['string',
                                                                                                         'null'],
                                                                                                'enum': ['standard',
                                                                                                         'custom',
                                                                                                         None]},
                                                                                       'plausible': {'type': ['string',
                                                                                                              'null'],
                                                                                                     'enum': ['goal',
                                                                                                              'event',
                                                                                                              None]}}},
                                                    'monetary': {'type': 'boolean'},
                                                    'sent_from': {'type': 'array',
                                                                  'minItems': 1,
                                                                  'uniqueItems': True,
                                                                  'items': {'type': 'string',
                                                                            'enum': ['browser',
                                                                                     'server']}},
                                                    'dedup': {'type': 'object',
                                                              'required': ['event_id_field',
                                                                           'shared_across_destinations'],
                                                              'additionalProperties': False,
                                                              'properties': {'event_id_field': {'$ref': '#/definitions/snake40'},
                                                                             'shared_across_destinations': {'const': True}}}},
                                     'allOf': [{'if': {'properties': {'monetary': {'const': True}}},
                                                'then': {'required': ['dedup'],
                                                         'properties': {'dedup': {'properties': {'event_id_field': {'const': 'transaction_id'}}}}}},
                                               {'if': {'properties': {'sent_from': {'minItems': 2}}},
                                                'then': {'required': ['dedup']}}]}},
                'qa': {'type': 'object',
                       'required': ['change_ref', 'browsers', 'adblock_profile', 'fixtures'],
                       'additionalProperties': False,
                       'properties': {'change_ref': {'type': 'string', 'minLength': 3},
                                      'browsers': {'type': 'array',
                                                   'minItems': 3,
                                                   'items': {'type': 'string',
                                                             'enum': ['chrome',
                                                                      'safari',
                                                                      'firefox']},
                                                   'allOf': [{'contains': {'const': 'chrome'}},
                                                             {'contains': {'const': 'safari'}},
                                                             {'contains': {'const': 'firefox'}}]},
                                      'adblock_profile': {'const': True},
                                      'fixtures': {'type': 'array',
                                                   'minItems': 1,
                                                   'items': {'type': 'object',
                                                             'required': ['event',
                                                                          'expected_parameters',
                                                                          'example_payload',
                                                                          'results'],
                                                             'additionalProperties': False,
                                                             'properties': {'event': {'$ref': '#/definitions/snake40'},
                                                                            'expected_parameters': {'type': 'array',
                                                                                                    'items': {'$ref': '#/definitions/snake40'}},
                                                                            'example_payload': {'type': 'object'},
                                                                            'results': {'type': 'array',
                                                                                        'minItems': 4,
                                                                                        'items': {'type': 'object',
                                                                                                  'required': ['browser',
                                                                                                               'destination',
                                                                                                               'seen'],
                                                                                                  'additionalProperties': False,
                                                                                                  'properties': {'browser': {'type': 'string',
                                                                                                                             'enum': ['chrome',
                                                                                                                                      'safari',
                                                                                                                                      'firefox',
                                                                                                                                      'chrome_adblock']},
                                                                                                                 'destination': {'$ref': '#/definitions/destination'},
                                                                                                                 'seen': {'type': 'boolean'}}}}}}}}}}}

OK = {'site_domain': 'example.com',
 'destinations': ['ga4', 'google_ads', 'meta'],
 'registry': {'file': 'events.yml', 'ci_validator': 'validate-events.py', 'enforced_in_ci': True},
 'consent': {'mode': 'v2',
             'defaults_before_config': True,
             'signals': ['ad_storage', 'analytics_storage', 'ad_user_data', 'ad_personalization'],
             'regional_defaults': [{'region': 'default',
                                    'ad_storage': 'granted',
                                    'analytics_storage': 'granted',
                                    'ad_user_data': 'granted',
                                    'ad_personalization': 'granted'},
                                   {'region': 'EU',
                                    'ad_storage': 'denied',
                                    'analytics_storage': 'denied',
                                    'ad_user_data': 'denied',
                                    'ad_personalization': 'denied'},
                                   {'region': 'GB',
                                    'ad_storage': 'denied',
                                    'analytics_storage': 'denied',
                                    'ad_user_data': 'denied',
                                    'ad_personalization': 'denied'}],
             'server_honours_consent': True},
 'server_side': {'enabled': True,
                 'endpoint': 'gtm.example.com',
                 'cookies_http_only': True,
                 'forwards': ['_fbp', '_fbc', 'client_id', 'session_id'],
                 'client_id_source': '_ga cookie',
                 'fresh_ids_generated': False},
 'events': [{'name': 'purchase',
             'recommended': True,
             'monetary': True,
             'sent_from': ['browser', 'server'],
             'parameters': [{'name': 'transaction_id',
                             'type': 'string',
                             'max_string_length': 64,
                             'pii': False},
                            {'name': 'value', 'type': 'number', 'pii': False},
                            {'name': 'currency', 'type': 'currency', 'pii': False},
                            {'name': 'items', 'type': 'array', 'pii': False},
                            {'name': 'coupon',
                             'type': 'string',
                             'max_string_length': 40,
                             'pii': False}],
             'conversion_role': {'ga4': 'key_event', 'google_ads': 'primary', 'meta': 'standard'},
             'dedup': {'event_id_field': 'transaction_id', 'shared_across_destinations': True}},
            {'name': 'sign_up',
             'recommended': True,
             'monetary': False,
             'sent_from': ['browser', 'server'],
             'parameters': [{'name': 'method',
                             'type': 'string',
                             'max_string_length': 20,
                             'pii': False},
                            {'name': 'event_id',
                             'type': 'string',
                             'max_string_length': 36,
                             'pii': False},
                            {'name': 'em',
                             'type': 'string',
                             'max_string_length': 64,
                             'pii': False,
                             'hashed': True}],
             'conversion_role': {'ga4': 'key_event', 'google_ads': 'secondary', 'meta': 'standard'},
             'dedup': {'event_id_field': 'event_id', 'shared_across_destinations': True}},
            {'name': 'funnel_step',
             'recommended': False,
             'monetary': False,
             'sent_from': ['browser'],
             'parameters': [{'name': 'funnel_name',
                             'type': 'string',
                             'max_string_length': 40,
                             'pii': False},
                            {'name': 'step_number', 'type': 'number', 'pii': False},
                            {'name': 'step_name',
                             'type': 'string',
                             'max_string_length': 40,
                             'pii': False}],
             'conversion_role': {'ga4': 'event', 'google_ads': None, 'meta': None}}],
 'qa': {'change_ref': 'PR-2214 checkout tracking v3',
        'browsers': ['chrome', 'safari', 'firefox'],
        'adblock_profile': True,
        'fixtures': [{'event': 'purchase',
                      'expected_parameters': ['transaction_id', 'value', 'currency', 'items'],
                      'example_payload': {'transaction_id': 'ORD-104233',
                                          'value': 129.0,
                                          'currency': 'EUR',
                                          'items': [{'item_id': 'SKU-88', 'quantity': 1}]},
                      'results': [{'browser': 'chrome', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'chrome', 'destination': 'google_ads', 'seen': True},
                                  {'browser': 'chrome', 'destination': 'meta', 'seen': True},
                                  {'browser': 'safari', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'safari', 'destination': 'google_ads', 'seen': True},
                                  {'browser': 'safari', 'destination': 'meta', 'seen': True},
                                  {'browser': 'firefox', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'firefox', 'destination': 'google_ads', 'seen': True},
                                  {'browser': 'firefox', 'destination': 'meta', 'seen': True},
                                  {'browser': 'chrome_adblock', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'chrome_adblock',
                                   'destination': 'google_ads',
                                   'seen': True},
                                  {'browser': 'chrome_adblock',
                                   'destination': 'meta',
                                   'seen': True}]},
                     {'event': 'sign_up',
                      'expected_parameters': ['method', 'event_id'],
                      'example_payload': {'method': 'google',
                                          'event_id': '5f2a1c9e-3b7d-4e1a-9c6b-2d8e7f1a0b3c',
                                          'em': 'b4c9a289323b21a01c3e940f150eb9b8c542587f1abfd8f0e1cc1ffc5e475514'},
                      'results': [{'browser': 'chrome', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'chrome', 'destination': 'google_ads', 'seen': True},
                                  {'browser': 'chrome', 'destination': 'meta', 'seen': True},
                                  {'browser': 'safari', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'safari', 'destination': 'google_ads', 'seen': True},
                                  {'browser': 'safari', 'destination': 'meta', 'seen': True},
                                  {'browser': 'firefox', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'firefox', 'destination': 'google_ads', 'seen': True},
                                  {'browser': 'firefox', 'destination': 'meta', 'seen': True},
                                  {'browser': 'chrome_adblock', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'chrome_adblock',
                                   'destination': 'google_ads',
                                   'seen': True},
                                  {'browser': 'chrome_adblock',
                                   'destination': 'meta',
                                   'seen': True}]},
                     {'event': 'funnel_step',
                      'expected_parameters': ['funnel_name', 'step_number', 'step_name'],
                      'example_payload': {'funnel_name': 'checkout',
                                          'step_number': 2,
                                          'step_name': 'shipping_info'},
                      'results': [{'browser': 'chrome', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'safari', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'firefox', 'destination': 'ga4', 'seen': True},
                                  {'browser': 'chrome_adblock',
                                   'destination': 'ga4',
                                   'seen': False}]}]}}

BAD = {'site_domain': 'example.com',
 'destinations': ['ga4', 'google_ads', 'meta'],
 'registry': {'file': 'events.yml', 'ci_validator': 'validate-events.py', 'enforced_in_ci': False},
 'consent': {'mode': 'v2',
             'defaults_before_config': False,
             'signals': ['ad_storage', 'analytics_storage'],
             'regional_defaults': [{'region': 'default',
                                    'ad_storage': 'granted',
                                    'analytics_storage': 'granted',
                                    'ad_user_data': 'granted',
                                    'ad_personalization': 'granted'}],
             'server_honours_consent': False},
 'server_side': {'enabled': True,
                 'endpoint': 'gtm-server.vendor.app',
                 'cookies_http_only': False,
                 'forwards': ['client_id'],
                 'client_id_source': 'uuid4 per hit',
                 'fresh_ids_generated': True},
 'events': [{'name': 'Order_Completed',
             'recommended': False,
             'monetary': True,
             'sent_from': ['browser', 'server'],
             'parameters': [{'name': 'value', 'type': 'number', 'pii': False},
                            {'name': 'email',
                             'type': 'string',
                             'max_string_length': 100,
                             'pii': True}],
             'conversion_role': {'ga4': 'key_event', 'google_ads': 'primary', 'meta': 'custom'}},
            {'name': 'checkout_step_completed_with_shipping_option_selected',
             'recommended': False,
             'monetary': False,
             'sent_from': ['browser'],
             'parameters': [],
             'conversion_role': {'ga4': 'event'}}],
 'qa': {'change_ref': 'hotfix',
        'browsers': ['chrome'],
        'adblock_profile': False,
        'fixtures': [{'event': 'Order_Completed',
                      'expected_parameters': ['value'],
                      'example_payload': {'value': 129.0,
                                          'email': 'jane.doe@example.com',
                                          'phone': '+44 7700 900123'},
                      'results': [{'browser': 'chrome', 'destination': 'ga4', 'seen': True}]}]}}


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

_SYNONYMS = {"order_completed": "purchase", "checkout_complete": "purchase", "transaction": "purchase", "signup": "sign_up", "register": "sign_up", "registration": "sign_up", "lead": "generate_lead", "add_cart": "add_to_cart", "cart_add": "add_to_cart"}
_PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")


def _strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from _strings(x)


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    site = obj.get("site_domain", "")
    dests = set(obj.get("destinations") or [])
    ss = obj.get("server_side") or {}
    if ss.get("enabled"):
        ep = ss.get("endpoint", "")
        if not ep.endswith("." + site):
            errs.append(f"server_side.endpoint {ep!r} is not a first-party subdomain of {site!r} (r-server-endpoint-first-party-domain)")
        if "meta" in dests and not {"_fbp", "_fbc"} <= set(ss.get("forwards") or []):
            errs.append("server_side.forwards must include _fbp and _fbc when meta is a destination (r-browser-server-dedup-and-identifiers)")
    events = {e.get("name"): e for e in obj.get("events") or [] if isinstance(e, dict)}
    for i, e in enumerate(obj.get("events") or []):
        name = e.get("name", "")
        if name in _SYNONYMS:
            errs.append(f"events[{i}]: {name!r} is a synonym of the recommended event {_SYNONYMS[name]!r}; use the exact recommended name (r-ga4-naming-and-parameter-limits)")
        pnames = {p.get("name") for p in e.get("parameters") or []}
        if e.get("monetary"):
            for req in ("value", "currency", "transaction_id"):
                if req not in pnames:
                    errs.append(f"events[{i}]: monetary event {name!r} lacks parameter {req!r} (r-monetary-conversion-carries-transaction-id)")
        if "server" in (e.get("sent_from") or []) and not ss.get("enabled"):
            errs.append(f"events[{i}]: {name!r} is sent from the server but server_side.enabled is false (r-browser-server-dedup-and-identifiers)")
        dd = e.get("dedup") or {}
        if dd and dd.get("event_id_field") not in pnames:
            errs.append(f"events[{i}]: dedup.event_id_field {dd.get('event_id_field')!r} is not a parameter of {name!r} (r-browser-server-dedup-and-identifiers)")
        for p in e.get("parameters") or []:
            if p.get("name") in ("em", "ph", "email_hash", "phone_hash") and p.get("hashed") is not True:
                errs.append(f"events[{i}]: matching identifier {p.get('name')!r} must be SHA-256 hashed (r-no-pii-in-parameters)")
        for role_dest in (e.get("conversion_role") or {}):
            if role_dest not in dests and (e.get("conversion_role") or {}).get(role_dest) is not None:
                errs.append(f"events[{i}]: conversion_role names {role_dest!r}, which is not in destinations (r-event-registry-single-source)")
    qa = obj.get("qa") or {}
    fx = {f.get("event"): f for f in qa.get("fixtures") or [] if isinstance(f, dict)}
    for name in events:
        if name not in fx:
            errs.append(f"qa.fixtures: no fixture for event {name!r} (r-qa-fixtures-per-tracking-change)")
    for i, f in enumerate(qa.get("fixtures") or []):
        ev = events.get(f.get("event"))
        if ev is None:
            errs.append(f"qa.fixtures[{i}]: event {f.get('event')!r} is not in events[] (r-event-registry-single-source)")
            continue
        pnames = {p.get("name") for p in ev.get("parameters") or []}
        for p in f.get("expected_parameters") or []:
            if p not in pnames:
                errs.append(f"qa.fixtures[{i}]: expected parameter {p!r} is not declared on {ev.get('name')!r} (r-event-registry-single-source)")
        for s in _strings(f.get("example_payload") or {}):
            if "@" in s or _PHONE.search(s):
                errs.append(f"qa.fixtures[{i}]: example_payload contains an email or phone-shaped value {s!r} (r-no-pii-in-parameters)")
        targets = {d for d, role in (ev.get("conversion_role") or {}).items() if role is not None} or dests
        seen = {(r.get("browser"), r.get("destination")) for r in f.get("results") or []}
        for b in ("chrome", "safari", "firefox", "chrome_adblock"):
            for d in sorted(targets):
                if (b, d) not in seen:
                    errs.append(f"qa.fixtures[{i}]: no result for {b} x {d} (r-qa-fixtures-per-tracking-change)")
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
        prog="validate-conversion-tracking.py",
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
