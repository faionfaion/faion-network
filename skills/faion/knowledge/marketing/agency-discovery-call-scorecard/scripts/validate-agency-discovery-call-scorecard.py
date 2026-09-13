#!/usr/bin/env python3
"""validate-agency-discovery-call-scorecard.py

Validate the artefact produced by the agency-discovery-call-scorecard methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/agency-discovery-call-scorecard.json',
 'title': 'Agency Discovery Call Scorecard rubric',
 'type': 'object',
 'required': ['rubric_version',
              'version_date',
              'version_reason',
              'axes',
              'score_range',
              'formula',
              'decision_threshold',
              'threshold_rule',
              'retro'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'datetime': {'type': 'string',
                              'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2})?(Z|[+-][0-9]{2}:[0-9]{2})$'},
                 'snake': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'},
                 'anchor': {'type': 'string',
                            'minLength': 8,
                            'not': {'pattern': '^(?i:poor|fair|good|excellent|strong|weak|low|medium|high)$'}}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'rubric_version': {'type': 'string', 'pattern': '^v[0-9]+$'},
                'version_date': {'$ref': '#/definitions/date'},
                'version_reason': {'type': 'string', 'minLength': 10},
                'axes': {'type': 'array',
                         'minItems': 4,
                         'allOf': [{'contains': {'properties': {'name': {'const': 'fit'}}}},
                                   {'contains': {'properties': {'name': {'const': 'budget'}}}},
                                   {'contains': {'properties': {'name': {'const': 'urgency'}}}},
                                   {'contains': {'properties': {'name': {'const': 'decision_maker'}}}}],
                         'items': {'type': 'object',
                                   'required': ['name', 'weight', 'anchors'],
                                   'additionalProperties': False,
                                   'properties': {'name': {'$ref': '#/definitions/snake'},
                                                  'weight': {'type': 'number',
                                                             'minimum': 0.01,
                                                             'maximum': 0.5,
                                                             'multipleOf': 0.01},
                                                  'anchors': {'type': 'array',
                                                              'minItems': 2,
                                                              'items': {'$ref': '#/definitions/anchor'}}},
                                   'allOf': [{'if': {'properties': {'name': {'const': 'budget'}}},
                                              'then': {'properties': {'anchors': {'items': {'pattern': '[0-9]'}}}}},
                                             {'if': {'properties': {'name': {'const': 'urgency'}}},
                                              'then': {'properties': {'anchors': {'items': {'pattern': '(?i)(day|week|month|quarter|Q[1-4]|20[0-9]{2}|no '
                                                                                                       'date|no '
                                                                                                       'timeline)'}}}}},
                                             {'if': {'properties': {'name': {'const': 'decision_maker'}}},
                                              'then': {'properties': {'anchors': {'items': {'pattern': '(?i)(owner|founder|partner|director|head|manager|vp|cfo|ceo|cmo|coo|procurement|sign-off|signs|approve|authority|contributor|not '
                                                                                                       'discussed)'}}}}},
                                             {'if': {'properties': {'name': {'const': 'fit'}}},
                                              'then': {'properties': {'anchors': {'items': {'pattern': '(?i)(icp|criteria|criterion|industry|size|service '
                                                                                                       'line|headcount|revenue)'}}}}}]}},
                'score_range': {'type': 'object',
                                'required': ['min', 'max'],
                                'additionalProperties': False,
                                'properties': {'min': {'const': 0}, 'max': {'const': 100}}},
                'formula': {'const': 'sum(weight * anchor_index / (anchor_count - 1)) * 100'},
                'decision_threshold': {'type': 'number',
                                       'exclusiveMinimum': 0,
                                       'exclusiveMaximum': 100},
                'threshold_rule': {'const': 'score at or above decision_threshold advances; below '
                                            'is rejected or nurtured'},
                'retro': {'type': 'object',
                          'required': ['cadence', 'same_version_only', 'compares'],
                          'additionalProperties': False,
                          'properties': {'cadence': {'const': 'weekly'},
                                         'same_version_only': {'const': True},
                                         'compares': {'type': 'array',
                                                      'minItems': 2,
                                                      'items': {'type': 'string',
                                                                'enum': ['advance_rate',
                                                                         'close_rate_of_advanced']},
                                                      'allOf': [{'contains': {'const': 'advance_rate'}},
                                                                {'contains': {'const': 'close_rate_of_advanced'}}]}}},
                'leads': {'type': 'array',
                          'items': {'type': 'object',
                                    'required': ['lead',
                                                 'call_date',
                                                 'scored_at',
                                                 'scorer_on_call',
                                                 'rubric_version',
                                                 'axis_scores',
                                                 'score',
                                                 'decision'],
                                    'additionalProperties': False,
                                    'properties': {'lead': {'type': 'string', 'minLength': 2},
                                                   'call_date': {'$ref': '#/definitions/datetime'},
                                                   'scored_at': {'$ref': '#/definitions/datetime'},
                                                   'scorer_on_call': {'const': True},
                                                   'rubric_version': {'type': 'string',
                                                                      'pattern': '^v[0-9]+$'},
                                                   'axis_scores': {'type': 'array',
                                                                   'minItems': 4,
                                                                   'items': {'type': 'object',
                                                                             'required': ['axis',
                                                                                          'anchor_index',
                                                                                          'evidence'],
                                                                             'additionalProperties': False,
                                                                             'properties': {'axis': {'$ref': '#/definitions/snake'},
                                                                                            'anchor_index': {'type': 'integer',
                                                                                                             'minimum': 0},
                                                                                            'evidence': {'type': 'string',
                                                                                                         'minLength': 15},
                                                                                            'authority_confirmed': {'type': 'boolean'}},
                                                                             'if': {'properties': {'axis': {'const': 'decision_maker'}}},
                                                                             'then': {'required': ['authority_confirmed']}}},
                                                   'score': {'type': 'number',
                                                             'minimum': 0,
                                                             'maximum': 100},
                                                   'decision': {'type': 'string',
                                                                'enum': ['advance',
                                                                         'reject',
                                                                         'nurture']}}}}}}

OK = {'rubric_version': 'v3',
 'version_date': '2026-05-04',
 'version_reason': 'budget anchors moved from 10k/30k to 15k/40k EUR after Q1 close data showed no '
                   'closed deal under 15k',
 'axes': [{'name': 'fit',
           'weight': 0.3,
           'anchors': ['outside ICP: none of industry, size or service line match',
                       'meets 1-2 of 3 ICP criteria',
                       'meets all 3 ICP criteria and asks for our core service line']},
          {'name': 'budget',
           'weight': 0.3,
           'anchors': ['no budget named or under 15k EUR per year',
                       '15k-40k EUR per year stated on the call',
                       'above 40k EUR per year stated on the call']},
          {'name': 'urgency',
           'weight': 0.2,
           'anchors': ['no date; browsing',
                       'start this quarter',
                       'start this month or a named deadline within 30 days']},
          {'name': 'decision_maker',
           'weight': 0.2,
           'anchors': ['authority not discussed, or an individual contributor',
                       'manager who must get sign-off from a named person',
                       'owner, partner or director who confirmed they approve the spend']}],
 'score_range': {'min': 0, 'max': 100},
 'formula': 'sum(weight * anchor_index / (anchor_count - 1)) * 100',
 'decision_threshold': 60,
 'threshold_rule': 'score at or above decision_threshold advances; below is rejected or nurtured',
 'retro': {'cadence': 'weekly',
           'same_version_only': True,
           'compares': ['advance_rate', 'close_rate_of_advanced']},
 'leads': [{'lead': 'Nordwind Logistics',
            'call_date': '2026-05-06T10:00:00Z',
            'scored_at': '2026-05-06T14:20:00Z',
            'scorer_on_call': True,
            'rubric_version': 'v3',
            'axis_scores': [{'axis': 'fit',
                             'anchor_index': 2,
                             'evidence': 'logistics SME, 120 staff, asked for paid search '
                                         'management: all three ICP criteria'},
                            {'axis': 'budget',
                             'anchor_index': 1,
                             'evidence': "'we have around 2,500 a month for this' = 30k EUR per "
                                         'year'},
                            {'axis': 'urgency',
                             'anchor_index': 2,
                             'evidence': "'peak season starts in June, we need campaigns live by 1 "
                                         "June'"},
                            {'axis': 'decision_maker',
                             'anchor_index': 1,
                             'evidence': "marketing manager; 'I need to run the number past our "
                                         "CFO, Eva' - authority not confirmed on the call",
                             'authority_confirmed': False}],
            'score': 75,
            'decision': 'advance'}]}

BAD = {'rubric_version': 'v3',
 'version_date': '2026-05-04',
 'version_reason': 'tweaked weights on Wednesday',
 'axes': [{'name': 'fit', 'weight': 0.4, 'anchors': ['poor', 'good', 'excellent']},
          {'name': 'budget',
           'weight': 0.4,
           'anchors': ['small budget', 'decent budget', 'large budget']},
          {'name': 'urgency',
           'weight': 0.2,
           'anchors': ['not urgent', 'somewhat urgent', 'very urgent']},
          {'name': 'decision_maker',
           'weight': 0.2,
           'anchors': ['individual contributor',
                       'manager who must get sign-off from a named person',
                       'owner or director who confirmed they approve the spend']}],
 'score_range': {'min': 0, 'max': 100},
 'formula': 'sum(weight * anchor_index / (anchor_count - 1)) * 100',
 'decision_threshold': 100,
 'threshold_rule': 'score at or above decision_threshold advances; below is rejected or nurtured',
 'retro': {'cadence': 'weekly', 'same_version_only': False, 'compares': ['advance_rate']},
 'leads': [{'lead': 'Nordwind Logistics',
            'call_date': '2026-05-06T10:00:00Z',
            'scored_at': '2026-05-09T17:00:00Z',
            'scorer_on_call': True,
            'rubric_version': 'v2',
            'axis_scores': [{'axis': 'fit',
                             'anchor_index': 2,
                             'evidence': 'seemed like a great fit overall'},
                            {'axis': 'budget',
                             'anchor_index': 2,
                             'evidence': 'they can probably afford us'},
                            {'axis': 'urgency',
                             'anchor_index': 1,
                             'evidence': 'sounded fairly keen to start'},
                            {'axis': 'decision_maker',
                             'anchor_index': 2,
                             'evidence': 'CRM title says Head of Marketing',
                             'authority_confirmed': False}],
            'score': 85,
            'decision': 'advance'}]}


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

from datetime import datetime, timedelta


def _ts(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    axes = [a for a in obj.get("axes") or [] if isinstance(a, dict)]
    total = sum(a.get("weight", 0) for a in axes)
    if abs(total - 1.0) > 0.001:
        errs.append(f"axes: weights sum to {round(total, 3)}, not 1.0 (r-weights-sum-to-one-no-dominant-axis)")
    counts = {a.get("name"): len(a.get("anchors") or []) for a in axes}
    weights = {a.get("name"): a.get("weight", 0) for a in axes}
    thr = obj.get("decision_threshold")
    for i, lead in enumerate(obj.get("leads") or []):
        if lead.get("rubric_version") != obj.get("rubric_version"):
            errs.append(f"leads[{i}]: scored under {lead.get('rubric_version')} but the rubric is {obj.get('rubric_version')}; scores across versions are not comparable (r-versioned-weekly-calibration)")
        c, s = _ts(lead.get("call_date")), _ts(lead.get("scored_at"))
        if c and s and (s < c or s - c > timedelta(hours=24)):
            errs.append(f"leads[{i}]: scored_at is not within 24 hours after call_date (r-scored-within-24h-with-evidence)")
        picks = {x.get("axis"): x for x in lead.get("axis_scores") or [] if isinstance(x, dict)}
        missing = sorted(set(counts) - set(picks))
        if missing:
            errs.append(f"leads[{i}]: no anchor pick or evidence for axes {missing} (r-scored-within-24h-with-evidence)")
        score = 0.0
        for name, x in picks.items():
            if name not in counts:
                errs.append(f"leads[{i}]: axis {name!r} is not in the rubric (r-four-axes-fit-budget-urgency-decision-maker)")
                continue
            if x.get("anchor_index", 0) >= counts[name]:
                errs.append(f"leads[{i}]: anchor_index {x.get('anchor_index')} is outside the {counts[name]} anchors of {name!r} (r-score-formula-0-100)")
                continue
            score += weights[name] * x.get("anchor_index", 0) / (counts[name] - 1)
            if name == "decision_maker" and x.get("authority_confirmed") is False and x.get("anchor_index", 0) > 1:
                errs.append(f"leads[{i}]: decision_maker scored at the top anchor with authority_confirmed false (r-decision-maker-scored-on-verified-authority)")
        if not missing and abs(round(score * 100, 1) - lead.get("score", -1)) > 0.05:
            errs.append(f"leads[{i}]: score must be {round(score * 100, 1)} by the formula from the anchor picks, got {lead.get('score')} (r-score-formula-0-100)")
        if thr is not None and lead.get("score") is not None:
            want = "advance" if lead["score"] >= thr else "reject-or-nurture"
            got = lead.get("decision")
            if (want == "advance") != (got == "advance"):
                errs.append(f"leads[{i}]: decision {got!r} contradicts score {lead['score']} against threshold {thr} (r-single-threshold-inside-range)")
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
        prog="validate-agency-discovery-call-scorecard.py",
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
