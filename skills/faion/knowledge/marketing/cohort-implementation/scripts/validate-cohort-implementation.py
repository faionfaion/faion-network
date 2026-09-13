#!/usr/bin/env python3
"""validate-cohort-implementation.py

Validate the artefact produced by the cohort-implementation methodology against the JSON Schema
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
 '$id': 'https://faion.net/schemas/cohort-implementation.json',
 'title': 'Cohort Implementation config',
 'type': 'object',
 'required': ['settings', 'sources', 'model', 'tests', 'chart'],
 'additionalProperties': False,
 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'ident': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*$'},
                 'utc_col': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]*_utc$'},
                 'rate': {'type': 'number', 'minimum': 0, 'maximum': 1}},
 'properties': {'__faion_header__': {'type': ['object', 'string']},
                'settings': {'type': 'object',
                             'required': ['warehouse_engine',
                                          'retention_event',
                                          'day_offsets',
                                          'week_start',
                                          'timezone'],
                             'additionalProperties': False,
                             'properties': {'warehouse_engine': {'type': 'string',
                                                                 'enum': ['bigquery',
                                                                          'snowflake',
                                                                          'postgres',
                                                                          'redshift']},
                                            'retention_event': {'$ref': '#/definitions/ident'},
                                            'day_offsets': {'type': 'array',
                                                            'minItems': 1,
                                                            'uniqueItems': True,
                                                            'items': {'type': 'integer',
                                                                      'minimum': 1}},
                                            'week_start': {'const': 'monday'},
                                            'timezone': {'const': 'UTC'}}},
                'sources': {'type': 'object',
                            'required': ['users_table',
                                         'events_table',
                                         'user_id_column',
                                         'identity_resolved_upstream',
                                         'signup_ts_column',
                                         'event_ts_column'],
                            'additionalProperties': False,
                            'properties': {'users_table': {'$ref': '#/definitions/ident'},
                                           'events_table': {'$ref': '#/definitions/ident'},
                                           'user_id_column': {'const': 'user_id'},
                                           'identity_resolved_upstream': {'const': True},
                                           'signup_ts_column': {'$ref': '#/definitions/utc_col'},
                                           'event_ts_column': {'$ref': '#/definitions/utc_col'}}},
                'model': {'type': 'object',
                          'required': ['name',
                                       'materialized',
                                       'unique_key',
                                       'partition_by',
                                       'lookback_days',
                                       'cohort_week_expr',
                                       'join_condition',
                                       'denominator_source',
                                       'retention_event_declared_in'],
                          'additionalProperties': False,
                          'properties': {'name': {'$ref': '#/definitions/ident'},
                                         'materialized': {'const': 'incremental'},
                                         'unique_key': {'type': 'array',
                                                        'minItems': 3,
                                                        'maxItems': 3,
                                                        'items': [{'const': 'cohort_week'},
                                                                  {'const': 'day_offset'},
                                                                  {'const': 'user_id'}]},
                                         'partition_by': {'const': 'cohort_week'},
                                         'lookback_days': {'type': 'integer', 'minimum': 1},
                                         'cohort_week_expr': {'type': 'string',
                                                              'minLength': 10,
                                                              'pattern': '(?i)monday'},
                                         'join_condition': {'const': 'event_ts_utc >= '
                                                                     'signup_ts_utc'},
                                         'denominator_source': {'const': 'users_table'},
                                         'retention_event_declared_in': {'type': 'array',
                                                                         'minItems': 3,
                                                                         'items': {'type': 'string',
                                                                                   'enum': ['sql',
                                                                                            'schema_yml',
                                                                                            'settings']},
                                                                         'allOf': [{'contains': {'const': 'sql'}},
                                                                                   {'contains': {'const': 'schema_yml'}},
                                                                                   {'contains': {'const': 'settings'}}]}}},
                'tests': {'type': 'object',
                          'required': ['not_null', 'accepted_values'],
                          'additionalProperties': False,
                          'properties': {'not_null': {'type': 'array',
                                                      'minItems': 3,
                                                      'items': {'$ref': '#/definitions/ident'},
                                                      'allOf': [{'contains': {'const': 'cohort_week'}},
                                                                {'contains': {'const': 'day_offset'}},
                                                                {'contains': {'const': 'user_id'}}]},
                                         'accepted_values': {'type': 'object',
                                                             'required': ['column', 'values'],
                                                             'additionalProperties': False,
                                                             'properties': {'column': {'const': 'day_offset'},
                                                                            'values': {'type': 'array',
                                                                                       'minItems': 1,
                                                                                       'items': {'type': 'integer',
                                                                                                 'minimum': 1}}}}}},
                'chart': {'type': 'object',
                          'required': ['data_cutoff',
                                       'x',
                                       'series',
                                       'metric',
                                       'immature_value',
                                       'render_immature_as'],
                          'additionalProperties': False,
                          'properties': {'data_cutoff': {'$ref': '#/definitions/date'},
                                         'x': {'const': 'cohort_week'},
                                         'series': {'const': 'day_offset'},
                                         'metric': {'const': 'retained_users / cohort_users'},
                                         'immature_value': {'type': 'null'},
                                         'render_immature_as': {'const': 'blank'}}},
                'cells': {'type': 'array',
                          'items': {'type': 'object',
                                    'required': ['cohort_week',
                                                 'day_offset',
                                                 'cohort_users',
                                                 'retained_users',
                                                 'retention'],
                                    'additionalProperties': False,
                                    'properties': {'cohort_week': {'$ref': '#/definitions/date'},
                                                   'day_offset': {'type': 'integer', 'minimum': 1},
                                                   'cohort_users': {'type': 'integer',
                                                                    'minimum': 1},
                                                   'retained_users': {'type': ['integer', 'null'],
                                                                      'minimum': 0},
                                                   'retention': {'anyOf': [{'$ref': '#/definitions/rate'},
                                                                           {'type': 'null'}]}}}}}}

OK = {'settings': {'warehouse_engine': 'bigquery',
              'retention_event': 'login',
              'day_offsets': [1, 7, 14, 30, 60, 90],
              'week_start': 'monday',
              'timezone': 'UTC'},
 'sources': {'users_table': 'stg_users',
             'events_table': 'stg_events',
             'user_id_column': 'user_id',
             'identity_resolved_upstream': True,
             'signup_ts_column': 'signup_ts_utc',
             'event_ts_column': 'event_ts_utc'},
 'model': {'name': 'cohort_retention_weekly',
           'materialized': 'incremental',
           'unique_key': ['cohort_week', 'day_offset', 'user_id'],
           'partition_by': 'cohort_week',
           'lookback_days': 90,
           'cohort_week_expr': 'CAST(DATE_TRUNC(DATE(signup_ts_utc), WEEK(MONDAY)) AS DATE)',
           'join_condition': 'event_ts_utc >= signup_ts_utc',
           'denominator_source': 'users_table',
           'retention_event_declared_in': ['sql', 'schema_yml', 'settings']},
 'tests': {'not_null': ['cohort_week', 'day_offset', 'user_id'],
           'accepted_values': {'column': 'day_offset', 'values': [1, 7, 14, 30, 60, 90]}},
 'chart': {'data_cutoff': '2026-05-04',
           'x': 'cohort_week',
           'series': 'day_offset',
           'metric': 'retained_users / cohort_users',
           'immature_value': None,
           'render_immature_as': 'blank'},
 'cells': [{'cohort_week': '2026-01-05',
            'day_offset': 90,
            'cohort_users': 1502,
            'retained_users': 240,
            'retention': 0.16},
           {'cohort_week': '2026-03-30',
            'day_offset': 1,
            'cohort_users': 1810,
            'retained_users': 1050,
            'retention': 0.58},
           {'cohort_week': '2026-03-30',
            'day_offset': 7,
            'cohort_users': 1810,
            'retained_users': 706,
            'retention': 0.39},
           {'cohort_week': '2026-03-30',
            'day_offset': 14,
            'cohort_users': 1810,
            'retained_users': 543,
            'retention': 0.3},
           {'cohort_week': '2026-03-30',
            'day_offset': 30,
            'cohort_users': 1810,
            'retained_users': None,
            'retention': None}]}

BAD = {'settings': {'warehouse_engine': 'bigquery',
              'retention_event': 'login',
              'day_offsets': [1, 7, 14, 30, 60, 90],
              'week_start': 'monday',
              'timezone': 'UTC'},
 'sources': {'users_table': 'stg_users',
             'events_table': 'stg_events',
             'user_id_column': 'distinct_id',
             'identity_resolved_upstream': False,
             'signup_ts_column': 'signup_ts_local',
             'event_ts_column': 'event_ts_utc'},
 'model': {'name': 'cohort_retention_weekly',
           'materialized': 'incremental',
           'unique_key': ['cohort_week', 'day_offset', 'user_id'],
           'partition_by': 'cohort_week',
           'lookback_days': 30,
           'cohort_week_expr': 'DATE_TRUNC(DATE(signup_ts_local), WEEK)',
           'join_condition': 'event_ts_utc >= signup_ts_utc',
           'denominator_source': 'model_rows',
           'retention_event_declared_in': ['sql']},
 'tests': {'not_null': ['cohort_week', 'day_offset'],
           'accepted_values': {'column': 'day_offset', 'values': [1, 7, 30]}},
 'chart': {'data_cutoff': '2026-05-04',
           'x': 'cohort_week',
           'series': 'day_offset',
           'metric': 'retained_users / cohort_users',
           'immature_value': 0,
           'render_immature_as': 'zero'},
 'cells': [{'cohort_week': '2026-03-30',
            'day_offset': 1,
            'cohort_users': 1050,
            'retained_users': 1050,
            'retention': 1.0},
           {'cohort_week': '2026-03-30',
            'day_offset': 30,
            'cohort_users': 1810,
            'retained_users': 0,
            'retention': 0},
           {'cohort_week': '2026-04-01',
            'day_offset': 3,
            'cohort_users': 1810,
            'retained_users': 900,
            'retention': 0.497}]}


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
    st = obj.get("settings") or {}
    offsets = list(st.get("day_offsets") or [])
    model = obj.get("model") or {}
    if offsets and model.get("lookback_days", 0) < max(offsets):
        errs.append(f"model.lookback_days {model.get('lookback_days')} is below the largest day_offset {max(offsets)}; late events for older cohorts never land (r-incremental-key-partition-and-lookback)")
    if offsets != sorted(offsets):
        errs.append("settings.day_offsets must be ascending (r-fixed-day-offsets-enforced-by-test)")
    av = ((obj.get("tests") or {}).get("accepted_values") or {}).get("values")
    if av is not None and sorted(av) != sorted(offsets):
        errs.append(f"tests.accepted_values.values {av} differs from settings.day_offsets {offsets} (r-fixed-day-offsets-enforced-by-test, r-settings-declare-engine-event-offsets)")
    src = obj.get("sources") or {}
    expr = model.get("cohort_week_expr", "")
    if src.get("signup_ts_column") and src["signup_ts_column"] not in expr:
        errs.append(f"model.cohort_week_expr does not read sources.signup_ts_column {src['signup_ts_column']!r} (r-cohort-key-signup-week-monday-utc)")
    cutoff = _d((obj.get("chart") or {}).get("data_cutoff", ""))
    for i, c in enumerate(obj.get("cells") or []):
        cw = _d(c.get("cohort_week", ""))
        if cw and cw.weekday() != 0:
            errs.append(f"cells[{i}]: cohort_week {cw} is not a Monday (r-cohort-key-signup-week-monday-utc)")
        if offsets and c.get("day_offset") not in offsets:
            errs.append(f"cells[{i}]: day_offset {c.get('day_offset')} is not in settings.day_offsets (r-fixed-day-offsets-enforced-by-test)")
        mature = bool(cw and cutoff and cw + timedelta(days=6 + c.get("day_offset", 0)) <= cutoff)
        ret, rate = c.get("retained_users"), c.get("retention")
        if not mature and (ret is not None or rate is not None):
            errs.append(f"cells[{i}]: cohort {cw} at day {c.get('day_offset')} is not mature on {cutoff} (week end + offset = {cw + timedelta(days=6 + c.get('day_offset', 0)) if cw else '?'}); retained_users and retention must be null, never 0 (r-incomplete-cells-null-not-zero)")
        if mature and (ret is None or rate is None):
            errs.append(f"cells[{i}]: mature cell carries null values (r-incomplete-cells-null-not-zero)")
        if ret is not None:
            if ret > c.get("cohort_users", 0):
                errs.append(f"cells[{i}]: retained_users exceeds cohort_users; the denominator must be the full cohort from the users table (r-denominator-is-full-cohort)")
            elif rate is not None and c.get("cohort_users") and abs(round(ret / c["cohort_users"], 3) - rate) > 0.0055:
                errs.append(f"cells[{i}]: retention must be retained_users / cohort_users = {round(ret / c['cohort_users'], 3)} (r-denominator-is-full-cohort)")
            if ret == c.get("cohort_users") and c.get("day_offset", 0) >= 1:
                errs.append(f"cells[{i}]: retention of 100 percent at day {c.get('day_offset')} is the row-count denominator (r-denominator-is-full-cohort)")
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
        prog="validate-cohort-implementation.py",
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
