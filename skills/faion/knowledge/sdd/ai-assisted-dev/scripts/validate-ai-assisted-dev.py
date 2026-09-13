#!/usr/bin/env python3
"""validate-ai-assisted-dev.py

Validate an AI-assisted development workflow record against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the ai-assisted-dev methodology, plus the
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
 '$id': 'https://faion.net/schemas/ai-assisted-dev.json',
 'title': 'AI-assisted development workflow record',
 'type': 'object',
 'required': ['team', 'owner', 'inputs', 'decision', 'evidence', 'review'],
 'additionalProperties': False,
 'definitions': {'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'url': {'type': 'string', 'pattern': '^https://'},
                 'tool': {'type': 'string',
                          'enum': ['claude-code', 'cursor', 'copilot', 'other', 'ai-off']},
                 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1},
                 'metrics': {'type': 'object',
                             'required': ['pr_count',
                                          'defect_escape_rate',
                                          'revert_rate',
                                          'churn_2w_rate'],
                             'additionalProperties': False,
                             'properties': {'pr_count': {'type': 'integer', 'minimum': 0},
                                            'defect_escape_rate': {'$ref': '#/definitions/rate'},
                                            'revert_rate': {'$ref': '#/definitions/rate'},
                                            'churn_2w_rate': {'$ref': '#/definitions/rate'}}}},
 'properties': {'__faion_header__': {'type': 'object'},
                'team': {'type': 'object',
                         'required': ['name', 'repo_url', 'record_version'],
                         'additionalProperties': False,
                         'properties': {'name': {'type': 'string', 'minLength': 2},
                                        'repo_url': {'$ref': '#/definitions/url'},
                                        'record_version': {'type': 'string',
                                                           'pattern': '^[0-9]+\\.[0-9]+\\.[0-9]+$'}}},
                'owner': {'$ref': '#/definitions/handle'},
                'inputs': {'type': 'array',
                           'minItems': 7,
                           'allOf': [{'contains': {'properties': {'name': {'const': 'tool_task_map'}}}},
                                     {'contains': {'properties': {'name': {'const': 'block_list'}}}},
                                     {'contains': {'properties': {'name': {'const': 'context_files'}}}},
                                     {'contains': {'properties': {'name': {'const': 'exclusion_file'}}}},
                                     {'contains': {'properties': {'name': {'const': 'tool_retention'}}}},
                                     {'contains': {'properties': {'name': {'const': 'prompt_template'}}}},
                                     {'contains': {'properties': {'name': {'const': 'ai_assisted_label'}}}}],
                           'items': {'type': 'object',
                                     'required': ['name', 'value'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'type': 'string',
                                                             'enum': ['tool_task_map',
                                                                      'block_list',
                                                                      'context_files',
                                                                      'exclusion_file',
                                                                      'tool_retention',
                                                                      'prompt_template',
                                                                      'ai_assisted_label']},
                                                    'value': {}},
                                     'allOf': [{'if': {'properties': {'name': {'const': 'tool_task_map'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'minItems': 7,
                                                                                  'allOf': [{'contains': {'properties': {'task_class': {'const': 'boilerplate-scaffolding'}}}},
                                                                                            {'contains': {'properties': {'task_class': {'const': 'unit-tests'}}}},
                                                                                            {'contains': {'properties': {'task_class': {'const': 'refactor'}}}},
                                                                                            {'contains': {'properties': {'task_class': {'const': 'code-review'}}}},
                                                                                            {'contains': {'properties': {'task_class': {'const': 'documentation'}}}},
                                                                                            {'contains': {'properties': {'task_class': {'const': 'data-migration'}}}},
                                                                                            {'contains': {'properties': {'task_class': {'const': 'infrastructure'}}}}],
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['task_class',
                                                                                                         'tool',
                                                                                                         'checkpoint'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'task_class': {'type': 'string',
                                                                                                                          'enum': ['boilerplate-scaffolding',
                                                                                                                                   'unit-tests',
                                                                                                                                   'refactor',
                                                                                                                                   'code-review',
                                                                                                                                   'documentation',
                                                                                                                                   'data-migration',
                                                                                                                                   'infrastructure']},
                                                                                                           'tool': {'$ref': '#/definitions/tool'},
                                                                                                           'checkpoint': {'type': 'string',
                                                                                                                          'enum': ['self-review',
                                                                                                                                   'one-reviewer',
                                                                                                                                   'two-reviewers-non-prompter',
                                                                                                                                   'ai-off']}},
                                                                                            'allOf': [{'if': {'properties': {'tool': {'const': 'ai-off'}}},
                                                                                                       'then': {'properties': {'checkpoint': {'const': 'ai-off'}}}},
                                                                                                      {'if': {'properties': {'checkpoint': {'const': 'ai-off'}}},
                                                                                                       'then': {'properties': {'tool': {'const': 'ai-off'}}}},
                                                                                                      {'if': {'properties': {'task_class': {'enum': ['data-migration',
                                                                                                                                                     'infrastructure']}}},
                                                                                                       'then': {'properties': {'checkpoint': {'enum': ['two-reviewers-non-prompter',
                                                                                                                                                       'ai-off']}}}}]}}}}},
                                               {'if': {'properties': {'name': {'const': 'block_list'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'minItems': 8,
                                                                                  'allOf': [{'contains': {'properties': {'area': {'const': 'authentication-session'}}}},
                                                                                            {'contains': {'properties': {'area': {'const': 'authorization'}}}},
                                                                                            {'contains': {'properties': {'area': {'const': 'cryptography-keys'}}}},
                                                                                            {'contains': {'properties': {'area': {'const': 'payments-billing'}}}},
                                                                                            {'contains': {'properties': {'area': {'const': 'pii-processing'}}}},
                                                                                            {'contains': {'properties': {'area': {'const': 'secrets-config-loading'}}}},
                                                                                            {'contains': {'properties': {'area': {'const': 'production-iac'}}}},
                                                                                            {'contains': {'properties': {'area': {'const': 'database-migrations'}}}}],
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['area',
                                                                                                         'paths',
                                                                                                         'policy'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'area': {'type': 'string',
                                                                                                                    'enum': ['authentication-session',
                                                                                                                             'authorization',
                                                                                                                             'cryptography-keys',
                                                                                                                             'payments-billing',
                                                                                                                             'pii-processing',
                                                                                                                             'secrets-config-loading',
                                                                                                                             'production-iac',
                                                                                                                             'database-migrations',
                                                                                                                             'other']},
                                                                                                           'paths': {'type': 'array',
                                                                                                                     'minItems': 1,
                                                                                                                     'items': {'type': 'string',
                                                                                                                               'minLength': 2}},
                                                                                                           'policy': {'type': 'string',
                                                                                                                      'enum': ['ai-off',
                                                                                                                               'two-reviewers-non-prompter']}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'context_files'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['tool',
                                                                                                         'path',
                                                                                                         'last_reviewed'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'tool': {'type': 'string',
                                                                                                                    'enum': ['claude-code',
                                                                                                                             'cursor',
                                                                                                                             'copilot',
                                                                                                                             'other']},
                                                                                                           'path': {'type': 'string',
                                                                                                                    'pattern': '(CLAUDE\\.md|\\.cursor/rules|\\.cursorrules|\\.github/copilot-instructions\\.md|AGENTS\\.md)$'},
                                                                                                           'last_reviewed': {'$ref': '#/definitions/date'}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'exclusion_file'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['path',
                                                                                               'excludes'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'path': {'type': 'string',
                                                                                                          'pattern': '(\\.cursorignore|\\.claudeignore|\\.gitignore|\\.aiignore|\\.copilotignore)$'},
                                                                                                 'excludes': {'type': 'array',
                                                                                                              'minItems': 1,
                                                                                                              'items': {'type': 'string',
                                                                                                                        'minLength': 2}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'tool_retention'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'minItems': 1,
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['tool',
                                                                                                         'terms_checked',
                                                                                                         'source'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'tool': {'type': 'string',
                                                                                                                    'enum': ['claude-code',
                                                                                                                             'cursor',
                                                                                                                             'copilot',
                                                                                                                             'other']},
                                                                                                           'terms_checked': {'type': 'boolean'},
                                                                                                           'source': {'$ref': '#/definitions/url'},
                                                                                                           'checked_on': {'$ref': '#/definitions/date'}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'prompt_template'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['path',
                                                                                               'blocks'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'path': {'type': 'string',
                                                                                                          'minLength': 4},
                                                                                                 'blocks': {'type': 'array',
                                                                                                            'const': ['Context',
                                                                                                                      'Task',
                                                                                                                      'Requirements',
                                                                                                                      'Output']}}}}}},
                                               {'if': {'properties': {'name': {'const': 'ai_assisted_label'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['label',
                                                                                               'auto_merge_disabled'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'label': {'type': 'string',
                                                                                                           'minLength': 4},
                                                                                                 'auto_merge_disabled': {'type': 'boolean',
                                                                                                                         'const': True}}}}}}]}},
                'decision': {'type': 'string', 'minLength': 20, 'pattern': 'ai-off'},
                'evidence': {'type': 'array',
                             'minItems': 1,
                             'items': {'$ref': '#/definitions/url'}},
                'review': {'type': 'object',
                           'required': ['cadence', 'next_review_at', 'last_outcome'],
                           'additionalProperties': False,
                           'properties': {'cadence': {'type': 'string',
                                                      'enum': ['monthly', 'quarterly']},
                                          'next_review_at': {'$ref': '#/definitions/date'},
                                          'last_outcome': {'oneOf': [{'type': 'null'},
                                                                     {'type': 'object',
                                                                      'required': ['period',
                                                                                   'ai_assisted',
                                                                                   'other',
                                                                                   'worse_on',
                                                                                   'map_tightened',
                                                                                   'url'],
                                                                      'additionalProperties': False,
                                                                      'properties': {'period': {'type': 'string',
                                                                                                'minLength': 6},
                                                                                     'ai_assisted': {'$ref': '#/definitions/metrics'},
                                                                                     'other': {'$ref': '#/definitions/metrics'},
                                                                                     'worse_on': {'type': 'array',
                                                                                                  'items': {'type': 'string',
                                                                                                            'enum': ['defect_escape_rate',
                                                                                                                     'revert_rate',
                                                                                                                     'churn_2w_rate']}},
                                                                                     'map_tightened': {'type': 'boolean'},
                                                                                     'action': {'type': 'string',
                                                                                                'minLength': 12},
                                                                                     'url': {'$ref': '#/definitions/url'}},
                                                                      'if': {'properties': {'worse_on': {'minItems': 1}}},
                                                                      'then': {'required': ['action'],
                                                                               'properties': {'map_tightened': {'const': True}}}}]}}}}}

OK = {'team': {'name': 'billing-platform',
          'repo_url': 'https://github.com/acme/billing',
          'record_version': '1.1.0'},
 'owner': 'swe:alice',
 'inputs': [{'name': 'tool_task_map',
             'value': [{'task_class': 'boilerplate-scaffolding',
                        'tool': 'claude-code',
                        'checkpoint': 'self-review'},
                       {'task_class': 'unit-tests',
                        'tool': 'claude-code',
                        'checkpoint': 'one-reviewer'},
                       {'task_class': 'refactor', 'tool': 'cursor', 'checkpoint': 'one-reviewer'},
                       {'task_class': 'code-review',
                        'tool': 'copilot',
                        'checkpoint': 'one-reviewer'},
                       {'task_class': 'documentation',
                        'tool': 'claude-code',
                        'checkpoint': 'self-review'},
                       {'task_class': 'data-migration', 'tool': 'ai-off', 'checkpoint': 'ai-off'},
                       {'task_class': 'infrastructure',
                        'tool': 'claude-code',
                        'checkpoint': 'two-reviewers-non-prompter'}]},
            {'name': 'block_list',
             'value': [{'area': 'authentication-session',
                        'paths': ['src/billing/auth/**'],
                        'policy': 'ai-off'},
                       {'area': 'authorization',
                        'paths': ['src/billing/permissions/**'],
                        'policy': 'two-reviewers-non-prompter'},
                       {'area': 'cryptography-keys',
                        'paths': ['src/billing/crypto/**'],
                        'policy': 'ai-off'},
                       {'area': 'payments-billing',
                        'paths': ['src/billing/charges/**', 'src/billing/invoices/**'],
                        'policy': 'two-reviewers-non-prompter'},
                       {'area': 'pii-processing',
                        'paths': ['src/billing/customers/**'],
                        'policy': 'two-reviewers-non-prompter'},
                       {'area': 'secrets-config-loading',
                        'paths': ['src/billing/config.py', 'deploy/secrets/**'],
                        'policy': 'ai-off'},
                       {'area': 'production-iac',
                        'paths': ['infra/prod/**'],
                        'policy': 'two-reviewers-non-prompter'},
                       {'area': 'database-migrations',
                        'paths': ['migrations/**'],
                        'policy': 'ai-off'}]},
            {'name': 'context_files',
             'value': [{'tool': 'claude-code', 'path': 'CLAUDE.md', 'last_reviewed': '2026-09-01'},
                       {'tool': 'cursor', 'path': '.cursor/rules', 'last_reviewed': '2026-09-01'},
                       {'tool': 'copilot',
                        'path': '.github/copilot-instructions.md',
                        'last_reviewed': '2026-09-01'}]},
            {'name': 'exclusion_file',
             'value': {'path': '.cursorignore',
                       'excludes': ['.env*',
                                    'deploy/secrets/**',
                                    'data/exports/**',
                                    'fixtures/customers/**']}},
            {'name': 'tool_retention',
             'value': [{'tool': 'claude-code',
                        'terms_checked': True,
                        'source': 'https://www.anthropic.com/legal/commercial-terms',
                        'checked_on': '2026-08-28'},
                       {'tool': 'cursor',
                        'terms_checked': True,
                        'source': 'https://cursor.com/privacy',
                        'checked_on': '2026-08-28'},
                       {'tool': 'copilot',
                        'terms_checked': True,
                        'source': 'https://docs.github.com/en/copilot/how-tos/manage-your-account/managing-copilot-policies-as-an-individual-subscriber',
                        'checked_on': '2026-08-28'}]},
            {'name': 'prompt_template',
             'value': {'path': 'templates/prompt-code.txt',
                       'blocks': ['Context', 'Task', 'Requirements', 'Output']}},
            {'name': 'ai_assisted_label',
             'value': {'label': 'ai-assisted', 'auto_merge_disabled': True}}],
 'decision': 'Claude Code for scaffolding, tests and docs, Cursor for refactors, Copilot for '
             'review suggestions; infrastructure only with two non-prompter reviewers; data '
             'migrations, auth, crypto and secrets loading are ai-off.',
 'evidence': ['https://github.com/acme/billing/blob/main/CLAUDE.md',
              'https://github.com/acme/billing/blob/main/.cursorignore',
              'https://grafana.example.com/d/pr-quality?var-label=ai-assisted&from=1751328000000&to=1756684800000'],
 'review': {'cadence': 'monthly',
            'next_review_at': '2026-10-01',
            'last_outcome': {'period': '2026-08',
                             'ai_assisted': {'pr_count': 41,
                                             'defect_escape_rate': 0.047,
                                             'revert_rate': 0.024,
                                             'churn_2w_rate': 0.17},
                             'other': {'pr_count': 63,
                                       'defect_escape_rate': 0.048,
                                       'revert_rate': 0.032,
                                       'churn_2w_rate': 0.09},
                             'worse_on': ['churn_2w_rate'],
                             'map_tightened': True,
                             'action': 'refactor moved from self-review to one-reviewer; '
                                       'record_version bumped 1.0.0 to 1.1.0',
                             'url': 'https://grafana.example.com/d/pr-quality?var-label=ai-assisted&from=1751328000000&to=1756684800000'}}}

BAD = {'team': {'name': 'billing-platform',
          'repo_url': 'https://github.com/acme/billing',
          'record_version': '1.0.0'},
 'owner': 'swe:bob',
 'inputs': [{'name': 'tool_task_map',
             'value': [{'task_class': 'boilerplate-scaffolding',
                        'tool': 'copilot',
                        'checkpoint': 'self-review'},
                       {'task_class': 'unit-tests', 'tool': 'copilot', 'checkpoint': 'self-review'},
                       {'task_class': 'refactor', 'tool': 'copilot', 'checkpoint': 'self-review'},
                       {'task_class': 'code-review',
                        'tool': 'copilot',
                        'checkpoint': 'self-review'},
                       {'task_class': 'documentation',
                        'tool': 'copilot',
                        'checkpoint': 'self-review'},
                       {'task_class': 'data-migration',
                        'tool': 'copilot',
                        'checkpoint': 'self-review'},
                       {'task_class': 'infrastructure',
                        'tool': 'copilot',
                        'checkpoint': 'one-reviewer'}]},
            {'name': 'block_list',
             'value': [{'area': 'payments-billing',
                        'paths': ['src/billing/charges/**'],
                        'policy': 'two-reviewers-non-prompter'}]},
            {'name': 'context_files', 'value': []},
            {'name': 'exclusion_file', 'value': {'path': '.gitignore', 'excludes': ['.env']}},
            {'name': 'tool_retention',
             'value': [{'tool': 'copilot',
                        'terms_checked': False,
                        'source': 'https://github.com/features/copilot'}]},
            {'name': 'prompt_template', 'value': {'path': 'none', 'blocks': ['Task']}},
            {'name': 'ai_assisted_label', 'value': {'label': '', 'auto_merge_disabled': False}}],
 'decision': 'We use Copilot for everything.',
 'evidence': ['https://github.com/acme/billing'],
 'review': {'cadence': 'quarterly',
            'next_review_at': '2026-12-01',
            'last_outcome': {'period': '2026-Q2',
                             'ai_assisted': {'pr_count': 80,
                                             'defect_escape_rate': 0.09,
                                             'revert_rate': 0.06,
                                             'churn_2w_rate': 0.31},
                             'other': {'pr_count': 20,
                                       'defect_escape_rate': 0.04,
                                       'revert_rate': 0.02,
                                       'churn_2w_rate': 0.08},
                             'worse_on': ['defect_escape_rate', 'revert_rate', 'churn_2w_rate'],
                             'map_tightened': False,
                             'url': 'https://grafana.example.com/d/pr-quality'}}}


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


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    inputs = {i.get("name"): i.get("value") for i in obj.get("inputs") or [] if isinstance(i, dict)}
    tools_in_use = {m.get("tool") for m in inputs.get("tool_task_map") or [] if m.get("tool") != "ai-off"}
    ctx = {c.get("tool") for c in inputs.get("context_files") or []}
    for t in sorted(tools_in_use - ctx):
        errs.append(f"tool {t} is in the map with no context_files entry (r-repo-context-file-maintained)")
    unchecked = {r.get("tool") for r in inputs.get("tool_retention") or [] if not r.get("terms_checked")}
    listed = {r.get("tool") for r in inputs.get("tool_retention") or []}
    for t in sorted(tools_in_use - listed):
        errs.append(f"tool {t} is in the map with no tool_retention entry (r-no-secrets-or-customer-data-in-prompts)")
    for t in sorted(tools_in_use & unchecked):
        errs.append(f"tool {t} has unchecked retention terms but is not ai-off in the map (r-no-secrets-or-customer-data-in-prompts)")
    last = (obj.get("review") or {}).get("last_outcome")
    if isinstance(last, dict):
        ai, other = last.get("ai_assisted") or {}, last.get("other") or {}
        actually_worse = [k for k in ("defect_escape_rate", "revert_rate", "churn_2w_rate") if ai.get(k, 0) > other.get(k, 0)]
        missing = [k for k in actually_worse if k not in (last.get("worse_on") or [])]
        if missing:
            errs.append(f"review.last_outcome.worse_on omits {missing} although ai_assisted is worse on them (r-defect-rate-tracked-ai-vs-human)")
        if last.get("url") and last["url"] not in (obj.get("evidence") or []):
            errs.append("review.last_outcome.url is not in evidence[] (r-defect-rate-tracked-ai-vs-human)")
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
        prog="validate-ai-assisted-dev.py",
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
