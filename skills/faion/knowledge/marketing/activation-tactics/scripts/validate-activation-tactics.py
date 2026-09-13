#!/usr/bin/env python3
"""validate-activation-tactics.py

Validate the artefact produced by the activation-tactics methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/activation-tactics.json',
 'title': 'Activation Tactics playbook step',
 'type': 'object',
 'required': ['activation_event',
              'window_days',
              'dropoffs',
              'tactics',
              'steps',
              'decision_branches'],
 'additionalProperties': False,
 'definitions': {'snake': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'},
                 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1},
                 'path': {'type': 'string', 'pattern': '^/'},
                 'deep_link': {'type': 'string',
                               'pattern': '^https://[^\\s]+/[^\\s]+$',
                               'not': {'pattern': '/(login|dashboard|home)?/?$'}}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'activation_event': {'$ref': '#/definitions/snake'},
                'window_days': {'type': 'integer', 'minimum': 1},
                'dropoffs': {'type': 'array',
                             'minItems': 1,
                             'items': {'type': 'object',
                                       'required': ['step',
                                                    'screen',
                                                    'current_conversion',
                                                    'live_tactic'],
                                       'additionalProperties': False,
                                       'properties': {'step': {'type': 'string', 'minLength': 2},
                                                      'screen': {'$ref': '#/definitions/path'},
                                                      'current_conversion': {'$ref': '#/definitions/rate'},
                                                      'live_tactic': {'type': 'boolean'}}}},
                'tactics': {'type': 'array',
                            'minItems': 1,
                            'items': {'type': 'object',
                                      'required': ['id',
                                                   'type',
                                                   'target_step',
                                                   'step_conversion_baseline'],
                                      'additionalProperties': False,
                                      'properties': {'id': {'type': 'string',
                                                            'pattern': '^t[0-9]+$'},
                                                     'type': {'type': 'string',
                                                              'enum': ['checklist',
                                                                       'email_sequence',
                                                                       'in_app_guide',
                                                                       'segmented_onboarding']},
                                                     'target_step': {'type': 'string',
                                                                     'minLength': 2},
                                                     'step_conversion_baseline': {'$ref': '#/definitions/rate'},
                                                     'experiment_id': {'type': 'string',
                                                                       'minLength': 2},
                                                     'checklist': {'type': 'object',
                                                                   'required': ['items'],
                                                                   'additionalProperties': False,
                                                                   'properties': {'items': {'type': 'array',
                                                                                            'minItems': 3,
                                                                                            'maxItems': 5,
                                                                                            'items': {'type': 'object',
                                                                                                      'required': ['id',
                                                                                                                   'label',
                                                                                                                   'required',
                                                                                                                   'activation_event',
                                                                                                                   'action',
                                                                                                                   'tracked_event'],
                                                                                                      'additionalProperties': False,
                                                                                                      'properties': {'id': {'$ref': '#/definitions/snake'},
                                                                                                                     'label': {'type': 'string',
                                                                                                                               'minLength': 3},
                                                                                                                     'required': {'type': 'boolean'},
                                                                                                                     'activation_event': {'type': 'boolean'},
                                                                                                                     'action': {'anyOf': [{'$ref': '#/definitions/path'},
                                                                                                                                          {'type': 'null'}]},
                                                                                                                     'tracked_event': {'anyOf': [{'$ref': '#/definitions/snake'},
                                                                                                                                                 {'type': 'null'}]}},
                                                                                                      'anyOf': [{'properties': {'action': {'type': 'string'}}},
                                                                                                                {'properties': {'tracked_event': {'type': 'string'}}}]}}}},
                                                     'emails': {'type': 'array',
                                                                'minItems': 1,
                                                                'maxItems': 4,
                                                                'items': {'type': 'object',
                                                                          'required': ['day',
                                                                                       'subject',
                                                                                       'cta_count',
                                                                                       'cta_url',
                                                                                       'expected_time_minutes',
                                                                                       'send_condition',
                                                                                       'condition_evaluated_at'],
                                                                          'additionalProperties': False,
                                                                          'properties': {'day': {'type': 'integer',
                                                                                                 'minimum': 0},
                                                                                         'subject': {'type': 'string',
                                                                                                     'minLength': 5},
                                                                                         'cta_count': {'const': 1},
                                                                                         'cta_url': {'$ref': '#/definitions/deep_link'},
                                                                                         'expected_time_minutes': {'type': 'integer',
                                                                                                                   'minimum': 1},
                                                                                         'send_condition': {'type': 'string',
                                                                                                            'enum': ['always',
                                                                                                                     'not_activated']},
                                                                                         'condition_evaluated_at': {'const': 'send_time'}},
                                                                          'if': {'properties': {'day': {'minimum': 1}}},
                                                                          'then': {'properties': {'send_condition': {'const': 'not_activated'}}}}},
                                                     'guide': {'type': 'object',
                                                               'required': ['screen',
                                                                            'guides_on_screen',
                                                                            'dismissible_in_one_click',
                                                                            'hidden_after_step_complete'],
                                                               'additionalProperties': False,
                                                               'properties': {'screen': {'$ref': '#/definitions/path'},
                                                                              'guides_on_screen': {'const': 1},
                                                                              'dismissible_in_one_click': {'const': True},
                                                                              'hidden_after_step_complete': {'const': True}}},
                                                     'segmentation': {'type': 'object',
                                                                      'required': ['segment_key',
                                                                                   'segments'],
                                                                      'additionalProperties': False,
                                                                      'properties': {'segment_key': {'type': 'object',
                                                                                                     'required': ['name',
                                                                                                                  'captured_at'],
                                                                                                     'additionalProperties': False,
                                                                                                     'properties': {'name': {'$ref': '#/definitions/snake'},
                                                                                                                    'captured_at': {'const': 'signup'}}},
                                                                                     'segments': {'type': 'array',
                                                                                                  'minItems': 2,
                                                                                                  'items': {'type': 'object',
                                                                                                            'required': ['name',
                                                                                                                         'first_action'],
                                                                                                            'additionalProperties': False,
                                                                                                            'properties': {'name': {'type': 'string',
                                                                                                                                    'minLength': 2},
                                                                                                                           'first_action': {'type': 'string',
                                                                                                                                            'minLength': 3}}}}}}},
                                      'allOf': [{'if': {'properties': {'type': {'const': 'checklist'}}},
                                                 'then': {'required': ['checklist']}},
                                                {'if': {'properties': {'type': {'const': 'email_sequence'}}},
                                                 'then': {'required': ['emails']}},
                                                {'if': {'properties': {'type': {'const': 'in_app_guide'}}},
                                                 'then': {'required': ['guide']}},
                                                {'if': {'properties': {'type': {'const': 'segmented_onboarding'}}},
                                                 'then': {'required': ['segmentation']}}]}},
                'steps': {'type': 'array',
                          'minItems': 1,
                          'items': {'type': 'object',
                                    'required': ['id',
                                                 'tactic_id',
                                                 'action',
                                                 'exit_criterion',
                                                 'output_location'],
                                    'additionalProperties': False,
                                    'properties': {'id': {'type': 'string', 'pattern': '^s[0-9]+$'},
                                                   'tactic_id': {'type': 'string',
                                                                 'pattern': '^t[0-9]+$'},
                                                   'action': {'type': 'string', 'minLength': 10},
                                                   'exit_criterion': {'type': 'object',
                                                                      'required': ['metric',
                                                                                   'baseline',
                                                                                   'minimum_lift'],
                                                                      'additionalProperties': False,
                                                                      'properties': {'metric': {'type': 'string',
                                                                                                'enum': ['step_conversion',
                                                                                                         'activation_rate']},
                                                                                     'baseline': {'$ref': '#/definitions/rate'},
                                                                                     'minimum_lift': {'type': 'number',
                                                                                                      'exclusiveMinimum': 0,
                                                                                                      'maximum': 1}}},
                                                   'output_location': {'type': 'string',
                                                                       'minLength': 3}}}},
                'decision_branches': {'type': 'array',
                                      'minItems': 1,
                                      'contains': {'properties': {'kind': {'const': 'defer_live_tactic'}}},
                                      'items': {'type': 'object',
                                                'required': ['kind', 'when', 'then'],
                                                'additionalProperties': False,
                                                'properties': {'kind': {'type': 'string',
                                                                        'enum': ['defer_live_tactic',
                                                                                 'keep',
                                                                                 'remove',
                                                                                 'loop_back']},
                                                               'when': {'type': 'string',
                                                                        'minLength': 10},
                                                               'then': {'type': 'string',
                                                                        'minLength': 10}}}}}}

OK = {'activation_event': 'project_created',
 'window_days': 7,
 'dropoffs': [{'step': 'project created',
               'screen': '/projects/new',
               'current_conversion': 0.326,
               'live_tactic': False},
              {'step': 'email verified',
               'screen': '/verify',
               'current_conversion': 0.73,
               'live_tactic': False},
              {'step': 'workspace named',
               'screen': '/workspace/setup',
               'current_conversion': 0.94,
               'live_tactic': True}],
 'tactics': [{'id': 't1',
              'type': 'checklist',
              'target_step': 'project created',
              'step_conversion_baseline': 0.326,
              'checklist': {'items': [{'id': 'workspace_named',
                                       'label': 'Name your workspace',
                                       'required': False,
                                       'activation_event': False,
                                       'action': None,
                                       'tracked_event': 'workspace_named'},
                                      {'id': 'first_project',
                                       'label': 'Create your first project',
                                       'required': True,
                                       'activation_event': True,
                                       'action': '/projects/new',
                                       'tracked_event': 'project_created'},
                                      {'id': 'invite',
                                       'label': 'Invite a team member',
                                       'required': False,
                                       'activation_event': False,
                                       'action': '/team/invite',
                                       'tracked_event': 'invite_sent'}]}},
             {'id': 't2',
              'type': 'email_sequence',
              'target_step': 'email verified',
              'step_conversion_baseline': 0.73,
              'emails': [{'day': 0,
                          'subject': 'Verify your email to open your workspace',
                          'cta_count': 1,
                          'cta_url': 'https://app.acme.com/verify?token={{token}}',
                          'expected_time_minutes': 1,
                          'send_condition': 'always',
                          'condition_evaluated_at': 'send_time'},
                         {'day': 1,
                          'subject': 'One click and your first project is 2 minutes away',
                          'cta_count': 1,
                          'cta_url': 'https://app.acme.com/verify?token={{token}}',
                          'expected_time_minutes': 1,
                          'send_condition': 'not_activated',
                          'condition_evaluated_at': 'send_time'},
                         {'day': 3,
                          'subject': 'Need a hand getting in?',
                          'cta_count': 1,
                          'cta_url': 'https://app.acme.com/verify?token={{token}}',
                          'expected_time_minutes': 1,
                          'send_condition': 'not_activated',
                          'condition_evaluated_at': 'send_time'}]}],
 'steps': [{'id': 's1',
            'tactic_id': 't1',
            'action': 'Ship the 3-item checklist on /projects/new to 100 percent of new signups '
                      'for two closed signup weeks',
            'exit_criterion': {'metric': 'step_conversion',
                               'baseline': 0.326,
                               'minimum_lift': 0.03},
            'output_location': 'growth/activation/2026-05-checklist.md'},
           {'id': 's2',
            'tactic_id': 't2',
            'action': 'Enable the 3-send verification sequence with send-time suppression for two '
                      'closed signup weeks',
            'exit_criterion': {'metric': 'step_conversion', 'baseline': 0.73, 'minimum_lift': 0.05},
            'output_location': 'growth/activation/2026-05-verify-emails.md'}],
 'decision_branches': [{'kind': 'defer_live_tactic',
                        'when': 'the target step already has a live tactic in this period '
                                '(workspace named)',
                        'then': 'defer the new tactic until the live one has hit or missed its '
                                'exit criterion'},
                       {'kind': 'remove',
                        'when': 'step conversion after two closed weeks is below baseline plus '
                                'minimum_lift',
                        'then': 'remove the tactic and return to the drop-off ranking'},
                       {'kind': 'keep',
                        'when': 'step conversion after two closed weeks is at or above baseline '
                                'plus minimum_lift',
                        'then': 'keep the tactic and move to the next drop-off step'}]}

BAD = {'activation_event': 'project_created',
 'window_days': 7,
 'dropoffs': [{'step': 'project created',
               'screen': '/projects/new',
               'current_conversion': 0.326,
               'live_tactic': False}],
 'tactics': [{'id': 't1',
              'type': 'checklist',
              'target_step': 'onboarding',
              'step_conversion_baseline': 0.5,
              'checklist': {'items': [{'id': 'profile',
                                       'label': 'Complete your profile',
                                       'required': False,
                                       'activation_event': False,
                                       'action': '/settings/profile',
                                       'tracked_event': None},
                                      {'id': 'read_docs',
                                       'label': 'Read the getting-started guide',
                                       'required': False,
                                       'activation_event': False,
                                       'action': None,
                                       'tracked_event': None},
                                      {'id': 'first_project',
                                       'label': 'Create your first project',
                                       'required': False,
                                       'activation_event': True,
                                       'action': '/projects/new',
                                       'tracked_event': 'project_created'},
                                      {'id': 'invite',
                                       'label': 'Invite a team member',
                                       'required': False,
                                       'activation_event': True,
                                       'action': '/team/invite',
                                       'tracked_event': 'invite_sent'},
                                      {'id': 'watch_video',
                                       'label': 'Watch the intro video',
                                       'required': False,
                                       'activation_event': False,
                                       'action': None,
                                       'tracked_event': None},
                                      {'id': 'connect',
                                       'label': 'Connect an integration',
                                       'required': False,
                                       'activation_event': False,
                                       'action': '/integrations',
                                       'tracked_event': None}]}},
             {'id': 't2',
              'type': 'email_sequence',
              'target_step': 'project created',
              'step_conversion_baseline': 0.326,
              'emails': [{'day': 0,
                          'subject': 'Welcome to Acme',
                          'cta_count': 2,
                          'cta_url': 'https://app.acme.com/',
                          'expected_time_minutes': 2,
                          'send_condition': 'always',
                          'condition_evaluated_at': 'send_time'},
                         {'day': 3,
                          'subject': 'Quick win: do this in 5 minutes',
                          'cta_count': 1,
                          'cta_url': 'https://app.acme.com/login',
                          'expected_time_minutes': 5,
                          'send_condition': 'always',
                          'condition_evaluated_at': 'send_time'},
                         {'day': 10,
                          'subject': 'Your account is waiting',
                          'cta_count': 1,
                          'cta_url': 'https://app.acme.com/projects/new',
                          'expected_time_minutes': 2,
                          'send_condition': 'not_activated',
                          'condition_evaluated_at': 'send_time'}]},
             {'id': 't3',
              'type': 'in_app_guide',
              'target_step': 'project created',
              'step_conversion_baseline': 0.326,
              'guide': {'screen': '/dashboard',
                        'guides_on_screen': 3,
                        'dismissible_in_one_click': True,
                        'hidden_after_step_complete': False}}],
 'steps': [{'id': 's1',
            'tactic_id': 't1',
            'action': 'Ship the checklist to everyone',
            'exit_criterion': {'metric': 'step_conversion', 'baseline': 0.5, 'minimum_lift': 0.02},
            'output_location': 'docs/published/'}],
 'decision_branches': [{'kind': 'loop_back',
                        'when': 'activation does not improve',
                        'then': 'try another tactic from the list'}]}


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
    window = obj.get("window_days") or 0
    drops = {d.get("step"): d for d in obj.get("dropoffs") or [] if isinstance(d, dict)}
    tactics = [t for t in obj.get("tactics") or [] if isinstance(t, dict)]
    by_step: dict[str, list[dict]] = {}
    for i, t in enumerate(tactics):
        step = t.get("target_step")
        d = drops.get(step)
        if d is None:
            errs.append(f"tactics[{i}]: target_step {step!r} is not a measured drop-off in dropoffs[] (r-tactic-targets-named-dropoff-step)")
        else:
            if abs(d.get("current_conversion", -1) - t.get("step_conversion_baseline", -2)) > 0.0005:
                errs.append(f"tactics[{i}]: step_conversion_baseline must equal dropoffs current_conversion {d.get('current_conversion')} for {step!r} (r-tactic-targets-named-dropoff-step)")
            if d.get("live_tactic") is True:
                errs.append(f"tactics[{i}]: {step!r} already has a live tactic; defer via the defer_live_tactic branch (r-one-tactic-per-step-at-a-time)")
            g = t.get("guide") or {}
            if g and g.get("screen") != d.get("screen"):
                errs.append(f"tactics[{i}]: guide.screen {g.get('screen')!r} is not the target step's screen {d.get('screen')!r} (r-in-app-guide-at-dropoff-only)")
        by_step.setdefault(step, []).append(t)
        items = (t.get("checklist") or {}).get("items") or []
        if items:
            act = [it for it in items if it.get("activation_event") is True]
            if len(act) != 1:
                errs.append(f"tactics[{i}]: checklist must flag exactly one item activation_event: true, found {len(act)} (r-checklist-single-activation-item)")
            elif act[0].get("required") is not True:
                errs.append(f"tactics[{i}]: the activation_event checklist item must be required: true (r-checklist-single-activation-item)")
        emails = t.get("emails") or []
        if emails:
            if emails[0].get("day") != 0:
                errs.append(f"tactics[{i}]: emails[0] must be the Day 0 send (r-email-sequence-suppressed-on-activation)")
            for j, e in enumerate(emails):
                if e.get("day", 0) > window:
                    errs.append(f"tactics[{i}].emails[{j}]: day {e.get('day')} is outside window_days {window} (r-email-sequence-suppressed-on-activation)")
        seg = t.get("segmentation") or {}
        acts = [s.get("first_action") for s in seg.get("segments") or []]
        if acts and len(set(acts)) != len(acts):
            errs.append(f"tactics[{i}]: segments share a first_action; merge them (r-segmented-onboarding-keyed-at-signup)")
    for step, ts in by_step.items():
        if len(ts) > 1 and len({t.get("experiment_id") for t in ts}) != 1 or (len(ts) > 1 and ts[0].get("experiment_id") is None):
            errs.append(f"tactics: {len(ts)} tactics target {step!r} in the same period without a shared experiment_id (r-one-tactic-per-step-at-a-time)")
    tids = {t.get("id") for t in tactics}
    covered = {s.get("tactic_id") for s in obj.get("steps") or [] if isinstance(s, dict)}
    for tid in sorted(tids - covered):
        errs.append(f"steps: tactic {tid} has no rollout step with an exit criterion (r-exit-criterion-states-metric-and-threshold)")
    for i, s in enumerate(obj.get("steps") or []):
        if s.get("tactic_id") not in tids:
            errs.append(f"steps[{i}]: tactic_id {s.get('tactic_id')!r} is not in tactics[] (r-exit-criterion-states-metric-and-threshold)")
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
        prog="validate-activation-tactics.py",
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
