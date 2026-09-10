#!/usr/bin/env python3
"""validate-ui-ux-design-template.py

Validate the artefact produced by the ui-ux-design-template methodology against the JSON
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
 '$id': 'https://faion.net/schemas/sdd/ui-ux-design.json',
 'title': 'ui-ux-design.md (per-feature design doc)',
 'type': 'object',
 'required': ['feature_id',
              'path',
              'intent',
              'layout',
              'states',
              'nielsen_audit',
              'norman_audit',
              'copy'],
 'additionalProperties': False,
 'definitions': {'audit_row': {'type': 'object',
                               'required': ['finding', 'fix_or_ok'],
                               'properties': {'finding': {'type': 'string', 'minLength': 1},
                                              'fix_or_ok': {'type': 'string', 'minLength': 1}}}},
 'properties': {'feature_id': {'type': 'string', 'pattern': '^F[0-9]{3,}$'},
                'path': {'type': 'string',
                         'pattern': '^features/in-progress/F[0-9]{3,}-[a-z0-9-]+/ui-ux-design\\.md$'},
                'intent': {'type': 'string', 'minLength': 1},
                'layout': {'type': 'string', 'minLength': 1},
                'states': {'type': 'object',
                           'required': ['empty', 'loading', 'error', 'success', 'disabled'],
                           'additionalProperties': False,
                           'properties': {'empty': {'type': 'string', 'minLength': 1},
                                          'loading': {'type': 'string', 'minLength': 1},
                                          'error': {'type': 'string', 'minLength': 1},
                                          'success': {'type': 'string', 'minLength': 1},
                                          'disabled': {'type': 'string', 'minLength': 1}}},
                'nielsen_audit': {'type': 'array',
                                  'minItems': 5,
                                  'maxItems': 5,
                                  'uniqueItems': True,
                                  'items': {'allOf': [{'$ref': '#/definitions/audit_row'},
                                                      {'required': ['heuristic'],
                                                       'properties': {'heuristic': {'type': 'string',
                                                                                    'enum': ['N1',
                                                                                             'N3',
                                                                                             'N4',
                                                                                             'N5',
                                                                                             'N6']}}}]}},
                'norman_audit': {'type': 'array',
                                 'minItems': 2,
                                 'maxItems': 2,
                                 'uniqueItems': True,
                                 'items': {'allOf': [{'$ref': '#/definitions/audit_row'},
                                                     {'required': ['principle'],
                                                      'properties': {'principle': {'type': 'string',
                                                                                   'enum': ['affordance',
                                                                                            'feedback']}}}]}},
                'copy': {'type': 'object',
                         'required': ['primary_button',
                                      'empty_state',
                                      'error_message',
                                      'success_message'],
                         'properties': {'primary_button': {'type': 'string', 'minLength': 1},
                                        'secondary_button': {'type': 'string'},
                                        'empty_state': {'type': 'string', 'minLength': 1},
                                        'error_message': {'type': 'string', 'minLength': 1},
                                        'success_message': {'type': 'string', 'minLength': 1}}}}}

OK: dict = {'feature_id': 'F021',
 'path': 'features/in-progress/F021-upgrade-page/ui-ux-design.md',
 'intent': 'A signed-in free-tier user upgrades to the solo tier without leaving the account area.',
 'layout': 'Plan cards in a single row above a Stripe Elements form; primary button below the '
           "form, secondary 'Back to account' link under it.",
 'states': {'empty': 'No plan selected: cards shown, form hidden, primary button disabled with '
                     "tooltip 'Pick a plan'.",
            'loading': 'After submit: button disabled with spinner, form fields read-only.',
            'error': 'Inline error under the card field; form stays editable; no charge created.',
            'success': 'Redirect to /account?upgraded=solo with success toast.',
            'disabled': "Card already on file and subscription active: cards greyed out, note 'You "
                        "are already on solo'."},
 'nielsen_audit': [{'heuristic': 'N1',
                    'finding': 'Spinner and read-only fields show the submit is in flight.',
                    'fix_or_ok': 'noted OK'},
                   {'heuristic': 'N3',
                    'finding': 'No way to cancel once submit was clicked.',
                    'fix_or_ok': "add 30s timeout with 'Connection lost. Try again.' toast"},
                   {'heuristic': 'N4',
                    'finding': "'Upgrade' in nav vs 'Choose plan' on the button.",
                    'fix_or_ok': "rename button to 'Upgrade to Solo'"},
                   {'heuristic': 'N5',
                    'finding': 'Card number accepts letters until submit.',
                    'fix_or_ok': 'Stripe Elements input mask'},
                   {'heuristic': 'N6',
                    'finding': 'Selected plan name repeated above the form.',
                    'fix_or_ok': 'noted OK'}],
 'norman_audit': [{'principle': 'affordance',
                   'finding': 'Plan cards are clickable but only the radio is styled.',
                   'fix_or_ok': 'hover + cursor:pointer on the whole card'},
                  {'principle': 'feedback',
                   'finding': 'Submit disables the button and shows a spinner immediately.',
                   'fix_or_ok': 'noted OK'}],
 'copy': {'primary_button': 'Upgrade to Solo',
          'secondary_button': 'Back to account',
          'empty_state': 'Pick a plan to continue.',
          'error_message': 'Your card was declined.',
          'success_message': 'You are on Solo now.'}}
BAD: dict = {'feature_id': 'F021',
 'path': 'features/in-progress/F021-upgrade-page/ui-ux-design.md',
 'intent': 'Upgrade page.',
 'states': {'success': 'Redirect to /account?upgraded=solo.'},
 'nielsen_audit': [{'heuristic': 'N1', 'finding': 'ok', 'fix_or_ok': 'ok'},
                   {'heuristic': 'N2', 'finding': 'ok', 'fix_or_ok': 'ok'},
                   {'heuristic': 'N7', 'finding': 'ok', 'fix_or_ok': 'ok'}],
 'norman_audit': [],
 'copy': {}}

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
    ap = argparse.ArgumentParser(prog="validate-ui-ux-design-template.py", description=__doc__,
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
