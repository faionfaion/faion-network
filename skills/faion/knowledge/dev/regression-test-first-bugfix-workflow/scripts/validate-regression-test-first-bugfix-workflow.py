#!/usr/bin/env python3
"""validate-regression-test-first-bugfix-workflow.py

Validate the artefact produced by the regression-test-first-bugfix-workflow methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/regression-test-first-bugfix-workflow.json',
 'title': 'Regression-test-first bugfix workflow record',
 'type': 'object',
 'required': ['alert', 'red_test', 'fix', 'verification', 'owner', 'review'],
 'additionalProperties': False,
 'definitions': {'url': {'type': 'string', 'pattern': '^https://'},
                 'sha': {'type': 'string', 'pattern': '^[0-9a-f]{7,40}$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'alert': {'type': 'object',
                          'required': ['kind',
                                       'url',
                                       'alert_id',
                                       'observed_outcome',
                                       'reproducing_inputs',
                                       'deterministic'],
                          'additionalProperties': False,
                          'properties': {'kind': {'type': 'string',
                                                  'enum': ['sentry',
                                                           'datadog',
                                                           'customer-ticket',
                                                           'log-aggregator']},
                                         'url': {'$ref': '#/definitions/url'},
                                         'alert_id': {'type': 'string', 'minLength': 1},
                                         'observed_outcome': {'type': 'object',
                                                              'required': ['kind', 'value'],
                                                              'additionalProperties': False,
                                                              'properties': {'kind': {'type': 'string',
                                                                                      'enum': ['exception',
                                                                                               'wrong-output']},
                                                                             'value': {'type': 'string',
                                                                                       'minLength': 3}}},
                                         'side_effect': {'type': 'string', 'minLength': 3},
                                         'reproducing_inputs': {'type': 'object',
                                                                'minProperties': 1},
                                         'pii_substitutions': {'type': 'array',
                                                               'items': {'type': 'object',
                                                                         'required': ['field',
                                                                                      'shape'],
                                                                         'additionalProperties': False,
                                                                         'properties': {'field': {'type': 'string',
                                                                                                  'minLength': 1},
                                                                                        'shape': {'type': 'string',
                                                                                                  'minLength': 1}}}},
                                         'deterministic': {'const': True}}},
                'red_test': {'type': 'object',
                             'required': ['status'],
                             'properties': {'status': {'type': 'string',
                                                       'enum': ['committed', 'pending']}},
                             'if': {'properties': {'status': {'const': 'committed'}}},
                             'then': {'required': ['path',
                                                   'commit',
                                                   'commit_message_has_alert_url',
                                                   'asserts',
                                                   'red_ci_run_url',
                                                   'failure_matches_alert',
                                                   'stable_runs'],
                                      'additionalProperties': False,
                                      'properties': {'status': {'const': 'committed'},
                                                     'path': {'type': 'string',
                                                              'pattern': '^tests/regression/'},
                                                     'commit': {'$ref': '#/definitions/sha'},
                                                     'commit_message_has_alert_url': {'const': True},
                                                     'asserts': {'type': 'array',
                                                                 'minItems': 1,
                                                                 'items': {'type': 'string',
                                                                           'minLength': 3,
                                                                           'not': {'pattern': 'raises\\(\\s*(Exception|BaseException)\\s*\\)'}}},
                                                     'side_effect_asserts': {'type': 'array',
                                                                             'items': {'type': 'string',
                                                                                       'minLength': 3}},
                                                     'red_ci_run_url': {'$ref': '#/definitions/url'},
                                                     'failure_matches_alert': {'const': True},
                                                     'stable_runs': {'type': 'integer',
                                                                     'minimum': 3}}},
                             'else': {'required': ['follow_up_ticket_url', 'due_at'],
                                      'additionalProperties': False,
                                      'properties': {'status': {'const': 'pending'},
                                                     'follow_up_ticket_url': {'$ref': '#/definitions/url'},
                                                     'due_at': {'$ref': '#/definitions/date'}}}},
                'fix': {'type': 'object',
                        'required': ['pr_url',
                                     'first_fix_commit',
                                     'diff_lines',
                                     'touches_red_test_assertions',
                                     'hotfix'],
                        'additionalProperties': False,
                        'properties': {'pr_url': {'$ref': '#/definitions/url'},
                                       'first_fix_commit': {'$ref': '#/definitions/sha'},
                                       'diff_lines': {'type': 'integer', 'minimum': 1},
                                       'touches_red_test_assertions': {'const': False},
                                       'hotfix': {'type': 'boolean'},
                                       'refactor_pr_url': {'$ref': '#/definitions/url'}}},
                'verification': {'type': 'object',
                                 'required': ['ci_run_url', 'passed', 'skipped_or_xfail'],
                                 'additionalProperties': False,
                                 'properties': {'ci_run_url': {'$ref': '#/definitions/url'},
                                                'passed': {'const': True},
                                                'skipped_or_xfail': {'const': False}}},
                'owner': {'$ref': '#/definitions/handle'},
                'review': {'type': 'object',
                           'required': ['merged_at', 'next_review_at', 'alert_resolved'],
                           'additionalProperties': False,
                           'properties': {'merged_at': {'$ref': '#/definitions/date'},
                                          'next_review_at': {'$ref': '#/definitions/date'},
                                          'alert_resolved': {'type': 'boolean'},
                                          'outcome': {'type': 'object',
                                                      'required': ['reviewed_at',
                                                                   'regression_events_in_window',
                                                                   'same_signature_new_issue'],
                                                      'additionalProperties': False,
                                                      'properties': {'reviewed_at': {'$ref': '#/definitions/date'},
                                                                     'regression_events_in_window': {'type': 'integer',
                                                                                                     'minimum': 0},
                                                                     'same_signature_new_issue': {'type': 'boolean'}}}}}}}

OK = {'alert': {'kind': 'sentry',
           'url': 'https://sentry.io/organizations/acme/issues/12345/',
           'alert_id': 'ACME-SHOP-12345',
           'observed_outcome': {'kind': 'exception',
                                'value': 'ValidationError: amount must be positive '
                                         '(checkout/serializers.py)'},
           'side_effect': 'an Order row is created before the serializer rejects the request',
           'reproducing_inputs': {'amount': 0.0,
                                  'locale': 'tr_TR',
                                  'currency': 'TRY',
                                  'cart_id': 'c_8f3a'},
           'pii_substitutions': [{'field': 'email', 'shape': 'same-domain synthetic address'}],
           'deterministic': True},
 'red_test': {'status': 'committed',
              'path': 'tests/regression/test_checkout_zero_amount.py',
              'commit': 'a1b2c3d4e5f',
              'commit_message_has_alert_url': True,
              'asserts': ['response.status_code == 422',
                          "'amount must be positive' in response.json()['detail']"],
              'side_effect_asserts': ["Order.objects.filter(cart_id='c_8f3a').count() == 0"],
              'red_ci_run_url': 'https://github.com/acme/shop/actions/runs/76',
              'failure_matches_alert': True,
              'stable_runs': 3},
 'fix': {'pr_url': 'https://github.com/acme/shop/pull/9981',
         'first_fix_commit': 'b2c3d4e5f6a',
         'diff_lines': 18,
         'touches_red_test_assertions': False,
         'hotfix': False},
 'verification': {'ci_run_url': 'https://github.com/acme/shop/actions/runs/77',
                  'passed': True,
                  'skipped_or_xfail': False},
 'owner': 'swe:alice',
 'review': {'merged_at': '2026-05-24',
            'next_review_at': '2026-08-22',
            'alert_resolved': True,
            'outcome': {'reviewed_at': '2026-08-22',
                        'regression_events_in_window': 0,
                        'same_signature_new_issue': False}}}

BAD = {'alert': {'kind': 'sentry',
           'url': 'https://sentry.io/organizations/acme/issues/12345/',
           'alert_id': 'ACME-SHOP-12345',
           'observed_outcome': {'kind': 'exception',
                                'value': 'ValidationError: amount must be positive '
                                         '(checkout/serializers.py)'},
           'side_effect': 'an Order row is created before the serializer rejects the request',
           'reproducing_inputs': {'amount': 9.99, 'locale': 'en_US'},
           'deterministic': True},
 'red_test': {'status': 'committed',
              'path': 'tests/unit/test_serializers.py',
              'commit': 'b2c3d4e5f6a',
              'commit_message_has_alert_url': False,
              'asserts': ['pytest.raises(Exception)'],
              'red_ci_run_url': 'https://github.com/acme/shop/actions/runs/77',
              'failure_matches_alert': True,
              'stable_runs': 1},
 'fix': {'pr_url': 'https://github.com/acme/shop/pull/9981',
         'first_fix_commit': 'b2c3d4e5f6a',
         'diff_lines': 412,
         'touches_red_test_assertions': True,
         'hotfix': False},
 'verification': {'ci_run_url': 'https://github.com/acme/shop/actions/runs/77',
                  'passed': True,
                  'skipped_or_xfail': False},
 'owner': 'swe:alice',
 'review': {'merged_at': '2026-05-24', 'next_review_at': '2026-06-24', 'alert_resolved': True}}


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

from datetime import date, timedelta


def _d(s: str) -> date | None:
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    alert = obj.get("alert") or {}
    rt = obj.get("red_test") or {}
    fix = obj.get("fix") or {}
    rv = obj.get("review") or {}
    merged, nxt = _d(rv.get("merged_at", "")), _d(rv.get("next_review_at", ""))
    if merged and nxt and nxt != merged + timedelta(days=90):
        errs.append(f"review.next_review_at must be merged_at + 90 days = {merged + timedelta(days=90)} (r-alert-closed-after-recurrence-window)")
    if rt.get("status") == "committed":
        if rt.get("commit") and rt.get("commit") == fix.get("first_fix_commit"):
            errs.append("red_test.commit equals fix.first_fix_commit: test and fix landed in one commit, the red state was never observed (r-red-test-committed-before-fix)")
        if alert.get("side_effect") and not rt.get("side_effect_asserts"):
            errs.append("alert.side_effect is set but red_test.side_effect_asserts is empty (r-test-fails-for-the-alerts-reason)")
    if rt.get("status") == "pending":
        if fix.get("hotfix") is not True:
            errs.append("red_test.status is pending but fix.hotfix is not true; only a hotfix may ship without the red test (r-hotfix-variant-carries-follow-up)")
        due = _d(rt.get("due_at", ""))
        if merged and due and due > merged + timedelta(days=14):
            errs.append(f"red_test.due_at is more than 14 days after merged_at ({merged + timedelta(days=14)} at the latest) (r-hotfix-variant-carries-follow-up)")
        if rv.get("alert_resolved") is True:
            errs.append("review.alert_resolved is true while the red test is still pending (r-hotfix-variant-carries-follow-up)")
    outcome = rv.get("outcome") or {}
    if outcome.get("regression_events_in_window", 0) > 0 and rv.get("alert_resolved") is True:
        errs.append("a regression event inside the window reopens the record; alert_resolved cannot stay true (r-alert-closed-after-recurrence-window)")
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
        prog="validate-regression-test-first-bugfix-workflow.py",
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
