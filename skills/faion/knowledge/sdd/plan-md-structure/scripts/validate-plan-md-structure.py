#!/usr/bin/env python3
"""validate-plan-md-structure.py

Validate the artefact produced by the plan-md-structure methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only; implements the
draft-07 subset the contract uses (required, type, enum, const, pattern,
minimum/maximum, minLength/maxLength, minItems, items, properties,
additionalProperties, allOf/anyOf/oneOf/not, if/then/else). The schema is embedded verbatim below; regenerate this
file when the contract changes.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid and invalid examples
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

SCHEMA: dict = {'$schema': 'http://json-schema.org/draft-07/schema#',
 '$id': 'https://faion.net/schemas/plan-md-structure.json',
 'type': 'object',
 'required': ['feature', 'skipped', 'files'],
 'additionalProperties': False,
 'properties': {'feature': {'type': 'string', 'pattern': '^F[0-9]{3,}$'},
                'skipped': {'type': 'boolean'},
                'skip_reason': {'type': 'string', 'minLength': 1},
                'task_count': {'type': 'integer', 'minimum': 0},
                'new_contract': {'type': 'boolean'},
                'files': {'type': 'array',
                          'items': {'type': 'string',
                                    'not': {'enum': ['design.md', 'implementation-plan.md']}}},
                'design': {'type': 'object',
                           'required': ['package_layout', 'api_contracts', 'schemas', 'sequencing'],
                           'properties': {'package_layout': {'type': 'array',
                                                             'items': {'type': 'string'}},
                                          'api_contracts': {'type': 'array',
                                                            'items': {'type': 'string'}},
                                          'schemas': {'type': 'array', 'items': {'type': 'string'}},
                                          'sequencing': {'type': 'array',
                                                         'items': {'type': 'string'}},
                                          'tradeoffs': {'type': 'array',
                                                        'items': {'type': 'string'}}}},
                'execution_plan': {'type': 'object',
                                   'required': ['waves', 'tasks', 'risks', 'rollback'],
                                   'properties': {'waves': {'type': 'array',
                                                            'minItems': 1,
                                                            'items': {'type': 'object',
                                                                      'required': ['name',
                                                                                   'mode',
                                                                                   'tasks'],
                                                                      'properties': {'name': {'type': 'string'},
                                                                                     'mode': {'type': 'string',
                                                                                              'enum': ['serial',
                                                                                                       'parallel']},
                                                                                     'tasks': {'type': 'array',
                                                                                               'items': {'type': 'string',
                                                                                                         'pattern': '^T[0-9]{2,}$'}}}}},
                                                  'tasks': {'type': 'array',
                                                            'minItems': 1,
                                                            'items': {'type': 'object',
                                                                      'required': ['id',
                                                                                   'description',
                                                                                   'deps',
                                                                                   'est_tokens'],
                                                                      'properties': {'id': {'type': 'string',
                                                                                            'pattern': '^T[0-9]{2,}$'},
                                                                                     'description': {'type': 'string',
                                                                                                     'minLength': 1},
                                                                                     'deps': {'type': 'array',
                                                                                              'items': {'type': 'string',
                                                                                                        'pattern': '^T[0-9]{2,}$'}},
                                                                                     'est_tokens': {'type': 'string'}}}},
                                                  'risks': {'type': 'array',
                                                            'items': {'type': 'string'}},
                                                  'rollback': {'type': 'string', 'minLength': 1}}}},
 'allOf': [{'if': {'properties': {'skipped': {'const': True}}},
            'then': {'required': ['skip_reason'],
                     'properties': {'task_count': {'maximum': 3},
                                    'new_contract': {'const': False},
                                    'files': {'maxItems': 0}}},
            'else': {'required': ['design', 'execution_plan'],
                     'properties': {'files': {'minItems': 1,
                                              'maxItems': 1,
                                              'items': {'const': 'plan.md'}}}}}]}

OK: dict = {'feature': 'F042',
 'skipped': False,
 'task_count': 6,
 'new_contract': True,
 'files': ['plan.md'],
 'design': {'package_layout': ['apps/accounts/verification/', 'apps/notifications/email/'],
            'api_contracts': ['POST /v1/verify {token} -> 204 | 410 token-expired'],
            'schemas': ['users.verified_at timestamptz null'],
            'sequencing': ['T02 must run after the T01 migration is deployed'],
            'tradeoffs': ['Token in URL vs 6-digit code: URL chosen; one click, no second input '
                          'field.']},
 'execution_plan': {'waves': [{'name': 'A', 'mode': 'serial', 'tasks': ['T01', 'T02']},
                              {'name': 'B', 'mode': 'parallel', 'tasks': ['T03', 'T04', 'T05']},
                              {'name': 'C', 'mode': 'serial', 'tasks': ['T06']}],
                    'tasks': [{'id': 'T01',
                               'description': 'Migration: add verified_at',
                               'deps': [],
                               'est_tokens': '~3k'},
                              {'id': 'T02',
                               'description': 'Serializer: expose verified',
                               'deps': ['T01'],
                               'est_tokens': '~2k'},
                              {'id': 'T03',
                               'description': 'Email service: send verify mail',
                               'deps': [],
                               'est_tokens': '~5k'},
                              {'id': 'T04',
                               'description': 'Verify endpoint',
                               'deps': [],
                               'est_tokens': '~4k'},
                              {'id': 'T05',
                               'description': 'Resend throttle',
                               'deps': [],
                               'est_tokens': '~2k'},
                              {'id': 'T06',
                               'description': 'Integration test T03-T05',
                               'deps': ['T03', 'T04', 'T05'],
                               'est_tokens': '~3k'}],
                    'risks': ['Mail provider rate limit during backfill — mitigate with batched '
                              'sends.'],
                    'rollback': 'Revert the migration (column is nullable), feature-flag the '
                                'verify endpoint off.'}}
BAD: dict = {'feature': 'F043',
 'skipped': True,
 'task_count': 6,
 'new_contract': True,
 'files': ['design.md', 'implementation-plan.md']}

_TYPES = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float),
           "boolean": bool, "null": type(None)}


def _check(node: dict, value, path: str, errs: list[str]) -> None:
    t = node.get("type")
    if t:
        allowed = t if isinstance(t, list) else [t]
        ok = any(isinstance(value, _TYPES[a]) and not (a in ("integer", "number") and isinstance(value, bool))
                 for a in allowed if a in _TYPES)
        if not ok:
            errs.append(f"{path}: expected type {t}, got {type(value).__name__}")
            return
    if "const" in node and value != node["const"]:
        errs.append(f"{path}: must equal {node['const']!r}")
    if "enum" in node and value not in node["enum"]:
        errs.append(f"{path}: {value!r} not in {node['enum']!r}")
    if isinstance(value, str):
        if "pattern" in node and not re.search(node["pattern"], value):
            errs.append(f"{path}: {value!r} does not match {node['pattern']!r}")
        if "minLength" in node and len(value) < node["minLength"]:
            errs.append(f"{path}: shorter than minLength {node['minLength']}")
        if "maxLength" in node and len(value) > node["maxLength"]:
            errs.append(f"{path}: longer than maxLength {node['maxLength']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in node and value < node["minimum"]:
            errs.append(f"{path}: {value} below minimum {node['minimum']}")
        if "maximum" in node and value > node["maximum"]:
            errs.append(f"{path}: {value} above maximum {node['maximum']}")
    if isinstance(value, list):
        if "minItems" in node and len(value) < node["minItems"]:
            errs.append(f"{path}: fewer than minItems {node['minItems']}")
        if "maxItems" in node and len(value) > node["maxItems"]:
            errs.append(f"{path}: more than maxItems {node['maxItems']}")
        if isinstance(node.get("items"), dict):
            for i, item in enumerate(value):
                _check(node["items"], item, f"{path}[{i}]", errs)
    if isinstance(value, dict):
        for k in node.get("required", []):
            if k not in value:
                errs.append(f"{path}: missing required field {k!r}")
        props = node.get("properties", {})
        for k, sub in props.items():
            if k in value and isinstance(sub, dict):
                _check(sub, value[k], f"{path}.{k}", errs)
        if node.get("additionalProperties") is False:
            for k in value:
                if k not in props:
                    errs.append(f"{path}: unexpected field {k!r}")

    # combinators and conditionals (draft-07 §6.7) — the sdd contracts use all four
    for sub in node.get("allOf", []):
        _check(sub, value, path, errs)
    if "anyOf" in node and not any(not _errs(sub, value, path) for sub in node["anyOf"]):
        errs.append(f"{path}: matches none of anyOf")
    if "oneOf" in node and sum(1 for sub in node["oneOf"] if not _errs(sub, value, path)) != 1:
        errs.append(f"{path}: must match exactly one of oneOf")
    if "not" in node and not _errs(node["not"], value, path):
        errs.append(f"{path}: matches the schema it must not")
    if "if" in node:
        branch = "then" if not _errs(node["if"], value, path) else "else"
        if isinstance(node.get(branch), dict):
            _check(node[branch], value, path, errs)

def _errs(node: dict, value, path: str) -> list[str]:
    out: list[str] = []
    _check(node, value, path, out)
    return out


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    _check(SCHEMA, obj, "$", errs)
    return errs


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: the contract's valid example was rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: the contract's invalid example was accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="validate-plan-md-structure.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run the contract's examples and exit")
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
