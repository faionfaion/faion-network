#!/usr/bin/env python3
"""validate-quality-gates.py

Validate the artefact produced by the quality-gates methodology against the JSON
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
 '$id': 'https://faion.net/schemas/quality-gates.json',
 'type': 'object',
 'required': ['change', 'layers_touched', 'required_gates', 'readiness', 'ci'],
 'additionalProperties': False,
 'definitions': {'gate': {'type': 'string',
                          'enum': ['unit',
                                   'api',
                                   'playwright-happy',
                                   'playwright-pos-neg',
                                   'ui-audit',
                                   'migration',
                                   'reversibility',
                                   'smoke']}},
 'properties': {'change': {'type': 'string', 'pattern': '^(F|CR|BUG)[0-9]{3,}$'},
                'layers_source': {'type': 'string', 'const': 'git-diff'},
                'layers_touched': {'type': 'array',
                                   'minItems': 1,
                                   'uniqueItems': True,
                                   'items': {'type': 'string',
                                             'enum': ['backend',
                                                      'frontend',
                                                      'user-facing-flow',
                                                      'pure-data',
                                                      'infra']}},
                'required_gates': {'type': 'array',
                                   'minItems': 1,
                                   'uniqueItems': True,
                                   'items': {'$ref': '#/definitions/gate'}},
                'readiness': {'type': 'array',
                              'minItems': 1,
                              'items': {'type': 'object',
                                        'required': ['gate', 'status'],
                                        'properties': {'gate': {'$ref': '#/definitions/gate'},
                                                       'status': {'type': 'string',
                                                                  'enum': ['tick', 'n/a']},
                                                       'evidence': {'type': 'string',
                                                                    'minLength': 1},
                                                       'reason': {'type': 'string',
                                                                  'minLength': 1}},
                                        'allOf': [{'if': {'properties': {'status': {'const': 'tick'}}},
                                                   'then': {'required': ['evidence']}},
                                                  {'if': {'properties': {'status': {'const': 'n/a'}}},
                                                   'then': {'required': ['reason']}}]}},
                'ci': {'type': 'object',
                       'required': ['ran_gates', 'green'],
                       'properties': {'ran_gates': {'type': 'array',
                                                    'items': {'$ref': '#/definitions/gate'}},
                                      'green': {'type': 'boolean'},
                                      'run_url': {'type': 'string'}}},
                'tools': {'type': 'object',
                          'additionalProperties': {'type': 'string',
                                                   'not': {'const': 'postman-collection'}}}}}

OK: dict = {'change': 'F042',
 'layers_source': 'git-diff',
 'layers_touched': ['backend', 'frontend', 'user-facing-flow'],
 'required_gates': ['unit', 'api', 'playwright-happy', 'playwright-pos-neg', 'ui-audit'],
 'readiness': [{'gate': 'unit', 'status': 'tick', 'evidence': 'ci/run/8812#unit'},
               {'gate': 'api', 'status': 'tick', 'evidence': 'tests/api/test_verify.py'},
               {'gate': 'playwright-happy',
                'status': 'tick',
                'evidence': 'e2e/verify.spec.ts::happy'},
               {'gate': 'playwright-pos-neg',
                'status': 'tick',
                'evidence': 'e2e/verify.spec.ts::expired-token'},
               {'gate': 'ui-audit', 'status': 'tick', 'evidence': 'ui-ux-design.md#verify-screen'}],
 'ci': {'ran_gates': ['unit', 'api', 'playwright-happy', 'playwright-pos-neg'],
        'green': True,
        'run_url': 'ci/run/8812'},
 'tools': {'unit': 'pytest', 'api': 'pytest+httpx', 'e2e': 'playwright'}}
BAD: dict = {'change': 'F043',
 'layers_source': 'author-says',
 'layers_touched': ['backend'],
 'required_gates': ['unit', 'api'],
 'readiness': [{'gate': 'unit', 'status': 'tick'}, {'gate': 'api', 'status': 'n/a'}],
 'ci': {'ran_gates': ['unit'], 'green': False},
 'tools': {'api': 'postman-collection'}}

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
    ap = argparse.ArgumentParser(prog="validate-quality-gates.py", description=__doc__,
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
