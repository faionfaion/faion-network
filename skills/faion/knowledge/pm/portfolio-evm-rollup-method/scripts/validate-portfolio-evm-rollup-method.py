#!/usr/bin/env python3
"""validate-portfolio-evm-rollup-method.py

Validate the artefact produced by the portfolio-evm-rollup-method methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/portfolio-evm-rollup-method.json',
 'title': 'Portfolio EVM rollup',
 'type': 'object',
 'required': ['portfolio',
              'owner',
              'data_date',
              'currency',
              'reporting_period',
              'executive_review_date',
              'variance_thresholds',
              'weighting',
              'projects',
              'stale_projects',
              'aggregate',
              'executive_summary',
              'owner_sign_off'],
 'additionalProperties': False,
 'definitions': {'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'timestamp': {'type': 'string',
                               'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2})?(Z|[+-][0-9]{2}:[0-9]{2})$'},
                 'money': {'type': 'number'},
                 'index': {'type': 'number', 'minimum': 0},
                 'trend': {'type': 'array',
                           'minItems': 3,
                           'items': {'type': 'object',
                                     'required': ['data_date', 'spi', 'cpi'],
                                     'additionalProperties': False,
                                     'properties': {'data_date': {'$ref': '#/definitions/date'},
                                                    'spi': {'$ref': '#/definitions/index'},
                                                    'cpi': {'$ref': '#/definitions/index'}}}},
                 'sums': {'type': 'object',
                          'required': ['bac', 'pv', 'ev', 'ac'],
                          'properties': {'bac': {'$ref': '#/definitions/money'},
                                         'pv': {'$ref': '#/definitions/money'},
                                         'ev': {'$ref': '#/definitions/money'},
                                         'ac': {'$ref': '#/definitions/money'}}}},
 'properties': {'__faion_header__': {'type': 'object'},
                'portfolio': {'type': 'string', 'minLength': 2},
                'owner': {'$ref': '#/definitions/handle'},
                'data_date': {'$ref': '#/definitions/date'},
                'currency': {'type': 'string', 'pattern': '^[A-Z]{3}$'},
                'reporting_period': {'type': 'string', 'enum': ['week', 'fortnight', 'month']},
                'executive_review_date': {'$ref': '#/definitions/date'},
                'variance_thresholds': {'type': 'object',
                                        'required': ['spi_min',
                                                     'cpi_min',
                                                     'cv_pct_of_bac_max',
                                                     'policy_source'],
                                        'additionalProperties': False,
                                        'properties': {'spi_min': {'type': 'number',
                                                                   'exclusiveMinimum': 0,
                                                                   'maximum': 1},
                                                       'cpi_min': {'type': 'number',
                                                                   'exclusiveMinimum': 0,
                                                                   'maximum': 1},
                                                       'cv_pct_of_bac_max': {'type': 'number',
                                                                             'exclusiveMinimum': 0,
                                                                             'maximum': 100},
                                                       'policy_source': {'type': 'string',
                                                                         'minLength': 3}}},
                'weighting': {'type': 'object',
                              'required': ['policy'],
                              'additionalProperties': False,
                              'properties': {'policy': {'type': 'string',
                                                        'enum': ['currency-sum',
                                                                 'strategic',
                                                                 'margin',
                                                                 'client-tier']},
                                             'policy_document': {'type': 'string', 'minLength': 3}},
                              'if': {'properties': {'policy': {'enum': ['strategic',
                                                                        'margin',
                                                                        'client-tier']}}},
                              'then': {'required': ['policy', 'policy_document']}},
                'projects': {'type': 'array',
                             'minItems': 3,
                             'items': {'type': 'object',
                                       'required': ['name',
                                                    'contract_type',
                                                    'ev_method',
                                                    'ledger_file',
                                                    'ledger_exported_at',
                                                    'data_date',
                                                    'currency',
                                                    'bac',
                                                    'pv',
                                                    'ev',
                                                    'ac',
                                                    'sv',
                                                    'cv',
                                                    'spi',
                                                    'cpi',
                                                    'eac',
                                                    'vac',
                                                    'eac_formula',
                                                    'trend'],
                                       'additionalProperties': False,
                                       'properties': {'name': {'type': 'string', 'minLength': 2},
                                                      'contract_type': {'type': 'string',
                                                                        'enum': ['fixed-bid',
                                                                                 'time-and-materials',
                                                                                 'internal']},
                                                      'ev_method': {'type': 'string',
                                                                    'enum': ['milestone-weight',
                                                                             '0/100',
                                                                             '50/50',
                                                                             'physical-percent-complete',
                                                                             'apportioned-effort',
                                                                             'level-of-effort']},
                                                      'ledger_file': {'type': 'string',
                                                                      'minLength': 3},
                                                      'ledger_exported_at': {'$ref': '#/definitions/timestamp'},
                                                      'data_date': {'$ref': '#/definitions/date'},
                                                      'currency': {'type': 'string',
                                                                   'pattern': '^[A-Z]{3}$'},
                                                      'bac': {'type': 'number',
                                                              'exclusiveMinimum': 0},
                                                      'pv': {'$ref': '#/definitions/money'},
                                                      'ev': {'$ref': '#/definitions/money'},
                                                      'ac': {'$ref': '#/definitions/money'},
                                                      'sv': {'$ref': '#/definitions/money'},
                                                      'cv': {'$ref': '#/definitions/money'},
                                                      'spi': {'$ref': '#/definitions/index'},
                                                      'cpi': {'$ref': '#/definitions/index'},
                                                      'eac': {'$ref': '#/definitions/money'},
                                                      'vac': {'$ref': '#/definitions/money'},
                                                      'eac_formula': {'type': 'string',
                                                                      'enum': ['BAC/CPI',
                                                                               'AC+(BAC-EV)/(CPI*SPI)',
                                                                               'bottom-up']},
                                                      'weight': {'type': 'number',
                                                                 'exclusiveMinimum': 0},
                                                      'contract_value': {'type': 'number',
                                                                         'exclusiveMinimum': 0},
                                                      'implied_margin': {'$ref': '#/definitions/money'},
                                                      'trend': {'$ref': '#/definitions/trend'},
                                                      'variance_narrative': {'type': 'object',
                                                                             'required': ['cause',
                                                                                          'corrective_action'],
                                                                             'additionalProperties': False,
                                                                             'properties': {'cause': {'type': 'string',
                                                                                                      'minLength': 12},
                                                                                            'corrective_action': {'type': 'string',
                                                                                                                  'minLength': 12}}}},
                                       'allOf': [{'if': {'properties': {'contract_type': {'const': 'fixed-bid'}}},
                                                  'then': {'required': ['contract_value',
                                                                        'implied_margin'],
                                                           'properties': {'ev_method': {'enum': ['milestone-weight',
                                                                                                 '0/100',
                                                                                                 '50/50']}}}}]}},
                'stale_projects': {'type': 'array',
                                   'items': {'type': 'object',
                                             'required': ['name',
                                                          'bac',
                                                          'last_data_date',
                                                          'ledger_exported_at'],
                                             'additionalProperties': False,
                                             'properties': {'name': {'type': 'string',
                                                                     'minLength': 2},
                                                            'bac': {'type': 'number',
                                                                    'exclusiveMinimum': 0},
                                                            'last_data_date': {'$ref': '#/definitions/date'},
                                                            'ledger_exported_at': {'$ref': '#/definitions/timestamp'}}}},
                'aggregate': {'type': 'object',
                              'required': ['discrete', 'loe', 'trend'],
                              'additionalProperties': False,
                              'properties': {'discrete': {'allOf': [{'$ref': '#/definitions/sums'}],
                                                          'required': ['bac',
                                                                       'pv',
                                                                       'ev',
                                                                       'ac',
                                                                       'spi',
                                                                       'cpi',
                                                                       'eac',
                                                                       'vac'],
                                                          'properties': {'spi': {'$ref': '#/definitions/index'},
                                                                         'cpi': {'$ref': '#/definitions/index'},
                                                                         'eac': {'$ref': '#/definitions/money'},
                                                                         'vac': {'$ref': '#/definitions/money'}}},
                                             'loe': {'$ref': '#/definitions/sums'},
                                             'weighted': {'type': 'object',
                                                          'required': ['spi', 'cpi', 'eac'],
                                                          'additionalProperties': False,
                                                          'properties': {'spi': {'$ref': '#/definitions/index'},
                                                                         'cpi': {'$ref': '#/definitions/index'},
                                                                         'eac': {'$ref': '#/definitions/money'}}},
                                             'trend': {'$ref': '#/definitions/trend'}}},
                'executive_summary': {'type': 'object',
                                      'required': ['bac',
                                                   'eac',
                                                   'vac',
                                                   'fixed_bid_margin_total',
                                                   'escalated_projects'],
                                      'additionalProperties': False,
                                      'properties': {'bac': {'$ref': '#/definitions/money'},
                                                     'eac': {'$ref': '#/definitions/money'},
                                                     'vac': {'$ref': '#/definitions/money'},
                                                     'fixed_bid_margin_total': {'$ref': '#/definitions/money'},
                                                     'escalated_projects': {'type': 'array',
                                                                            'items': {'type': 'string',
                                                                                      'minLength': 2},
                                                                            'uniqueItems': True}}},
                'owner_sign_off': {'type': 'object',
                                   'required': ['signed_by', 'signed_at'],
                                   'additionalProperties': False,
                                   'properties': {'signed_by': {'$ref': '#/definitions/handle'},
                                                  'signed_at': {'$ref': '#/definitions/date'}}}}}

OK = {'portfolio': 'delivery-2026',
 'owner': 'portfolio:dana',
 'data_date': '2026-08-31',
 'currency': 'USD',
 'reporting_period': 'month',
 'executive_review_date': '2026-09-08',
 'variance_thresholds': {'spi_min': 0.9,
                         'cpi_min': 0.9,
                         'cv_pct_of_bac_max': 10,
                         'policy_source': 'portfolio-runbook.md#variance-thresholds'},
 'weighting': {'policy': 'strategic', 'policy_document': 'portfolio-weighting-policy-2026.md'},
 'projects': [{'name': 'atlas-crm',
               'contract_type': 'fixed-bid',
               'ev_method': 'milestone-weight',
               'ledger_file': 'ledgers/atlas-crm-2026-08.csv',
               'ledger_exported_at': '2026-09-01T08:10:00Z',
               'data_date': '2026-08-31',
               'currency': 'USD',
               'bac': 1200000,
               'pv': 600000,
               'ev': 540000,
               'ac': 600000,
               'sv': -60000,
               'cv': -60000,
               'spi': 0.9,
               'cpi': 0.9,
               'eac': 1333333,
               'vac': -133333,
               'eac_formula': 'BAC/CPI',
               'weight': 1.0,
               'contract_value': 1400000,
               'implied_margin': 66667,
               'trend': [{'data_date': '2026-06-30', 'spi': 0.96, 'cpi': 0.94},
                         {'data_date': '2026-07-31', 'spi': 0.92, 'cpi': 0.91},
                         {'data_date': '2026-08-31', 'spi': 0.9, 'cpi': 0.9}]},
              {'name': 'hermes-billing',
               'contract_type': 'fixed-bid',
               'ev_method': '0/100',
               'ledger_file': 'ledgers/hermes-billing-2026-08.csv',
               'ledger_exported_at': '2026-09-01T09:02:00Z',
               'data_date': '2026-08-31',
               'currency': 'USD',
               'bac': 800000,
               'pv': 500000,
               'ev': 400000,
               'ac': 500000,
               'sv': -100000,
               'cv': -100000,
               'spi': 0.8,
               'cpi': 0.8,
               'eac': 1000000,
               'vac': -200000,
               'eac_formula': 'BAC/CPI',
               'weight': 1.5,
               'contract_value': 900000,
               'implied_margin': -100000,
               'trend': [{'data_date': '2026-06-30', 'spi': 0.95, 'cpi': 0.93},
                         {'data_date': '2026-07-31', 'spi': 0.88, 'cpi': 0.86},
                         {'data_date': '2026-08-31', 'spi': 0.8, 'cpi': 0.8}],
               'variance_narrative': {'cause': 'Invoicing milestone M4 slipped six weeks: the '
                                               "client's ERP sandbox was delivered late and 0/100 "
                                               'earns nothing until acceptance.',
                                      'corrective_action': 'Descope the reconciliation report to a '
                                                           'change request (+120k contract value) '
                                                           'and re-baseline M4 to 2026-10-15; '
                                                           'portfolio owner to confirm with the '
                                                           'account lead by 2026-09-12.'}},
              {'name': 'orion-platform',
               'contract_type': 'time-and-materials',
               'ev_method': 'physical-percent-complete',
               'ledger_file': 'ledgers/orion-platform-2026-08.csv',
               'ledger_exported_at': '2026-09-01T07:45:00Z',
               'data_date': '2026-08-31',
               'currency': 'USD',
               'bac': 2000000,
               'pv': 1000000,
               'ev': 1050000,
               'ac': 1000000,
               'sv': 50000,
               'cv': 50000,
               'spi': 1.05,
               'cpi': 1.05,
               'eac': 1904762,
               'vac': 95238,
               'eac_formula': 'BAC/CPI',
               'weight': 1.0,
               'trend': [{'data_date': '2026-06-30', 'spi': 1.02, 'cpi': 1.03},
                         {'data_date': '2026-07-31', 'spi': 1.04, 'cpi': 1.04},
                         {'data_date': '2026-08-31', 'spi': 1.05, 'cpi': 1.05}]},
              {'name': 'ops-support',
               'contract_type': 'internal',
               'ev_method': 'level-of-effort',
               'ledger_file': 'ledgers/ops-support-2026-08.csv',
               'ledger_exported_at': '2026-09-01T08:30:00Z',
               'data_date': '2026-08-31',
               'currency': 'USD',
               'bac': 300000,
               'pv': 150000,
               'ev': 150000,
               'ac': 160000,
               'sv': 0,
               'cv': -10000,
               'spi': 1.0,
               'cpi': 0.94,
               'eac': 320000,
               'vac': -20000,
               'eac_formula': 'BAC/CPI',
               'weight': 1.0,
               'trend': [{'data_date': '2026-06-30', 'spi': 1.0, 'cpi': 0.97},
                         {'data_date': '2026-07-31', 'spi': 1.0, 'cpi': 0.95},
                         {'data_date': '2026-08-31', 'spi': 1.0, 'cpi': 0.94}]}],
 'stale_projects': [{'name': 'zeus-mobile',
                     'bac': 500000,
                     'last_data_date': '2026-06-30',
                     'ledger_exported_at': '2026-07-02T10:00:00Z'}],
 'aggregate': {'discrete': {'bac': 4000000,
                            'pv': 2100000,
                            'ev': 1990000,
                            'ac': 2100000,
                            'spi': 0.95,
                            'cpi': 0.95,
                            'eac': 4238095,
                            'vac': -238095},
               'loe': {'bac': 300000, 'pv': 150000, 'ev': 150000, 'ac': 160000},
               'weighted': {'spi': 0.93, 'cpi': 0.93, 'eac': 4738095},
               'trend': [{'data_date': '2026-06-30', 'spi': 0.99, 'cpi': 0.98},
                         {'data_date': '2026-07-31', 'spi': 0.97, 'cpi': 0.96},
                         {'data_date': '2026-08-31', 'spi': 0.95, 'cpi': 0.95}]},
 'executive_summary': {'bac': 4300000,
                       'eac': 4558095,
                       'vac': -258095,
                       'fixed_bid_margin_total': -33333,
                       'escalated_projects': ['hermes-billing']},
 'owner_sign_off': {'signed_by': 'portfolio:dana', 'signed_at': '2026-09-04'}}

BAD = {'portfolio': 'delivery-2026',
 'owner': 'portfolio:dana',
 'data_date': '2026-08-31',
 'currency': 'USD',
 'reporting_period': 'month',
 'executive_review_date': '2026-09-08',
 'variance_thresholds': {'spi_min': 0.9,
                         'cpi_min': 0.9,
                         'cv_pct_of_bac_max': 10,
                         'policy_source': 'portfolio-runbook.md#variance-thresholds'},
 'weighting': {'policy': 'strategic'},
 'projects': [{'name': 'atlas-crm',
               'contract_type': 'fixed-bid',
               'ev_method': 'physical-percent-complete',
               'ledger_file': 'ledgers/atlas-crm-2026-08.csv',
               'ledger_exported_at': '2026-09-01T08:10:00Z',
               'data_date': '2026-08-31',
               'currency': 'USD',
               'bac': 1200000,
               'pv': 600000,
               'ev': 1080000,
               'ac': 600000,
               'sv': 480000,
               'cv': 480000,
               'spi': 1.8,
               'cpi': 1.8,
               'eac': 666667,
               'vac': 533333,
               'eac_formula': 'BAC/CPI',
               'contract_value': 1400000,
               'implied_margin': 733333,
               'trend': [{'data_date': '2026-08-31', 'spi': 1.8, 'cpi': 1.8}]},
              {'name': 'hermes-billing',
               'contract_type': 'fixed-bid',
               'ev_method': '0/100',
               'ledger_file': 'ledgers/hermes-billing-2026-08.csv',
               'ledger_exported_at': '2026-09-01T09:02:00Z',
               'data_date': '2026-08-31',
               'currency': 'USD',
               'bac': 800000,
               'pv': 500000,
               'ev': 400000,
               'ac': 500000,
               'sv': -100000,
               'cv': -100000,
               'spi': 0.8,
               'cpi': 0.8,
               'eac': 1000000,
               'vac': -200000,
               'eac_formula': 'BAC/CPI',
               'contract_value': 900000,
               'implied_margin': -100000,
               'trend': [{'data_date': '2026-08-31', 'spi': 0.8, 'cpi': 0.8}]},
              {'name': 'zeus-mobile',
               'contract_type': 'time-and-materials',
               'ev_method': 'physical-percent-complete',
               'ledger_file': 'ledgers/zeus-mobile-2026-06.csv',
               'ledger_exported_at': '2026-07-02T10:00:00Z',
               'data_date': '2026-06-30',
               'currency': 'USD',
               'bac': 500000,
               'pv': 200000,
               'ev': 200000,
               'ac': 200000,
               'sv': 0,
               'cv': 0,
               'spi': 1.0,
               'cpi': 1.0,
               'eac': 500000,
               'vac': 0,
               'eac_formula': 'BAC/CPI',
               'trend': [{'data_date': '2026-06-30', 'spi': 1.0, 'cpi': 1.0}]}],
 'stale_projects': [],
 'aggregate': {'discrete': {'bac': 2500000,
                            'pv': 1300000,
                            'ev': 1680000,
                            'ac': 1300000,
                            'spi': 1.2,
                            'cpi': 1.2,
                            'eac': 2166667,
                            'vac': 333333},
               'loe': {'bac': 0, 'pv': 0, 'ev': 0, 'ac': 0},
               'trend': [{'data_date': '2026-08-31', 'spi': 1.2, 'cpi': 1.2}]},
 'executive_summary': {'bac': 2500000,
                       'eac': 2166667,
                       'vac': 333333,
                       'fixed_bid_margin_total': 633333,
                       'escalated_projects': []},
 'owner_sign_off': {'signed_by': 'portfolio:dana', 'signed_at': '2026-09-04'}}


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
from datetime import date

_PERIOD_DAYS = {"week": 7, "fortnight": 14, "month": 31}


def _d(s):
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _near(a, b, tol):
    return isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) <= tol


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    dd, cur = obj.get("data_date"), obj.get("currency")
    period = _PERIOD_DAYS.get(obj.get("reporting_period"), 31)
    th = obj.get("variance_thresholds") or {}
    rows = [r for r in obj.get("projects") or [] if isinstance(r, dict)]
    weighted_policy = (obj.get("weighting") or {}).get("policy") != "currency-sum"
    beyond: list[str] = []
    fixed_margin = 0.0
    for i, r in enumerate(rows):
        p = f"projects[{i}] ({r.get('name')})"
        if r.get("data_date") != dd:
            errs.append(f"{p}: data_date {r.get('data_date')} differs from the artefact data_date {dd}; align the export or move the row to stale_projects (r-single-data-date)")
        if r.get("currency") != cur:
            errs.append(f"{p}: currency {r.get('currency')} differs from the reporting currency {cur}; convert before summing (r-rollup-sums-currency-not-indices)")
        ex, rd = _d((r.get("ledger_exported_at") or "")[:10]), _d(dd)
        if ex and rd and (rd - ex).days > period:
            errs.append(f"{p}: ledger exported {ex} is more than one {obj.get('reporting_period')} before the data date; mark stale and exclude (r-single-data-date)")
        bac, pv, ev, ac = r.get("bac", 0), r.get("pv", 0), r.get("ev", 0), r.get("ac", 0)
        if not _near(r.get("sv"), ev - pv, 1):
            errs.append(f"{p}: sv must be EV - PV = {ev - pv} (r-per-project-table-fields)")
        if not _near(r.get("cv"), ev - ac, 1):
            errs.append(f"{p}: cv must be EV - AC = {ev - ac} (r-per-project-table-fields)")
        if pv and not _near(r.get("spi"), ev / pv, 0.01):
            errs.append(f"{p}: spi must be EV / PV = {ev / pv:.2f} (r-per-project-table-fields)")
        if ac and not _near(r.get("cpi"), ev / ac, 0.01):
            errs.append(f"{p}: cpi must be EV / AC = {ev / ac:.2f} (r-per-project-table-fields)")
        spi, cpi, eac = r.get("spi") or 0, r.get("cpi") or 0, r.get("eac", 0)
        f = r.get("eac_formula")
        if f == "BAC/CPI" and cpi and not _near(eac, bac / cpi, 0.01 * bac):
            errs.append(f"{p}: eac must be BAC / CPI = {bac / cpi:.0f} for the named formula (r-per-project-table-fields)")
        if f == "AC+(BAC-EV)/(CPI*SPI)" and cpi and spi and not _near(eac, ac + (bac - ev) / (cpi * spi), 0.01 * bac):
            errs.append(f"{p}: eac must be AC + (BAC - EV) / (CPI x SPI) = {ac + (bac - ev) / (cpi * spi):.0f} for the named formula (r-per-project-table-fields)")
        if not _near(r.get("vac"), bac - eac, 1):
            errs.append(f"{p}: vac must be BAC - EAC = {bac - eac} (r-per-project-table-fields)")
        if r.get("contract_type") == "fixed-bid":
            cv_ = r.get("contract_value", 0)
            if not _near(r.get("implied_margin"), cv_ - eac, 1):
                errs.append(f"{p}: implied_margin must be contract_value - EAC = {cv_ - eac} (r-eac-and-margin-in-money)")
            fixed_margin += r.get("implied_margin") or 0
        tr = r.get("trend") or []
        if tr and not (_near(tr[-1].get("spi"), spi, 0.005) and _near(tr[-1].get("cpi"), cpi, 0.005) and tr[-1].get("data_date") == dd):
            errs.append(f"{p}: last trend point must be the current data_date, spi and cpi (r-trend-three-periods)")
        if weighted_policy and "weight" not in r:
            errs.append(f"{p}: weight missing while weighting.policy is not currency-sum (r-weighting-policy-declared)")
        over = (spi < th.get("spi_min", 0) or cpi < th.get("cpi_min", 0)
                or abs(r.get("cv", 0)) > th.get("cv_pct_of_bac_max", 100) / 100 * bac)
        if over:
            beyond.append(r.get("name"))
            if "variance_narrative" not in r:
                errs.append(f"{p}: beyond a variance threshold but carries no variance_narrative (r-variance-thresholds-named)")
        elif "variance_narrative" in r:
            errs.append(f"{p}: inside every threshold but carries a variance_narrative (r-variance-thresholds-named)")
    for i, s in enumerate(obj.get("stale_projects") or []):
        ld, rd = _d(s.get("last_data_date")), _d(dd)
        if ld and rd and (rd - ld).days <= period:
            errs.append(f"stale_projects[{i}] ({s.get('name')}): last_data_date is within one {obj.get('reporting_period')} of the data date; it belongs in projects[] (r-single-data-date)")
    agg = obj.get("aggregate") or {}
    disc, loe = agg.get("discrete") or {}, agg.get("loe") or {}
    drows = [r for r in rows if r.get("ev_method") != "level-of-effort"]
    lrows = [r for r in rows if r.get("ev_method") == "level-of-effort"]
    for k in ("bac", "pv", "ev", "ac"):
        want = sum(r.get(k, 0) for r in drows)
        if not _near(disc.get(k), want, 1):
            errs.append(f"aggregate.discrete.{k} must be the currency sum of the non-LOE rows = {want} (r-rollup-sums-currency-not-indices, r-normalise-contract-types)")
        want = sum(r.get(k, 0) for r in lrows)
        if not _near(loe.get(k), want, 1):
            errs.append(f"aggregate.loe.{k} must be the currency sum of the level-of-effort rows = {want} (r-normalise-contract-types)")
    spv, sev, sac = sum(r.get("pv", 0) for r in drows), sum(r.get("ev", 0) for r in drows), sum(r.get("ac", 0) for r in drows)
    if spv and not _near(disc.get("spi"), sev / spv, 0.01):
        errs.append(f"aggregate.discrete.spi must be sum(EV) / sum(PV) = {sev / spv:.2f}, not an average of row indices (r-rollup-sums-currency-not-indices)")
    if sac and not _near(disc.get("cpi"), sev / sac, 0.01):
        errs.append(f"aggregate.discrete.cpi must be sum(EV) / sum(AC) = {sev / sac:.2f}, not an average of row indices (r-rollup-sums-currency-not-indices)")
    deac = sum(r.get("eac", 0) for r in drows)
    if not _near(disc.get("eac"), deac, 1):
        errs.append(f"aggregate.discrete.eac must be the sum of row EACs = {deac} (r-eac-and-margin-in-money)")
    if not _near(disc.get("vac"), disc.get("bac", 0) - disc.get("eac", 0), 1):
        errs.append("aggregate.discrete.vac must be BAC - EAC (r-eac-and-margin-in-money)")
    if weighted_policy and "weighted" not in agg:
        errs.append("aggregate.weighted missing while weighting.policy is not currency-sum; print it beside the unweighted figures (r-weighting-policy-declared)")
    if weighted_policy and "weighted" in agg and all("weight" in r for r in drows) and drows:
        wpv = sum(r["weight"] * r.get("pv", 0) for r in drows)
        wev = sum(r["weight"] * r.get("ev", 0) for r in drows)
        wac = sum(r["weight"] * r.get("ac", 0) for r in drows)
        w = agg["weighted"]
        if wpv and not _near(w.get("spi"), wev / wpv, 0.01):
            errs.append(f"aggregate.weighted.spi must be sum(w x EV) / sum(w x PV) = {wev / wpv:.2f} (r-weighting-policy-declared)")
        if wac and not _near(w.get("cpi"), wev / wac, 0.01):
            errs.append(f"aggregate.weighted.cpi must be sum(w x EV) / sum(w x AC) = {wev / wac:.2f} (r-weighting-policy-declared)")
    tr = agg.get("trend") or []
    if tr and not (_near(tr[-1].get("spi"), disc.get("spi"), 0.005) and _near(tr[-1].get("cpi"), disc.get("cpi"), 0.005) and tr[-1].get("data_date") == dd):
        errs.append("aggregate.trend: last point must be the current data_date and discrete spi / cpi (r-trend-three-periods)")
    es = obj.get("executive_summary") or {}
    tot_bac = disc.get("bac", 0) + loe.get("bac", 0)
    tot_eac = disc.get("eac", 0) + sum(r.get("eac", 0) for r in lrows)
    if not _near(es.get("bac"), tot_bac, 1):
        errs.append(f"executive_summary.bac must be discrete + LOE BAC = {tot_bac} (r-eac-and-margin-in-money)")
    if not _near(es.get("eac"), tot_eac, 1):
        errs.append(f"executive_summary.eac must be discrete EAC + LOE row EACs = {tot_eac} (r-eac-and-margin-in-money)")
    if not _near(es.get("vac"), es.get("bac", 0) - es.get("eac", 0), 1):
        errs.append("executive_summary.vac must be BAC - EAC (r-eac-and-margin-in-money)")
    if not _near(es.get("fixed_bid_margin_total"), fixed_margin, 1):
        errs.append(f"executive_summary.fixed_bid_margin_total must be the sum of fixed-bid implied_margin = {fixed_margin:.0f} (r-eac-and-margin-in-money)")
    if sorted(es.get("escalated_projects") or []) != sorted(beyond):
        errs.append(f"executive_summary.escalated_projects must be exactly the rows beyond a threshold: {sorted(beyond)} (r-variance-thresholds-named)")
    so = obj.get("owner_sign_off") or {}
    if so.get("signed_by") != obj.get("owner"):
        errs.append("owner_sign_off.signed_by must be the portfolio owner (03 human checkpoint)")
    if (so.get("signed_at") or "") > (obj.get("executive_review_date") or ""):
        errs.append("owner_sign_off.signed_at is after executive_review_date (03 human checkpoint)")
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
        prog="validate-portfolio-evm-rollup-method.py",
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
