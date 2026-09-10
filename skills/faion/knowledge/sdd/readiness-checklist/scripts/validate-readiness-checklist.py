#!/usr/bin/env python3
"""validate-readiness-checklist.py

Validate the artefact produced by the readiness-checklist methodology against the JSON
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
 '$id': 'https://faion.net/schemas/sdd/readiness-checklist.json',
 'title': 'Readiness Checklist (readiness.md)',
 'type': 'object',
 'required': ['feature_id', 'path', 'reviewer', 'items', 'verdict'],
 'additionalProperties': False,
 'properties': {'feature_id': {'type': 'string', 'pattern': '^F[0-9]{3,}$'},
                'path': {'type': 'string',
                         'pattern': '^features/in-progress/F[0-9]{3,}-[a-z0-9-]+/readiness\\.md$'},
                'reviewer': {'type': 'string', 'minLength': 2},
                'verdict': {'type': 'string', 'enum': ['done', 'blocked']},
                'items': {'type': 'array',
                          'minItems': 10,
                          'maxItems': 10,
                          'items': {'type': 'object',
                                    'required': ['n', 'title', 'applies', 'ticked'],
                                    'additionalProperties': False,
                                    'properties': {'n': {'type': 'integer',
                                                         'minimum': 1,
                                                         'maximum': 10},
                                                   'title': {'type': 'string', 'minLength': 1},
                                                   'applies': {'type': 'boolean'},
                                                   'ticked': {'type': 'boolean'},
                                                   'evidence': {'type': 'array',
                                                                'minItems': 1,
                                                                'items': {'type': 'string',
                                                                          'format': 'uri-reference',
                                                                          'minLength': 1}},
                                                   'reason': {'type': 'string', 'minLength': 1}},
                                    'allOf': [{'if': {'properties': {'ticked': {'const': True}}},
                                               'then': {'required': ['evidence']}},
                                              {'if': {'properties': {'applies': {'const': False}}},
                                               'then': {'required': ['reason'],
                                                        'properties': {'ticked': {'const': False}}}}]}}}}

OK: dict = {'feature_id': 'F012',
 'path': 'features/in-progress/F012-billing-export/readiness.md',
 'reviewer': 'main-thread',
 'verdict': 'blocked',
 'items': [{'n': 1,
            'title': 'ACs evidence',
            'applies': True,
            'ticked': True,
            'evidence': ['tests/api/test_export.py::test_csv_columns',
                         'screenshots/F012-export-success.png']},
           {'n': 2,
            'title': 'tasks done',
            'applies': True,
            'ticked': True,
            'evidence': ['features/in-progress/F012-billing-export/tasks/done/']},
           {'n': 3,
            'title': 'commit hygiene',
            'applies': True,
            'ticked': True,
            'evidence': ['git log --oneline main..F012']},
           {'n': 4,
            'title': 'CI green',
            'applies': True,
            'ticked': True,
            'evidence': ['https://ci.example.com/runs/4471']},
           {'n': 5,
            'title': 'API tests',
            'applies': True,
            'ticked': True,
            'evidence': ['https://ci.example.com/runs/4471#pytest-apps-billing-tests-api']},
           {'n': 6,
            'title': 'Playwright pos+neg',
            'applies': False,
            'ticked': False,
            'reason': 'no user-facing flow: export is triggered by an existing button, no new page '
                      'or form'},
           {'n': 7,
            'title': 'UI heuristics',
            'applies': False,
            'ticked': False,
            'reason': 'no UI impact: no rendered element changed'},
           {'n': 8,
            'title': 'spec delta',
            'applies': True,
            'ticked': True,
            'evidence': ['project-spec/api.md#billing-export (same PR)']},
           {'n': 9,
            'title': 'surface coupling',
            'applies': True,
            'ticked': True,
            'evidence': ["grep 'path: /billing' project-spec/api.md — sibling /billing/invoices, "
                         'no overlap']},
           {'n': 10, 'title': 'deployed', 'applies': True, 'ticked': False}]}
BAD: dict = {'feature_id': 'F012',
 'path': 'features/in-progress/F012-billing-export/readiness.md',
 'reviewer': 'team',
 'verdict': 'done',
 'items': [{'n': 1, 'title': 'ACs evidence', 'applies': True, 'ticked': True},
           {'n': 5, 'title': 'API tests', 'applies': False, 'ticked': False},
           {'n': 9,
            'title': 'surface coupling',
            'applies': True,
            'ticked': True,
            'evidence': ['no public surface']}]}

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
    ap = argparse.ArgumentParser(prog="validate-readiness-checklist.py", description=__doc__,
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
