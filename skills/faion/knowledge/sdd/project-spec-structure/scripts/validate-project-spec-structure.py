#!/usr/bin/env python3
"""validate-project-spec-structure.py

Validate the artefact produced by the project-spec-structure methodology against the JSON
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
 '$id': 'https://faion.net/schemas/project-spec-structure.json',
 'type': 'object',
 'required': ['location', 'committed', 'flat_files', 'subdirs', 'rebuild_test', 'history_in_tree'],
 'additionalProperties': False,
 'properties': {'location': {'type': 'string',
                             'pattern': '^\\.aidocs/project-spec/$|^[^~].*/project-spec/$'},
                'committed': {'type': 'boolean', 'const': True},
                'constitution_declares_path': {'type': 'boolean'},
                'flat_files': {'type': 'array',
                               'uniqueItems': True,
                               'allOf': [{'contains': {'const': 'AGENTS.md'}},
                                         {'contains': {'const': 'CLAUDE.md'}},
                                         {'contains': {'const': 'mission.md'}},
                                         {'contains': {'const': 'glossary.md'}},
                                         {'contains': {'const': 'business-rules.md'}},
                                         {'contains': {'const': 'data-model.md'}},
                                         {'contains': {'const': 'auth.md'}},
                                         {'contains': {'const': 'deploy.md'}},
                                         {'contains': {'const': 'config-secrets.md'}},
                                         {'contains': {'const': 'non-functional.md'}},
                                         {'contains': {'const': 'observability.md'}},
                                         {'contains': {'const': 'invariants.md'}}],
                               'items': {'type': 'string',
                                         'pattern': '^[a-z0-9-]+\\.md$|^AGENTS\\.md$|^CLAUDE\\.md$'}},
                'subdirs': {'type': 'array',
                            'minItems': 4,
                            'allOf': [{'contains': {'properties': {'name': {'const': 'domain'}}}},
                                      {'contains': {'properties': {'name': {'const': 'api'}}}},
                                      {'contains': {'properties': {'name': {'const': 'integrations'}}}},
                                      {'contains': {'properties': {'name': {'const': 'decisions'}}}}],
                            'items': {'type': 'object',
                                      'required': ['name', 'agents_md', 'claude_md'],
                                      'properties': {'name': {'type': 'string',
                                                              'pattern': '^[a-z0-9-]+$'},
                                                     'agents_md': {'type': 'boolean',
                                                                   'const': True},
                                                     'claude_md': {'type': 'boolean',
                                                                   'const': True}}}},
                'rebuild_test': {'type': 'object',
                                 'required': ['event', 'passed', 'assumptions'],
                                 'properties': {'event': {'type': 'string',
                                                          'enum': ['end-of-feature',
                                                                   'post-cr-bug-deploy']},
                                                'feature_or_fix': {'type': 'string',
                                                                   'pattern': '^(F|CR|BUG)[0-9]{3,}$'},
                                                'passed': {'type': 'boolean'},
                                                'assumptions': {'type': 'array',
                                                                'items': {'type': 'string'}}}},
                'history_in_tree': {'type': 'boolean', 'const': False}}}

OK: dict = {'location': '.aidocs/project-spec/',
 'committed': True,
 'flat_files': ['AGENTS.md',
                'CLAUDE.md',
                'mission.md',
                'glossary.md',
                'business-rules.md',
                'data-model.md',
                'auth.md',
                'deploy.md',
                'config-secrets.md',
                'non-functional.md',
                'observability.md',
                'invariants.md'],
 'subdirs': [{'name': 'domain', 'agents_md': True, 'claude_md': True},
             {'name': 'api', 'agents_md': True, 'claude_md': True},
             {'name': 'integrations', 'agents_md': True, 'claude_md': True},
             {'name': 'decisions', 'agents_md': True, 'claude_md': True}],
 'rebuild_test': {'event': 'end-of-feature',
                  'feature_or_fix': 'F042',
                  'passed': True,
                  'assumptions': ['retry back-off for the mail provider is exponential (documented '
                                  'in integrations/mail.md)']},
 'history_in_tree': False}
BAD: dict = {'location': '~/.faion/projects/acme/project-spec.md',
 'committed': False,
 'flat_files': ['project-spec.md'],
 'subdirs': [{'name': 'domain', 'agents_md': False, 'claude_md': False}],
 'rebuild_test': {'event': 'quarterly-cron', 'passed': True, 'assumptions': []},
 'history_in_tree': True}

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
    ap = argparse.ArgumentParser(prog="validate-project-spec-structure.py", description=__doc__,
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
