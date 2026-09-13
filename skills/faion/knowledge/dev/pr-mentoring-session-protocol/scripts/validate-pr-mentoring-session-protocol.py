#!/usr/bin/env python3
"""validate-pr-mentoring-session-protocol.py

Validate a PR mentoring session record against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the pr-mentoring-session-protocol methodology, plus the
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
 '$id': 'https://faion.net/schemas/pr-mentoring-session-protocol.json',
 'title': 'PR mentoring session record',
 'type': 'object',
 'required': ['session',
              'owner',
              'inputs',
              'fix_commit',
              'progression',
              'decision',
              'junior_confirmation',
              'evidence',
              'status'],
 'additionalProperties': False,
 'definitions': {'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'url': {'type': 'string', 'pattern': '^https://'},
                 'behaviour': {'type': 'string',
                               'minLength': 15,
                               'pattern': '^(?![\\s\\S]*([Bb]e more careful|[Tt]hink about|[Bb]e '
                                          'careful|[Kk]eep this in mind|[Nn]ext '
                                          'time|[Ss]loppy|[Rr]ushed|[Cc]areless))'}},
 'properties': {'__faion_header__': {'type': 'object'},
                'session': {'type': 'object',
                            'required': ['pr_url',
                                         'junior',
                                         'senior',
                                         'date',
                                         'record_readable_by_junior',
                                         'evaluation_use'],
                            'additionalProperties': False,
                            'properties': {'pr_url': {'type': 'string',
                                                      'pattern': '^https://[^\\s,]+/(pull|merge_requests|pull-requests)/[0-9]+$'},
                                           'junior': {'$ref': '#/definitions/handle'},
                                           'senior': {'$ref': '#/definitions/handle'},
                                           'date': {'$ref': '#/definitions/date'},
                                           'record_readable_by_junior': {'type': 'boolean',
                                                                         'const': True},
                                           'evaluation_use': {'type': 'string',
                                                              'enum': ['not-used-in-evaluation',
                                                                       'aggregated-in-performance-review',
                                                                       'aggregated-in-promotion-case']}}},
                'owner': {'$ref': '#/definitions/handle'},
                'inputs': {'type': 'array',
                           'minItems': 6,
                           'allOf': [{'contains': {'properties': {'name': {'const': 'learning_goal'}}}},
                                     {'contains': {'properties': {'name': {'const': 'observed_gap'}}}},
                                     {'contains': {'properties': {'name': {'const': 'restated_gap'}}}},
                                     {'contains': {'properties': {'name': {'const': 'comment_counts'}}}},
                                     {'contains': {'properties': {'name': {'const': 'deferred_findings'}}}},
                                     {'contains': {'properties': {'name': {'const': 'session_outcome'}}}}],
                           'items': {'type': 'object',
                                     'required': ['name', 'value'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'type': 'string',
                                                             'enum': ['learning_goal',
                                                                      'observed_gap',
                                                                      'restated_gap',
                                                                      'comment_counts',
                                                                      'deferred_findings',
                                                                      'session_outcome']},
                                                    'value': {}},
                                     'allOf': [{'if': {'properties': {'name': {'const': 'learning_goal'}}},
                                                'then': {'properties': {'value': {'$ref': '#/definitions/behaviour'}}}},
                                               {'if': {'properties': {'name': {'const': 'observed_gap'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['did',
                                                                                               'should'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'did': {'$ref': '#/definitions/behaviour'},
                                                                                                 'should': {'$ref': '#/definitions/behaviour'}}}}}},
                                               {'if': {'properties': {'name': {'const': 'restated_gap'}}},
                                                'then': {'properties': {'value': {'type': 'string',
                                                                                  'minLength': 20}}}},
                                               {'if': {'properties': {'name': {'const': 'comment_counts'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['issue',
                                                                                               'suggestion',
                                                                                               'question',
                                                                                               'nitpick',
                                                                                               'praise',
                                                                                               'thought'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'issue': {'type': 'integer',
                                                                                                           'minimum': 0},
                                                                                                 'suggestion': {'type': 'integer',
                                                                                                                'minimum': 0},
                                                                                                 'question': {'type': 'integer',
                                                                                                              'minimum': 0},
                                                                                                 'nitpick': {'type': 'integer',
                                                                                                             'minimum': 0},
                                                                                                 'praise': {'type': 'integer',
                                                                                                            'minimum': 1},
                                                                                                 'thought': {'type': 'integer',
                                                                                                             'minimum': 0}}}}}},
                                               {'if': {'properties': {'name': {'const': 'deferred_findings'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['url',
                                                                                                         'note'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'url': {'$ref': '#/definitions/url'},
                                                                                                           'note': {'type': 'string',
                                                                                                                    'minLength': 8}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'session_outcome'}}},
                                                'then': {'properties': {'value': {'type': 'string',
                                                                                  'enum': ['learning_goal_addressed',
                                                                                           'learning_goal_not_addressed']}}}}]}},
                'fix_commit': {'oneOf': [{'type': 'null'},
                                         {'type': 'object',
                                          'required': ['url', 'author'],
                                          'additionalProperties': False,
                                          'properties': {'url': {'$ref': '#/definitions/url'},
                                                         'author': {'$ref': '#/definitions/handle'}}}]},
                'progression': {'type': 'object',
                                'required': ['prior_record_url', 'not_demonstrated_streak'],
                                'additionalProperties': False,
                                'properties': {'prior_record_url': {'type': ['string', 'null'],
                                                                    'pattern': '^https://'},
                                               'prior_action_status': {'type': 'string',
                                                                       'enum': ['demonstrated',
                                                                                'partial',
                                                                                'not-demonstrated']},
                                               'not_demonstrated_streak': {'type': 'integer',
                                                                           'minimum': 0}},
                                'allOf': [{'if': {'properties': {'prior_record_url': {'type': 'string'}}},
                                           'then': {'required': ['prior_action_status']}},
                                          {'if': {'properties': {'prior_record_url': {'type': 'null'}}},
                                           'then': {'properties': {'not_demonstrated_streak': {'const': 0}}}}]},
                'decision': {'type': 'object',
                             'required': ['follow_up_action', 'demonstrate_in'],
                             'additionalProperties': False,
                             'properties': {'follow_up_action': {'$ref': '#/definitions/behaviour'},
                                            'demonstrate_in': {'type': 'object',
                                                               'required': ['window', 'url'],
                                                               'additionalProperties': False,
                                                               'properties': {'window': {'oneOf': [{'type': 'integer',
                                                                                                    'minimum': 1,
                                                                                                    'maximum': 14},
                                                                                                   {'type': 'string',
                                                                                                    'const': 'next-two-prs'}]},
                                                                              'url': {'type': ['string',
                                                                                               'null'],
                                                                                      'pattern': '^https://'}}},
                                            'escalation': {'type': 'object',
                                                           'required': ['intervention',
                                                                        'escalated_to'],
                                                           'additionalProperties': False,
                                                           'properties': {'intervention': {'type': 'string',
                                                                                           'enum': ['pairing-session',
                                                                                                    'structured-exercise',
                                                                                                    'course']},
                                                                          'escalated_to': {'$ref': '#/definitions/handle'}}}}},
                'junior_confirmation': {'type': 'object',
                                        'required': ['method', 'url', 'confirmed_at'],
                                        'additionalProperties': False,
                                        'properties': {'method': {'type': 'string',
                                                                  'enum': ['comment',
                                                                           'reaction',
                                                                           'co-authorship']},
                                                       'url': {'$ref': '#/definitions/url'},
                                                       'confirmed_at': {'$ref': '#/definitions/date'}}},
                'evidence': {'type': 'array',
                             'minItems': 2,
                             'items': {'$ref': '#/definitions/url'},
                             'contains': {'pattern': '#(discussion_r[0-9]+|L[0-9]+|note_[0-9]+|diff)'}},
                'status': {'type': 'string', 'enum': ['open', 'closed']}}}

OK = {'session': {'pr_url': 'https://github.com/acme/billing/pull/412',
             'junior': 'swe:bohdan',
             'senior': 'swe:alice',
             'date': '2026-09-09',
             'record_readable_by_junior': True,
             'evaluation_use': 'not-used-in-evaluation'},
 'owner': 'swe:alice',
 'inputs': [{'name': 'learning_goal',
             'value': 'writes a migration that is safe to re-run: every ALTER guarded by IF NOT '
                      'EXISTS or a state check'},
            {'name': 'observed_gap',
             'value': {'did': 'migrations/0042.py line 18 runs ALTER TABLE invoices ADD COLUMN '
                              'vat_rate unconditionally, so a second apply fails',
                       'should': 'check for the column with IF NOT EXISTS (or inspect '
                                 'information_schema) so the migration can run twice without '
                                 'error'}},
            {'name': 'restated_gap',
             'value': 'my ALTER assumes the column is absent; if the deploy retries the migration '
                      'it crashes, so I need to guard the ADD COLUMN'},
            {'name': 'comment_counts',
             'value': {'issue': 1,
                       'suggestion': 1,
                       'question': 1,
                       'nitpick': 2,
                       'praise': 1,
                       'thought': 0}},
            {'name': 'deferred_findings',
             'value': [{'url': 'https://github.com/acme/billing/pull/412/files#diff-9a1L44',
                        'note': 'unused import of Decimal; posted as an ordinary nitpick after the '
                                'session'}]},
            {'name': 'session_outcome', 'value': 'learning_goal_addressed'}],
 'fix_commit': {'url': 'https://github.com/acme/billing/pull/412/commits/c4d5e6f',
                'author': 'swe:bohdan'},
 'progression': {'prior_record_url': 'https://github.com/acme/billing/blob/main/.product/pr-mentoring-session-protocol/bohdan-2026-08-26.md',
                 'prior_action_status': 'not-demonstrated',
                 'not_demonstrated_streak': 2},
 'decision': {'follow_up_action': 'opens the next migration PR with every ALTER guarded and a '
                                  're-run test in the PR description',
              'demonstrate_in': {'window': 14, 'url': 'https://github.com/acme/billing/pull/420'}},
 'junior_confirmation': {'method': 'comment',
                         'url': 'https://github.com/acme/billing/pull/412#issuecomment-2210001',
                         'confirmed_at': '2026-09-09'},
 'evidence': ['https://github.com/acme/billing/pull/412/files#discussion_r1987001',
              'https://github.com/acme/billing/blob/main/.product/pr-mentoring-session-protocol/bohdan-2026-08-26.md',
              'https://github.com/acme/billing/pull/420'],
 'status': 'closed'}

BAD = {'session': {'pr_url': 'https://github.com/acme/billing/pull/412',
             'junior': 'swe:bohdan',
             'senior': 'swe:alice',
             'date': '2026-09-09',
             'record_readable_by_junior': True,
             'evaluation_use': 'not-used-in-evaluation'},
 'owner': 'swe:alice',
 'inputs': [{'name': 'learning_goal',
             'value': 'be more careful with migrations and think about edge cases'},
            {'name': 'observed_gap',
             'value': {'did': 'the migration was rushed and sloppy',
                       'should': 'take more time before opening the PR'}},
            {'name': 'restated_gap', 'value': 'I will be more careful next time with migrations'},
            {'name': 'comment_counts',
             'value': {'issue': 1,
                       'suggestion': 0,
                       'question': 0,
                       'nitpick': 14,
                       'praise': 0,
                       'thought': 0}},
            {'name': 'deferred_findings', 'value': []},
            {'name': 'session_outcome', 'value': 'learning_goal_addressed'}],
 'fix_commit': {'url': 'https://github.com/acme/billing/pull/412/commits/a1b2c3d',
                'author': 'swe:alice'},
 'progression': {'prior_record_url': 'https://github.com/acme/billing/blob/main/.product/pr-mentoring-session-protocol/bohdan-2026-08-26.md',
                 'not_demonstrated_streak': 3},
 'decision': {'follow_up_action': 'keep this in mind next time',
              'demonstrate_in': {'window': 30, 'url': None}},
 'junior_confirmation': {'method': 'comment',
                         'url': 'https://github.com/acme/billing/pull/412#issuecomment-2210001',
                         'confirmed_at': '2026-09-09'},
 'evidence': ['https://github.com/acme/billing/pull/412',
              'https://github.com/acme/billing/blob/main/.product/pr-mentoring-session-protocol/bohdan-2026-08-26.md'],
 'status': 'closed'}


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
    sess = obj.get("session") or {}
    fix = obj.get("fix_commit")
    if isinstance(fix, dict) and fix.get("author") != sess.get("junior"):
        errs.append(f"fix_commit.author {fix.get('author')} is not the junior {sess.get('junior')} (r-junior-restates-and-writes-the-fix)")
    counts = inputs.get("comment_counts") or {}
    others = sum(v for k, v in counts.items() if k != "nitpick" and isinstance(v, int))
    if counts.get("nitpick", 0) > others and inputs.get("session_outcome") != "learning_goal_not_addressed":
        errs.append(f"nitpick {counts.get('nitpick')} outnumbers all other labels {others}; session_outcome must be learning_goal_not_addressed (r-comments-labelled-with-counts)")
    prog, dec = obj.get("progression") or {}, obj.get("decision") or {}
    if prog.get("not_demonstrated_streak", 0) >= 3 and not dec.get("escalation"):
        errs.append("not_demonstrated_streak is 3 or more and decision.escalation is missing (r-progression-linked-to-prior-session)")
    if prog.get("prior_action_status") == "not-demonstrated" and prog.get("not_demonstrated_streak", 0) < 1:
        errs.append("prior_action_status not-demonstrated with not_demonstrated_streak 0 (r-progression-linked-to-prior-session)")
    if obj.get("status") == "closed" and not (dec.get("demonstrate_in") or {}).get("url"):
        errs.append("status closed but decision.demonstrate_in.url is null (r-follow-up-is-a-named-next-pr)")
    ev = obj.get("evidence") or []
    if prog.get("prior_record_url") and prog["prior_record_url"] not in ev:
        errs.append("progression.prior_record_url is not in evidence[] (r-progression-linked-to-prior-session)")
    fu = (dec.get("demonstrate_in") or {}).get("url")
    if fu and fu not in ev:
        errs.append("decision.demonstrate_in.url is not in evidence[] (r-follow-up-is-a-named-next-pr)")
    if obj.get("owner") != sess.get("senior"):
        errs.append("owner differs from session.senior")
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
        prog="validate-pr-mentoring-session-protocol.py",
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
