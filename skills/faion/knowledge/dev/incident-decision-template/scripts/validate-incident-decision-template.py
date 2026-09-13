#!/usr/bin/env python3
"""validate-incident-decision-template.py

Validate an incident decision record against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the incident-decision-template methodology, plus the
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
 '$id': 'https://faion.net/schemas/incident-decision-template.json',
 'title': 'Incident decision record',
 'type': 'object',
 'required': ['trigger', 'owner', 'inputs', 'decision', 'evidence', 'review'],
 'additionalProperties': False,
 'definitions': {'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                 'timestamp': {'type': 'string',
                               'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2})?(Z|[+-][0-9]{2}:[0-9]{2})$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}},
 'properties': {'__faion_header__': {'type': 'object'},
                'trigger': {'type': 'object',
                            'required': ['kind',
                                         'url',
                                         'incident_id',
                                         'decided_at',
                                         'committed_at',
                                         'bridge_open_at_commit'],
                            'additionalProperties': False,
                            'properties': {'kind': {'type': 'string', 'const': 'incident'},
                                           'url': {'type': 'string', 'pattern': '^https://'},
                                           'incident_id': {'type': 'string', 'minLength': 3},
                                           'decided_at': {'$ref': '#/definitions/timestamp'},
                                           'committed_at': {'$ref': '#/definitions/timestamp'},
                                           'bridge_open_at_commit': {'type': 'boolean'}}},
                'owner': {'$ref': '#/definitions/handle'},
                'inputs': {'type': 'array',
                           'minItems': 3,
                           'allOf': [{'contains': {'properties': {'name': {'const': 'options_considered'}}}},
                                     {'contains': {'properties': {'name': {'const': 'blast_radius'}}}},
                                     {'contains': {'properties': {'name': {'const': 'rollback_trigger'}}}}],
                           'items': {'type': 'object',
                                     'required': ['name', 'value'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'type': 'string',
                                                             'enum': ['options_considered',
                                                                      'blast_radius',
                                                                      'rollback_trigger',
                                                                      'executor',
                                                                      'reconstructed']},
                                                    'value': {}},
                                     'allOf': [{'if': {'properties': {'name': {'const': 'options_considered'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'minItems': 2,
                                                                                  'items': {'type': 'string',
                                                                                            'minLength': 12},
                                                                                  'contains': {'type': 'string',
                                                                                               'pattern': '[Dd]o '
                                                                                                          'nothing|[Kk]eep '
                                                                                                          'observing'}}}}},
                                               {'if': {'properties': {'name': {'const': 'blast_radius'}}},
                                                'then': {'properties': {'value': {'type': 'string',
                                                                                  'minLength': 10,
                                                                                  'pattern': '[0-9]'}}}},
                                               {'if': {'properties': {'name': {'const': 'rollback_trigger'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['metric',
                                                                                               'threshold',
                                                                                               'window',
                                                                                               'rollback'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'metric': {'type': 'string',
                                                                                                            'minLength': 3},
                                                                                                 'threshold': {'type': 'string',
                                                                                                               'minLength': 2,
                                                                                                               'pattern': '[0-9]'},
                                                                                                 'window': {'type': 'string',
                                                                                                            'minLength': 2,
                                                                                                            'pattern': '[0-9]'},
                                                                                                 'rollback': {'type': 'string',
                                                                                                              'minLength': 4}}}}}},
                                               {'if': {'properties': {'name': {'const': 'executor'}}},
                                                'then': {'properties': {'value': {'$ref': '#/definitions/handle'}}}},
                                               {'if': {'properties': {'name': {'const': 'reconstructed'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['reconstructed',
                                                                                               'at'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'reconstructed': {'const': True},
                                                                                                 'at': {'$ref': '#/definitions/timestamp'}}}}}}]}},
                'decision': {'type': 'string',
                             'minLength': 12,
                             'pattern': '^(?![\\s\\S]*([Cc]onsider|[Mm]aybe|[Ll]ook into|[Ss]hould '
                                        'probably))[^.!?]+[.!]?$'},
                'evidence': {'type': 'array',
                             'minItems': 1,
                             'items': {'type': 'string', 'pattern': '^https://'}},
                'review': {'type': 'object',
                           'required': ['postmortem_date', 'next_review_at'],
                           'additionalProperties': False,
                           'properties': {'postmortem_date': {'$ref': '#/definitions/date'},
                                          'next_review_at': {'$ref': '#/definitions/date'},
                                          'outcome': {'type': 'object',
                                                      'required': ['rollback_trigger_fired',
                                                                   'blast_radius_matched',
                                                                   'reviewed_at'],
                                                      'additionalProperties': False,
                                                      'properties': {'rollback_trigger_fired': {'type': 'boolean'},
                                                                     'blast_radius_matched': {'type': 'boolean'},
                                                                     'measured_blast_radius': {'type': 'string'},
                                                                     'reviewed_at': {'$ref': '#/definitions/date'}}}}}}}

OK = {'trigger': {'kind': 'incident',
             'url': 'https://acme.pagerduty.com/incidents/Q2X4',
             'incident_id': 'INC-2417',
             'decided_at': '2026-09-12T02:14:00Z',
             'committed_at': '2026-09-12T02:15:40Z',
             'bridge_open_at_commit': True},
 'owner': 'ic:alice',
 'inputs': [{'name': 'options_considered',
             'value': ['disable the recommendations sidecar in eu-west-1 (chosen: isolates the '
                       'failing dependency, 1 min to apply)',
                       'roll back the full checkout release 41 -> 40 (rejected: 20 min, widens '
                       'blast radius to all regions)',
                       'do nothing / keep observing for 10 min (rejected: 5xx rate rising 0.4 pp '
                       'per minute)']},
            {'name': 'blast_radius',
             'value': '38% of checkout requests in eu-west-1 returning 5xx, approx. 1,900 req/min, '
                      '3 tenants on dedicated shards unaffected'},
            {'name': 'rollback_trigger',
             'value': {'metric': 'checkout_http_5xx_rate (grafana: checkout-overview)',
                       'threshold': 'above 2%',
                       'window': '5 consecutive minutes',
                       'rollback': 'helm rollback checkout 41 -n prod-eu-west-1'}},
            {'name': 'executor', 'value': 'sre:bob'}],
 'decision': 'Disable the recommendations sidecar in eu-west-1 now.',
 'evidence': ['https://grafana.acme.internal/d/checkout-overview?from=1789178400000&to=1789180200000&var-region=eu-west-1',
              'https://acme.pagerduty.com/incidents/Q2X4/alerts/A7',
              'https://acme.slack.com/archives/C0INC2417/p1789178040001200'],
 'review': {'postmortem_date': '2026-09-15',
            'next_review_at': '2026-09-15',
            'outcome': {'rollback_trigger_fired': False,
                        'blast_radius_matched': True,
                        'measured_blast_radius': '36% of eu-west-1 checkout requests over 11 '
                                                 'minutes',
                        'reviewed_at': '2026-09-15'}}}

BAD = {'trigger': {'kind': 'incident',
             'url': 'https://acme.pagerduty.com/incidents/Q2X4',
             'incident_id': 'INC-2417',
             'decided_at': '2026-09-12T02:14:00Z',
             'committed_at': '2026-09-12T02:15:40Z',
             'bridge_open_at_commit': True},
 'owner': 'sre:bob',
 'inputs': [{'name': 'options_considered',
             'value': ['disable the recommendations sidecar in eu-west-1 (chosen)']},
            {'name': 'blast_radius', 'value': 'some EU users seeing errors on checkout'},
            {'name': 'rollback_trigger',
             'value': {'metric': 'checkout errors',
                       'threshold': 'if it gets worse',
                       'window': 'a while',
                       'rollback': 'roll back'}},
            {'name': 'executor', 'value': 'sre:bob'}],
 'decision': 'We should probably consider disabling the sidecar and look into the release.',
 'evidence': ['https://grafana.acme.internal/d/checkout-overview',
              'https://docs.acme.internal/runbooks/checkout'],
 'review': {'postmortem_date': '2026-09-15', 'next_review_at': '2026-12-15'}}


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


from datetime import datetime

_DASH = re.compile(r"grafana|datadog|kibana|/d/|dashboard", re.I)
_PINNED = re.compile(r"[?&](from|to|start|end|time|_g)=", re.I)
_DOCS = re.compile(r"docs\.|/docs/|wiki|confluence|runbook", re.I)


def _ts(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    trig = obj.get("trigger") or {}
    names = {i.get("name"): i.get("value") for i in obj.get("inputs") or [] if isinstance(i, dict)}
    d, c = _ts(trig.get("decided_at", "")), _ts(trig.get("committed_at", ""))
    late = d and c and (c - d).total_seconds() > 120
    if (late or trig.get("bridge_open_at_commit") is False) and "reconstructed" not in names:
        errs.append("trigger: committed more than 2 minutes after the decision or after the bridge closed, and no `reconstructed` entry (r-record-before-bridge-closes)")
    ev = obj.get("evidence") or []
    for i, u in enumerate(ev):
        if _DASH.search(u) and not _PINNED.search(u):
            errs.append(f"evidence[{i}]: dashboard URL without a pinned time range (r-evidence-is-timestamped-signal)")
    if ev and all(_DOCS.search(u) for u in ev):
        errs.append("evidence: only documentation pages; add the pinned dashboard, alert or chat permalink (r-evidence-is-timestamped-signal)")
    rv = obj.get("review") or {}
    if rv.get("next_review_at", "") > rv.get("postmortem_date", ""):
        errs.append("review.next_review_at is later than review.postmortem_date (r-review-at-postmortem)")
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
        prog="validate-incident-decision-template.py",
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
