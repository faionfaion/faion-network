#!/usr/bin/env python3
"""validate-new-dependency-risk-checklist.py

Validate a new-dependency risk record against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the new-dependency-risk-checklist methodology, plus the
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
 '$id': 'https://faion.net/schemas/new-dependency-risk-checklist.json',
 'title': 'New dependency risk record',
 'type': 'object',
 'required': ['package',
              'owner',
              'inputs',
              'advisory_lookup',
              'lockfile',
              'decision',
              'evidence',
              'alert_routing',
              'review'],
 'additionalProperties': False,
 'definitions': {'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'url': {'type': 'string', 'pattern': '^https://'},
                 'window': {'type': 'string', 'pattern': '^[0-9]+d$'}},
 'properties': {'__faion_header__': {'type': 'object'},
                'package': {'type': 'object',
                            'required': ['name',
                                         'version',
                                         'ecosystem',
                                         'registry_repository_url',
                                         'readme_repository_url',
                                         'repository_matches',
                                         'near_name',
                                         'install_scripts'],
                            'additionalProperties': False,
                            'properties': {'name': {'type': 'string',
                                                    'minLength': 1,
                                                    'pattern': '^[^\\s]+$'},
                                           'version': {'type': 'string',
                                                       'pattern': '^[0-9]+\\.[0-9]+(\\.[0-9]+)?([-+][0-9A-Za-z.-]+)?$'},
                                           'ecosystem': {'type': 'string',
                                                         'enum': ['npm',
                                                                  'pypi',
                                                                  'crates.io',
                                                                  'go',
                                                                  'maven',
                                                                  'rubygems',
                                                                  'nuget']},
                                           'registry_repository_url': {'$ref': '#/definitions/url'},
                                           'readme_repository_url': {'$ref': '#/definitions/url'},
                                           'repository_matches': {'type': 'boolean'},
                                           'near_name': {'type': 'object',
                                                         'required': ['searched',
                                                                      'popular_near_name'],
                                                         'additionalProperties': False,
                                                         'properties': {'searched': {'type': 'boolean',
                                                                                     'const': True},
                                                                        'popular_near_name': {'type': ['string',
                                                                                                       'null']}}},
                                           'install_scripts': {'type': 'object',
                                                               'required': ['declared', 'hooks'],
                                                               'additionalProperties': False,
                                                               'properties': {'declared': {'type': 'boolean'},
                                                                              'hooks': {'type': 'array',
                                                                                        'items': {'type': 'object',
                                                                                                  'required': ['hook',
                                                                                                               'runs'],
                                                                                                  'additionalProperties': False,
                                                                                                  'properties': {'hook': {'type': 'string',
                                                                                                                          'enum': ['preinstall',
                                                                                                                                   'install',
                                                                                                                                   'postinstall']},
                                                                                                                 'runs': {'type': 'string',
                                                                                                                          'minLength': 2}}}}},
                                                               'if': {'properties': {'declared': {'const': True}}},
                                                               'then': {'properties': {'hooks': {'minItems': 1}}}}}},
                'owner': {'$ref': '#/definitions/handle'},
                'inputs': {'type': 'array',
                           'minItems': 6,
                           'allOf': [{'contains': {'properties': {'name': {'const': 'licence'}}}},
                                     {'contains': {'properties': {'name': {'const': 'transitive_count'}}}},
                                     {'contains': {'properties': {'name': {'const': 'maintainers'}}}},
                                     {'contains': {'properties': {'name': {'const': 'last_release'}}}},
                                     {'contains': {'properties': {'name': {'const': 'alternative'}}}},
                                     {'contains': {'properties': {'name': {'const': 'patch_window'}}}}],
                           'items': {'type': 'object',
                                     'required': ['name', 'value'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'type': 'string',
                                                             'enum': ['licence',
                                                                      'transitive_count',
                                                                      'maintainers',
                                                                      'last_release',
                                                                      'alternative',
                                                                      'patch_window',
                                                                      'useful_surface_lines',
                                                                      'distribution_model']},
                                                    'value': {}},
                                     'allOf': [{'if': {'properties': {'name': {'const': 'licence'}}},
                                                'then': {'properties': {'value': {'type': 'string',
                                                                                  'minLength': 3,
                                                                                  'pattern': '^(?![Uu]nknown|[Ss]ee '
                                                                                             'repo|MIT-ish)[A-Za-z0-9.+-]+( '
                                                                                             '(WITH|OR|AND) '
                                                                                             '[A-Za-z0-9.+-]+)*$'}}}},
                                               {'if': {'properties': {'name': {'const': 'transitive_count'}}},
                                                'then': {'properties': {'value': {'type': 'integer',
                                                                                  'minimum': 0}}}},
                                               {'if': {'properties': {'name': {'const': 'maintainers'}}},
                                                'then': {'properties': {'value': {'type': 'integer',
                                                                                  'minimum': 1}}}},
                                               {'if': {'properties': {'name': {'const': 'last_release'}}},
                                                'then': {'properties': {'value': {'$ref': '#/definitions/date'}}}},
                                               {'if': {'properties': {'name': {'const': 'alternative'}}},
                                                'then': {'properties': {'value': {'type': 'array',
                                                                                  'minItems': 1,
                                                                                  'items': {'type': 'object',
                                                                                            'required': ['name',
                                                                                                         'reason'],
                                                                                            'additionalProperties': False,
                                                                                            'properties': {'name': {'type': 'string',
                                                                                                                    'minLength': 2},
                                                                                                           'reason': {'type': 'string',
                                                                                                                      'minLength': 8}}},
                                                                                  'contains': {'properties': {'name': {'enum': ['in-house',
                                                                                                                                'already-in-tree']}}}}}}},
                                               {'if': {'properties': {'name': {'const': 'patch_window'}}},
                                                'then': {'properties': {'value': {'type': 'object',
                                                                                  'required': ['critical',
                                                                                               'high'],
                                                                                  'additionalProperties': False,
                                                                                  'properties': {'critical': {'$ref': '#/definitions/window'},
                                                                                                 'high': {'$ref': '#/definitions/window'}}}}}},
                                               {'if': {'properties': {'name': {'const': 'useful_surface_lines'}}},
                                                'then': {'properties': {'value': {'type': 'integer',
                                                                                  'minimum': 1}}}},
                                               {'if': {'properties': {'name': {'const': 'distribution_model'}}},
                                                'then': {'properties': {'value': {'type': 'string',
                                                                                  'enum': ['saas-backend',
                                                                                           'shipped-binary',
                                                                                           'browser-bundle',
                                                                                           'internal-tool']}}}}]}},
                'advisory_lookup': {'type': 'object',
                                    'required': ['source', 'url', 'checked_on', 'open_advisories'],
                                    'additionalProperties': False,
                                    'properties': {'source': {'type': 'string',
                                                              'enum': ['osv.dev',
                                                                       'github-advisory-database',
                                                                       'nvd']},
                                                   'url': {'$ref': '#/definitions/url'},
                                                   'checked_on': {'$ref': '#/definitions/date'},
                                                   'open_advisories': {'type': 'array',
                                                                       'items': {'type': 'string',
                                                                                 'pattern': '^(CVE-[0-9]{4}-[0-9]{4,}|GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4})$'}}}},
                'lockfile': {'type': 'object',
                             'required': ['file', 'commit_url'],
                             'additionalProperties': False,
                             'properties': {'file': {'type': 'string',
                                                     'enum': ['package-lock.json',
                                                              'yarn.lock',
                                                              'pnpm-lock.yaml',
                                                              'poetry.lock',
                                                              'uv.lock',
                                                              'requirements.txt (hashed)',
                                                              'Cargo.lock',
                                                              'go.sum',
                                                              'Gemfile.lock',
                                                              'packages.lock.json']},
                                            'commit_url': {'$ref': '#/definitions/url'}}},
                'decision': {'type': 'object',
                             'required': ['verdict', 'statement'],
                             'additionalProperties': False,
                             'properties': {'verdict': {'type': 'string',
                                                        'enum': ['accept',
                                                                 'accept-with-mitigation',
                                                                 'reject',
                                                                 'in-house']},
                                            'statement': {'type': 'string',
                                                          'minLength': 20,
                                                          'pattern': '@[0-9]+\\.[0-9]+'},
                                            'fallback': {'type': 'object',
                                                         'required': ['kind', 'target'],
                                                         'additionalProperties': False,
                                                         'properties': {'kind': {'type': 'string',
                                                                                 'enum': ['vendor',
                                                                                          'fork',
                                                                                          'alternative']},
                                                                        'target': {'type': 'string',
                                                                                   'minLength': 2}}},
                                            'mitigation': {'type': 'object',
                                                           'required': ['advisory_id', 'action'],
                                                           'additionalProperties': False,
                                                           'properties': {'advisory_id': {'type': 'string',
                                                                                          'pattern': '^(CVE-[0-9]{4}-[0-9]{4,}|GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4})$'},
                                                                          'action': {'type': 'string',
                                                                                     'minLength': 8}}},
                                            'distribution_model': {'type': 'string',
                                                                   'enum': ['saas-backend',
                                                                            'shipped-binary',
                                                                            'browser-bundle',
                                                                            'internal-tool']},
                                            'override_reason': {'type': 'string', 'minLength': 12},
                                            'install_hook_reason': {'type': 'string',
                                                                    'minLength': 12}},
                             'if': {'properties': {'verdict': {'const': 'accept-with-mitigation'}}},
                             'then': {'required': ['mitigation']}},
                'evidence': {'type': 'array',
                             'minItems': 2,
                             'items': {'$ref': '#/definitions/url'},
                             'allOf': [{'contains': {'pattern': 'osv\\.dev|github\\.com/advisories|nvd\\.nist\\.gov'}},
                                       {'contains': {'pattern': '/commit/|/pull/|/merge_requests/'}}]},
                'alert_routing': {'type': 'object',
                                  'required': ['tool', 'recipient'],
                                  'additionalProperties': False,
                                  'properties': {'tool': {'type': 'string',
                                                          'enum': ['dependabot',
                                                                   'renovate',
                                                                   'npm-audit',
                                                                   'pip-audit',
                                                                   'cargo-audit',
                                                                   'govulncheck']},
                                                 'recipient': {'$ref': '#/definitions/handle'}}},
                'review': {'type': 'object',
                           'required': ['reopen_on', 'next_review_at'],
                           'additionalProperties': False,
                           'properties': {'reopen_on': {'type': 'string',
                                                        'const': 'major-version-bump'},
                                          'next_review_at': {'$ref': '#/definitions/date'}}}}}

OK = {'package': {'name': 'dayjs',
             'version': '1.11.10',
             'ecosystem': 'npm',
             'registry_repository_url': 'https://github.com/iamkun/dayjs',
             'readme_repository_url': 'https://github.com/iamkun/dayjs',
             'repository_matches': True,
             'near_name': {'searched': True, 'popular_near_name': None},
             'install_scripts': {'declared': False, 'hooks': []}},
 'owner': 'swe:alice',
 'inputs': [{'name': 'licence', 'value': 'MIT'},
            {'name': 'transitive_count', 'value': 0},
            {'name': 'maintainers', 'value': 3},
            {'name': 'last_release', 'value': '2026-07-18'},
            {'name': 'alternative',
             'value': [{'name': 'in-house',
                        'reason': 'locale tables and DST handling are far more than twenty lines'},
                       {'name': 'already-in-tree',
                        'reason': 'no date library in the lockfile; Intl.DateTimeFormat lacks '
                                  'parsing'},
                       {'name': 'date-fns',
                        'reason': 'tree-shakeable but 3x the bundle for the four functions we '
                                  'need'}]},
            {'name': 'patch_window', 'value': {'critical': '7d', 'high': '30d'}},
            {'name': 'useful_surface_lines', 'value': 400},
            {'name': 'distribution_model', 'value': 'browser-bundle'}],
 'advisory_lookup': {'source': 'osv.dev',
                     'url': 'https://osv.dev/list?ecosystem=npm&q=dayjs%401.11.10',
                     'checked_on': '2026-09-10',
                     'open_advisories': []},
 'lockfile': {'file': 'pnpm-lock.yaml',
              'commit_url': 'https://github.com/acme/storefront/pull/2231/commits/9f3c1e2'},
 'decision': {'verdict': 'accept',
              'statement': 'Accept dayjs@1.11.10 as a direct dependency of the storefront browser '
                           'bundle; MIT; no transitive additions; three maintainers with a release '
                           'two months ago.'},
 'evidence': ['https://osv.dev/list?ecosystem=npm&q=dayjs%401.11.10',
              'https://github.com/acme/storefront/pull/2231/commits/9f3c1e2',
              'https://www.npmjs.com/package/dayjs'],
 'alert_routing': {'tool': 'renovate', 'recipient': 'swe:alice'},
 'review': {'reopen_on': 'major-version-bump', 'next_review_at': '2027-03-10'}}

BAD = {'package': {'name': 'crossenv',
             'version': '^6.1.1',
             'ecosystem': 'npm',
             'registry_repository_url': 'https://github.com/kentcdodds/cross-env',
             'readme_repository_url': 'https://github.com/kentcdodds/cross-env',
             'repository_matches': False,
             'near_name': {'searched': True, 'popular_near_name': 'cross-env'},
             'install_scripts': {'declared': True,
                                 'hooks': [{'hook': 'postinstall',
                                            'runs': 'node package-setup.js (posts process.env to a '
                                                    'remote host)'}]}},
 'owner': 'swe:bob',
 'inputs': [{'name': 'licence', 'value': 'MIT-ish'},
            {'name': 'transitive_count', 'value': 0},
            {'name': 'maintainers', 'value': 1},
            {'name': 'last_release', 'value': '2024-06-01'},
            {'name': 'alternative',
             'value': [{'name': 'dotenv',
                        'reason': 'different purpose, does not set env for a child process'}]},
            {'name': 'patch_window', 'value': {'critical': '7d', 'high': '30d'}}],
 'advisory_lookup': {'source': 'osv.dev',
                     'url': 'https://osv.dev/list?ecosystem=npm&q=crossenv',
                     'checked_on': '2026-09-10',
                     'open_advisories': ['GHSA-6h6q-4wq8-7w5g']},
 'lockfile': {'file': 'package-lock.json',
              'commit_url': 'https://github.com/acme/storefront/pull/2232'},
 'decision': {'verdict': 'accept',
              'statement': 'Accept crossenv for cross-platform env vars in npm scripts.'},
 'evidence': ['https://osv.dev/list?ecosystem=npm&q=crossenv',
              'https://github.com/acme/storefront/pull/2232'],
 'alert_routing': {'tool': 'dependabot', 'recipient': 'team:platform'},
 'review': {'reopen_on': 'major-version-bump', 'next_review_at': '2027-03-10'}}


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


from datetime import date

_COPYLEFT = re.compile(r"^(GPL|AGPL|LGPL|SSPL|BUSL)", re.I)
_REMOTE = re.compile(r"curl|wget|https?://|remote|download|posts .* to", re.I)


def _d(s: str):
    try:
        return date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    inputs = {i.get("name"): i.get("value") for i in obj.get("inputs") or [] if isinstance(i, dict)}
    pkg, dec = obj.get("package") or {}, obj.get("decision") or {}
    verdict = dec.get("verdict")
    if _COPYLEFT.match(str(inputs.get("licence", ""))) and not dec.get("distribution_model"):
        errs.append("licence is copyleft or source-available and decision.distribution_model is missing (r-licence-spdx-recorded)")
    checked = _d((obj.get("advisory_lookup") or {}).get("checked_on", "")) or date.today()
    last = _d(str(inputs.get("last_release", "")))
    stale = last is not None and (checked - last).days > 365
    if (inputs.get("maintainers") == 1 or stale) and verdict in ("accept", "accept-with-mitigation") and not dec.get("fallback"):
        errs.append("maintainers is 1 or last_release is older than 12 months and decision.fallback is missing (r-maintainer-and-release-recency)")
    open_adv = (obj.get("advisory_lookup") or {}).get("open_advisories") or []
    if open_adv and verdict == "accept":
        errs.append(f"open advisories {open_adv} with verdict accept; use reject or accept-with-mitigation (r-advisory-query-in-evidence)")
    if open_adv and verdict == "accept-with-mitigation" and (dec.get("mitigation") or {}).get("advisory_id") not in open_adv:
        errs.append("decision.mitigation.advisory_id is not one of the open advisories (r-advisory-query-in-evidence)")
    lines = inputs.get("useful_surface_lines")
    if isinstance(lines, int) and lines <= 20 and verdict != "in-house" and not dec.get("override_reason"):
        errs.append(f"useful_surface_lines {lines} is 20 or fewer; verdict must be in-house or decision.override_reason must say what the package does that twenty lines cannot (r-alternative-considered-including-in-house)")
    near = (pkg.get("near_name") or {}).get("popular_near_name")
    remote_hook = any(_REMOTE.search(h.get("runs", "")) for h in (pkg.get("install_scripts") or {}).get("hooks") or [])
    if (near or pkg.get("repository_matches") is False) and verdict != "reject":
        errs.append("popular near-name or repository mismatch with a verdict other than reject (r-install-hooks-and-provenance-reviewed)")
    if remote_hook and verdict != "reject" and not dec.get("install_hook_reason"):
        errs.append("an install hook fetches or runs a remote binary; reject, or give decision.install_hook_reason (r-install-hooks-and-provenance-reviewed)")
    if (obj.get("alert_routing") or {}).get("recipient") != obj.get("owner"):
        errs.append("alert_routing.recipient differs from owner (r-upgrade-owner-and-patch-window)")
    if f"{pkg.get('name')}@{pkg.get('version')}" not in dec.get("statement", ""):
        errs.append(f"decision.statement does not name {pkg.get('name')}@{pkg.get('version')} (r-exact-version-pinned-in-lockfile)")
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
        prog="validate-new-dependency-risk-checklist.py",
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
