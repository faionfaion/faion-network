#!/usr/bin/env python3
"""validate-user-flows-template.py

Validate the artefact produced by the user-flows-template methodology against the JSON
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
 '$id': 'https://faion.net/schemas/sdd/user-flows.json',
 'title': 'user-flows.md (per-feature test spec)',
 'type': 'object',
 'required': ['feature_id', 'path', 'flows'],
 'additionalProperties': False,
 'properties': {'feature_id': {'type': 'string', 'pattern': '^F[0-9]{3,}$'},
                'path': {'type': 'string',
                         'pattern': '^features/in-progress/F[0-9]{3,}-[a-z0-9-]+/user-flows\\.md$'},
                'flows': {'type': 'array',
                          'minItems': 1,
                          'items': {'type': 'object',
                                    'required': ['id',
                                                 'title',
                                                 'actor',
                                                 'preconditions',
                                                 'happy_path',
                                                 'negative_paths',
                                                 'playwright_spec'],
                                    'additionalProperties': False,
                                    'properties': {'id': {'type': 'string',
                                                          'pattern': '^F-[0-9]{2,}$'},
                                                   'title': {'type': 'string', 'minLength': 1},
                                                   'actor': {'type': 'string', 'minLength': 1},
                                                   'preconditions': {'type': 'array',
                                                                     'minItems': 1,
                                                                     'items': {'type': 'string',
                                                                               'minLength': 1}},
                                                   'happy_path': {'type': 'array',
                                                                  'minItems': 1,
                                                                  'items': {'type': 'object',
                                                                            'required': ['action',
                                                                                         'expected'],
                                                                            'properties': {'action': {'type': 'string',
                                                                                                      'minLength': 1},
                                                                                           'expected': {'type': 'string',
                                                                                                        'minLength': 1}}}},
                                                   'negative_paths': {'type': 'array',
                                                                      'minItems': 1,
                                                                      'items': {'type': 'object',
                                                                                'required': ['name',
                                                                                             'trigger',
                                                                                             'expected_ux'],
                                                                                'properties': {'name': {'type': 'string',
                                                                                                        'minLength': 1},
                                                                                               'trigger': {'type': 'string',
                                                                                                           'minLength': 1},
                                                                                               'expected_ux': {'type': 'string',
                                                                                                               'minLength': 1}}}},
                                                   'playwright_spec': {'type': 'string',
                                                                       'pattern': '\\.spec\\.[jt]s$'}}}}}}

OK: dict = {'feature_id': 'F021',
 'path': 'features/in-progress/F021-upgrade-page/user-flows.md',
 'flows': [{'id': 'F-01',
            'title': 'Signed-in user upgrades to solo tier',
            'actor': 'signed-in free-tier user with verified email',
            'preconditions': ['account exists',
                              'Stripe customer record exists',
                              'no active subscription'],
            'happy_path': [{'action': 'Click "Upgrade" in nav', 'expected': 'routed to /upgrade'},
                           {'action': 'Select "Solo $19/mo"',
                            'expected': 'Stripe Elements form appears'},
                           {'action': 'Enter test card 4242 4242 4242 4242, submit',
                            'expected': 'request sent'},
                           {'action': 'Wait for response',
                            'expected': '200 redirect to /account?upgraded=solo; success toast; '
                                        'tier=solo in /api/account'}],
            'negative_paths': [{'name': 'Card declined (test card 4000 0000 0000 0002)',
                                'trigger': 'submit declined card',
                                'expected_ux': 'inline error under card field "Your card was '
                                               'declined.", form stays editable, no charge '
                                               'created'},
                               {'name': 'Network drop mid-submit',
                                'trigger': 'throttle network to offline after click submit',
                                'expected_ux': 'spinner times out at 30s, toast "Connection lost. '
                                               'Try again." NO partial subscription'}],
            'playwright_spec': 'faion-net-e2e/tests/upgrade.spec.ts'}]}
BAD: dict = {'feature_id': 'F021',
 'path': 'features/in-progress/F021-upgrade-page/user-flows.md',
 'flows': [{'id': 'F-01',
            'title': 'Upgrade',
            'actor': 'user',
            'preconditions': [],
            'happy_path': [{'action': 'Click Upgrade'}, {'action': 'Pay'}, {'action': 'Done'}],
            'negative_paths': []}]}

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
    ap = argparse.ArgumentParser(prog="validate-user-flows-template.py", description=__doc__,
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
