#!/usr/bin/env python3
"""validate-llm-friendly-architecture.py

Validate an LLM-friendly architecture audit record against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the llm-friendly-architecture methodology, plus the
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
 '$id': 'https://faion.net/schemas/llm-friendly-architecture.json',
 'title': 'LLM-friendly architecture audit record',
 'type': 'object',
 'required': ['repo', 'owner', 'inputs', 'audit', 'decision', 'evidence', 'review'],
 'additionalProperties': False,
 'definitions': {'path': {'type': 'string', 'minLength': 3, 'pattern': '^[^\\s]+$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}},
 'properties': {'__faion_header__': {'type': 'object'},
                'repo': {'type': 'object',
                         'required': ['url', 'commit_sha', 'source_root'],
                         'additionalProperties': False,
                         'properties': {'url': {'type': 'string', 'pattern': '^(https://|git@)'},
                                        'commit_sha': {'type': 'string',
                                                       'pattern': '^[0-9a-f]{7,40}$'},
                                        'source_root': {'$ref': '#/definitions/path'}}},
                'owner': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                'inputs': {'type': 'array',
                           'minItems': 1,
                           'contains': {'properties': {'name': {'const': 'line_limit'}}},
                           'items': {'type': 'object',
                                     'required': ['name', 'value'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'type': 'string',
                                                             'enum': ['line_limit',
                                                                      'namespace_import_allowlist']},
                                                    'value': {}},
                                     'allOf': [{'if': {'properties': {'name': {'const': 'line_limit'}}},
                                                'then': {'properties': {'value': {'type': 'integer',
                                                                                  'minimum': 100,
                                                                                  'maximum': 300,
                                                                                  'default': 250}}}},
                                               {'if': {'properties': {'name': {'const': 'namespace_import_allowlist'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'items': {'type': 'string',
                                                                                            'minLength': 1}}}}}]}},
                'audit': {'type': 'object',
                          'required': ['command',
                                       'file_size',
                                       'directory_depth',
                                       'barrels',
                                       'wildcard_imports',
                                       'naming',
                                       'inline_data',
                                       'claude_md',
                                       'ci_wired'],
                          'additionalProperties': False,
                          'properties': {'command': {'type': 'string',
                                                     'minLength': 8,
                                                     'pattern': 'audit'},
                                         'file_size': {'type': 'object',
                                                       'required': ['histogram', 'oversized'],
                                                       'additionalProperties': False,
                                                       'properties': {'histogram': {'type': 'array',
                                                                                    'minItems': 2,
                                                                                    'items': {'type': 'object',
                                                                                              'required': ['bucket',
                                                                                                           'files'],
                                                                                              'additionalProperties': False,
                                                                                              'properties': {'bucket': {'type': 'string',
                                                                                                                        'pattern': '^[0-9]+(-[0-9]+|\\+)$'},
                                                                                                             'files': {'type': 'integer',
                                                                                                                       'minimum': 0}}}},
                                                                      'oversized': {'type': 'array',
                                                                                    'items': {'type': 'object',
                                                                                              'required': ['path',
                                                                                                           'lines',
                                                                                                           'proposed_split'],
                                                                                              'additionalProperties': False,
                                                                                              'properties': {'path': {'$ref': '#/definitions/path'},
                                                                                                             'lines': {'type': 'integer',
                                                                                                                       'minimum': 101},
                                                                                                             'proposed_split': {'type': 'string',
                                                                                                                                'minLength': 12,
                                                                                                                                'pattern': '/'}}}}}},
                                         'directory_depth': {'type': 'object',
                                                             'required': ['limit',
                                                                          'feature_limit',
                                                                          'violations'],
                                                             'additionalProperties': False,
                                                             'properties': {'limit': {'type': 'integer',
                                                                                      'const': 3},
                                                                            'feature_limit': {'type': 'integer',
                                                                                              'const': 2},
                                                                            'violations': {'type': 'array',
                                                                                           'items': {'type': 'object',
                                                                                                     'required': ['path',
                                                                                                                  'depth'],
                                                                                                     'additionalProperties': False,
                                                                                                     'properties': {'path': {'$ref': '#/definitions/path'},
                                                                                                                    'depth': {'type': 'integer',
                                                                                                                              'minimum': 4}}}}}},
                                         'barrels': {'type': 'array',
                                                     'items': {'$ref': '#/definitions/path'}},
                                         'wildcard_imports': {'type': 'object',
                                                              'required': ['lint', 'hits'],
                                                              'additionalProperties': False,
                                                              'properties': {'lint': {'type': 'string',
                                                                                      'enum': ['ruff '
                                                                                               'F403/F405',
                                                                                               'eslint '
                                                                                               'import/no-namespace',
                                                                                               'eslint '
                                                                                               'no-restricted-syntax',
                                                                                               'biome '
                                                                                               'noNamespaceImport']},
                                                                             'hits': {'type': 'array',
                                                                                      'items': {'type': 'object',
                                                                                                'required': ['path',
                                                                                                             'line'],
                                                                                                'additionalProperties': False,
                                                                                                'properties': {'path': {'$ref': '#/definitions/path'},
                                                                                                               'line': {'type': 'integer',
                                                                                                                        'minimum': 1}}}}}},
                                         'naming': {'type': 'object',
                                                    'required': ['rubric', 'score', 'offenders'],
                                                    'additionalProperties': False,
                                                    'properties': {'rubric': {'type': 'array',
                                                                              'minItems': 4,
                                                                              'items': {'type': 'string',
                                                                                        'minLength': 8}},
                                                                   'score': {'type': 'integer',
                                                                             'minimum': 0,
                                                                             'maximum': 100},
                                                                   'offenders': {'type': 'array',
                                                                                 'items': {'type': 'object',
                                                                                           'required': ['path',
                                                                                                        'reason',
                                                                                                        'proposed_name'],
                                                                                           'additionalProperties': False,
                                                                                           'properties': {'path': {'$ref': '#/definitions/path'},
                                                                                                          'reason': {'type': 'string',
                                                                                                                     'minLength': 8},
                                                                                                          'proposed_name': {'$ref': '#/definitions/path'}}}}},
                                                    'if': {'properties': {'score': {'maximum': 99}}},
                                                    'then': {'properties': {'offenders': {'minItems': 1}}}},
                                         'inline_data': {'type': 'array',
                                                         'items': {'type': 'object',
                                                                   'required': ['path', 'lines'],
                                                                   'additionalProperties': False,
                                                                   'properties': {'path': {'$ref': '#/definitions/path'},
                                                                                  'lines': {'type': 'integer',
                                                                                            'minimum': 1}}}},
                                         'claude_md': {'type': 'object',
                                                       'required': ['present', 'line_limit'],
                                                       'additionalProperties': False,
                                                       'properties': {'present': {'type': 'boolean',
                                                                                  'const': True},
                                                                      'line_limit': {'type': 'integer',
                                                                                     'minimum': 100,
                                                                                     'maximum': 300}}},
                                         'ci_wired': {'type': 'boolean'}}},
                'decision': {'type': 'string',
                             'minLength': 20,
                             'pattern': '(\\.(tsx?|jsx?|py|md)\\b|/)'},
                'evidence': {'type': 'array',
                             'minItems': 2,
                             'items': {'type': 'string', 'minLength': 7},
                             'allOf': [{'contains': {'pattern': 'audit'}},
                                       {'contains': {'pattern': '\\b[0-9a-f]{7,40}\\b'}}]},
                'review': {'type': 'object',
                           'required': ['cadence', 'next_review_at'],
                           'additionalProperties': False,
                           'properties': {'cadence': {'type': 'string',
                                                      'enum': ['monthly', 'quarterly']},
                                          'next_review_at': {'$ref': '#/definitions/date'}}}}}

OK = {'repo': {'url': 'https://github.com/acme/storefront',
          'commit_sha': 'a1b2c3d4e5f',
          'source_root': 'src'},
 'owner': 'swe:alice',
 'inputs': [{'name': 'line_limit', 'value': 250},
            {'name': 'namespace_import_allowlist', 'value': ['react', 'three']}],
 'audit': {'command': 'bash scripts/llm-arch-audit.sh src 250',
           'file_size': {'histogram': [{'bucket': '0-100', 'files': 212},
                                       {'bucket': '101-250', 'files': 61},
                                       {'bucket': '251-500', 'files': 4},
                                       {'bucket': '501+', 'files': 1}],
                         'oversized': [{'path': 'src/features/checkout/CheckoutPage.tsx',
                                        'lines': 1412,
                                        'proposed_split': 'menu and copy arrays to '
                                                          'src/data/checkout.ts; useCheckoutTotals '
                                                          'to src/hooks/use-checkout-totals.ts; '
                                                          'AddressForm to '
                                                          'src/features/checkout/AddressForm.tsx'},
                                       {'path': 'src/components/ProductCard.tsx',
                                        'lines': 388,
                                        'proposed_split': 'price formatting to '
                                                          'src/utils/format-price.ts; badges to '
                                                          'src/components/ProductBadges.tsx'},
                                       {'path': 'src/utils/helpers.ts',
                                        'lines': 302,
                                        'proposed_split': 'one function per file under src/utils/: '
                                                          'format-date.ts, slugify.ts, '
                                                          'debounce.ts'}]},
           'directory_depth': {'limit': 3,
                               'feature_limit': 2,
                               'violations': [{'path': 'src/features/billing/invoices/pdf/renderers/table.ts',
                                               'depth': 5}]},
           'barrels': ['src/components/index.ts'],
           'wildcard_imports': {'lint': 'eslint import/no-namespace',
                                'hits': [{'path': 'src/features/search/SearchPanel.tsx',
                                          'line': 3}]},
           'naming': {'rubric': ['file name equals its primary export',
                                 'components PascalCase, hooks use-*.ts, utils kebab-case',
                                 'no catch-all names: utils2, misc, helpers, common, stuff',
                                 'no unexplained abbreviations'],
                      'score': 84,
                      'offenders': [{'path': 'src/utils/helpers.ts',
                                     'reason': 'catch-all name',
                                     'proposed_name': 'src/utils/format-date.ts'},
                                    {'path': 'src/components/misc/Btn.tsx',
                                     'reason': 'catch-all directory and abbreviation',
                                     'proposed_name': 'src/components/Button.tsx'}]},
           'inline_data': [{'path': 'src/features/checkout/CheckoutPage.tsx', 'lines': 214}],
           'claude_md': {'present': True, 'line_limit': 250},
           'ci_wired': False},
 'decision': 'Delete src/components/index.ts and rewrite its 14 importers; split CheckoutPage.tsx '
             'into src/data/checkout.ts, use-checkout-totals.ts and AddressForm.tsx; split '
             'ProductCard.tsx and helpers.ts as proposed; flatten billing/invoices/pdf/renderers '
             'into src/features/billing-invoice-pdf/; replace the namespace import in '
             'SearchPanel.tsx; rename misc/Btn.tsx to Button.tsx; then wire the audit into CI.',
 'evidence': ['bash scripts/llm-arch-audit.sh src 250',
              'a1b2c3d4e5f',
              'https://github.com/acme/storefront/pull/2210'],
 'review': {'cadence': 'quarterly', 'next_review_at': '2026-12-12'}}

BAD = {'repo': {'url': 'https://github.com/acme/storefront',
          'commit_sha': 'a1b2c3d4e5f',
          'source_root': 'src'},
 'owner': 'swe:alice',
 'inputs': [{'name': 'line_limit', 'value': 400}],
 'audit': {'command': 'bash scripts/llm-arch-audit.sh src 400',
           'file_size': {'histogram': [{'bucket': '0-400', 'files': 274},
                                       {'bucket': '401+', 'files': 4}],
                         'oversized': [{'path': 'src/features/checkout/CheckoutPage.tsx',
                                        'lines': 1412,
                                        'proposed_split': 'split later'}]},
           'directory_depth': {'limit': 3, 'feature_limit': 2, 'violations': []},
           'barrels': ['src/components/index.ts'],
           'wildcard_imports': {'lint': 'eslint import/no-namespace', 'hits': []},
           'naming': {'rubric': ['file name equals its primary export',
                                 'components PascalCase, hooks use-*.ts, utils kebab-case',
                                 'no catch-all names: utils2, misc, helpers, common, stuff',
                                 'no unexplained abbreviations'],
                      'score': 71,
                      'offenders': []},
           'inline_data': [],
           'claude_md': {'present': True, 'line_limit': 250},
           'ci_wired': False},
 'decision': 'Reduce file sizes across the codebase and improve naming over the next quarter.',
 'evidence': ['https://github.com/acme/storefront/pull/2210'],
 'review': {'cadence': 'quarterly', 'next_review_at': '2026-12-12'}}


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
    limit = inputs.get("line_limit", 250)
    audit = obj.get("audit") or {}
    over = (audit.get("file_size") or {}).get("oversized") or []
    for i, f in enumerate(over):
        if f.get("lines", 0) <= limit:
            errs.append(f"audit.file_size.oversized[{i}]: {f.get('lines')} lines is not above line_limit {limit} (r-file-size-histogram-with-threshold)")
        if re.search(r"(2|-part\d*)\.(tsx?|jsx?|py)\b", f.get("proposed_split", "")):
            errs.append(f"audit.file_size.oversized[{i}]: proposed_split is a cosmetic Foo2 / -part split (fm-01)")
    lines = [f.get("lines", 0) for f in over]
    if lines != sorted(lines, reverse=True):
        errs.append("audit.file_size.oversized: not sorted by lines descending (r-file-size-histogram-with-threshold)")
    cm = audit.get("claude_md") or {}
    if cm.get("line_limit") != limit:
        errs.append(f"audit.claude_md.line_limit {cm.get('line_limit')} differs from line_limit input {limit} (r-claude-md-matches-audit)")
    findings = (len(over) + len((audit.get("directory_depth") or {}).get("violations") or [])
                + len(audit.get("barrels") or []) + len((audit.get("wildcard_imports") or {}).get("hits") or [])
                + len((audit.get("naming") or {}).get("offenders") or []) + len(audit.get("inline_data") or []))
    if findings == 0 and audit.get("ci_wired") is not True:
        errs.append("audit: baseline is clean but ci_wired is false (r-audit-is-reproducible-command)")
    decision = obj.get("decision", "")
    for b in audit.get("barrels") or []:
        if b.split("/")[-1] not in decision and b not in decision:
            errs.append(f"decision does not name barrel {b} for deletion (fm-02)")
    for v in (audit.get("directory_depth") or {}).get("violations") or []:
        parts = v.get("path", "").split("/")
        if not any(p and p in decision for p in parts[1:-1]):
            errs.append(f"decision does not name the deep path {v.get('path')} (fm-03)")
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
        prog="validate-llm-friendly-architecture.py",
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
