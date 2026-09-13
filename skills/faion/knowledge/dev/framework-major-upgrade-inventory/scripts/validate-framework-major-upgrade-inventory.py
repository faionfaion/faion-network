#!/usr/bin/env python3
"""validate-framework-major-upgrade-inventory.py

Validate the upgrade inventory produced by the framework-major-upgrade-inventory methodology against the
draft-07 JSON Schema embedded in content/02-output-contract.xml. Stdlib-only;
the schema and both fixtures are inlined because `faion get-content` ships
this file alone.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run the contract's own valid + invalid examples
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (VIOLATION lines on stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/framework-major-upgrade-inventory.json', 'title': 'Framework major-upgrade inventory (one major step)', 'type': 'object', 'required': ['repository', 'framework', 'deprecation_run', 'release_notes_covered', 'breaking_changes', 'unverified', 'dependent_packages', 'runtime_prerequisites', 'review'], 'additionalProperties': False, 'properties': {'repository': {'type': 'string', 'minLength': 3}, 'framework': {'type': 'object', 'required': ['name', 'current_version', 'target_version', 'current_major', 'target_major', 'major_gap', 'upgrade_guide_url'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'current_version': {'type': 'string', 'pattern': '^\\d+\\.\\d+(\\.\\d+)?'}, 'target_version': {'type': 'string', 'pattern': '^\\d+\\.\\d+(\\.\\d+)?'}, 'current_major': {'type': 'integer', 'minimum': 0}, 'target_major': {'type': 'integer', 'minimum': 1}, 'major_gap': {'const': 1}, 'step_index': {'type': 'integer', 'minimum': 1}, 'steps_total': {'type': 'integer', 'minimum': 1}, 'upgrade_guide_url': {'type': 'string', 'pattern': '^https?://'}}}, 'deprecation_run': {'type': 'object', 'required': ['command', 'ran_on_version', 'log_url', 'distinct_warnings', 'every_warning_has_an_entry'], 'properties': {'command': {'type': 'string', 'minLength': 5}, 'ran_on_version': {'type': 'string', 'pattern': '^\\d+\\.\\d+(\\.\\d+)?'}, 'log_url': {'type': 'string', 'minLength': 5}, 'distinct_warnings': {'type': 'integer', 'minimum': 0}, 'every_warning_has_an_entry': {'const': True}}}, 'release_notes_covered': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['version', 'url'], 'properties': {'version': {'type': 'string', 'pattern': '^\\d+\\.\\d+'}, 'url': {'type': 'string', 'pattern': '^https?://'}}}}, 'breaking_changes': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['id', 'title', 'vendor_citation', 'call_sites', 'status', 'classification', 'risk'], 'properties': {'id': {'type': 'string', 'pattern': '^bc-[a-z0-9-]+$'}, 'title': {'type': 'string', 'minLength': 5}, 'vendor_citation': {'type': 'object', 'required': ['url', 'version'], 'properties': {'url': {'type': 'string', 'pattern': '^https?://'}, 'version': {'type': 'string', 'pattern': '^\\d+\\.\\d+'}}}, 'from_deprecation_run': {'type': 'boolean'}, 'call_sites': {'type': 'object', 'required': ['count', 'search_kind', 'search_pattern', 'search_link'], 'properties': {'count': {'type': 'integer', 'minimum': 0}, 'search_kind': {'type': 'string', 'enum': ['grep', 'ripgrep', 'ast_query', 'codemod_dry_run', 'deprecation_run']}, 'search_pattern': {'type': 'string', 'minLength': 2}, 'search_link': {'type': 'string', 'minLength': 3}}}, 'status': {'type': 'string', 'enum': ['affected', 'not_affected']}, 'classification': {'type': 'string', 'enum': ['codemod', 'manual']}, 'codemod': {'type': 'object', 'required': ['tool', 'command', 'dry_run_diff_lines', 'documented_as_partial_or_experimental'], 'properties': {'tool': {'type': 'string', 'minLength': 2}, 'command': {'type': 'string', 'minLength': 5}, 'dry_run_diff_lines': {'type': 'integer', 'minimum': 0}, 'documented_as_partial_or_experimental': {'const': False}}}, 'risk': {'type': 'object', 'required': ['runs_in', 'blast_radius', 'detectability'], 'properties': {'runs_in': {'type': 'string', 'enum': ['production_requests', 'jobs', 'both', 'neither']}, 'blast_radius': {'type': 'integer', 'minimum': 0}, 'detectability': {'type': 'string', 'enum': ['compile_time', 'runtime_with_test', 'runtime_no_test']}, 'characterisation_test': {'type': 'string', 'minLength': 3}}, 'if': {'properties': {'detectability': {'const': 'runtime_no_test'}}}, 'then': {'required': ['characterisation_test']}}}, 'allOf': [{'if': {'properties': {'status': {'const': 'not_affected'}}}, 'then': {'properties': {'call_sites': {'properties': {'count': {'const': 0}}}}}}, {'if': {'properties': {'call_sites': {'properties': {'count': {'const': 0}}, 'required': ['count']}}}, 'then': {'properties': {'status': {'const': 'not_affected'}}}}, {'if': {'properties': {'classification': {'const': 'codemod'}}}, 'then': {'required': ['codemod']}}]}}, 'unverified': {'type': 'array', 'items': {'type': 'object', 'required': ['suspected_change', 'search_tried'], 'properties': {'suspected_change': {'type': 'string', 'minLength': 5}, 'search_tried': {'type': 'string', 'minLength': 5}}}}, 'dependent_packages': {'type': 'array', 'items': {'type': 'object', 'required': ['name', 'current_version', 'earliest_compatible_version', 'compatible_release_available', 'release_notes_url', 'blocker'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'current_version': {'type': 'string', 'minLength': 1}, 'earliest_compatible_version': {'type': 'string', 'minLength': 1}, 'compatible_release_available': {'type': 'boolean'}, 'release_notes_url': {'type': 'string', 'pattern': '^https?://'}, 'blocker': {'type': 'boolean'}, 'plan': {'type': 'string', 'enum': ['fork', 'replace', 'remove', 'wait_for_release']}, 'plan_detail': {'type': 'string', 'minLength': 5}}, 'allOf': [{'if': {'properties': {'compatible_release_available': {'const': False}}}, 'then': {'properties': {'blocker': {'const': True}}}}, {'if': {'properties': {'blocker': {'const': True}}}, 'then': {'required': ['plan', 'plan_detail']}}]}}, 'runtime_prerequisites': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['kind', 'target_minimum', 'source_url', 'environments', 'blocker'], 'properties': {'kind': {'type': 'string', 'enum': ['language', 'database', 'node', 'jvm', 'os_or_base_image', 'other']}, 'name': {'type': 'string'}, 'target_minimum': {'type': 'string', 'minLength': 1}, 'source_url': {'type': 'string', 'pattern': '^https?://'}, 'environments': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['name', 'current', 'meets_minimum'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'current': {'type': 'string', 'minLength': 1}, 'meets_minimum': {'type': 'boolean'}}}}, 'blocker': {'type': 'boolean'}, 'upgrade_plan': {'type': 'string', 'minLength': 5}}, 'if': {'properties': {'blocker': {'const': True}}}, 'then': {'required': ['upgrade_plan']}}}, 'review': {'type': 'object', 'required': ['status', 'upgrade_branch_opened_by_agent'], 'properties': {'status': {'type': 'string', 'enum': ['draft', 'ready_for_review', 'approved']}, 'reviewer': {'type': 'string', 'minLength': 3}, 'approved_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'upgrade_branch_opened_by_agent': {'const': False}}, 'if': {'properties': {'status': {'const': 'approved'}}}, 'then': {'required': ['reviewer', 'approved_on']}}}}

OK = {'repository': 'github.com/acme/billing-api', 'framework': {'name': 'Django', 'current_version': '4.2.11', 'target_version': '5.0.6', 'current_major': 4, 'target_major': 5, 'major_gap': 1, 'step_index': 1, 'steps_total': 1, 'upgrade_guide_url': 'https://docs.djangoproject.com/en/5.0/howto/upgrade-version/'}, 'deprecation_run': {'command': 'python -W error::DeprecationWarning -W error::PendingDeprecationWarning -m pytest', 'ran_on_version': '4.2.11', 'log_url': 'https://ci.acme.example/billing-api/runs/48211', 'distinct_warnings': 3, 'every_warning_has_an_entry': True}, 'release_notes_covered': [{'version': '5.0', 'url': 'https://docs.djangoproject.com/en/5.0/releases/5.0/'}], 'breaking_changes': [{'id': 'bc-form-rendering-div', 'title': 'Default form template changed to div-based rendering', 'vendor_citation': {'url': 'https://docs.djangoproject.com/en/5.0/releases/5.0/#forms', 'version': '5.0'}, 'from_deprecation_run': False, 'call_sites': {'count': 14, 'search_kind': 'ripgrep', 'search_pattern': 'as_table\\(\\)|\\{\\{ *form *\\}\\}', 'search_link': 'https://github.com/acme/billing-api/blob/main/docs/upgrade/5.0/searches.md#forms'}, 'status': 'affected', 'classification': 'manual', 'risk': {'runs_in': 'production_requests', 'blast_radius': 28, 'detectability': 'runtime_no_test', 'characterisation_test': 'tests/characterisation/test_form_rendering_snapshots.py'}}, {'id': 'bc-uslugify-usc-removed', 'title': 'django.utils.text.unescape_string_literal and USE_L10N removed', 'vendor_citation': {'url': 'https://docs.djangoproject.com/en/5.0/releases/5.0/#features-removed-in-5-0', 'version': '5.0'}, 'from_deprecation_run': True, 'call_sites': {'count': 2, 'search_kind': 'deprecation_run', 'search_pattern': 'RemovedInDjango50Warning: The USE_L10N setting is deprecated', 'search_link': 'https://ci.acme.example/billing-api/runs/48211#L212'}, 'status': 'affected', 'classification': 'codemod', 'codemod': {'tool': 'django-upgrade', 'command': "django-upgrade --target-version 5.0 $(git ls-files '*.py')", 'dry_run_diff_lines': 6, 'documented_as_partial_or_experimental': False}, 'risk': {'runs_in': 'both', 'blast_radius': 4, 'detectability': 'compile_time'}}, {'id': 'bc-index-together-removed', 'title': 'Meta.index_together removed in favour of Meta.indexes', 'vendor_citation': {'url': 'https://docs.djangoproject.com/en/5.0/releases/5.0/#features-removed-in-5-0', 'version': '5.0'}, 'from_deprecation_run': True, 'call_sites': {'count': 0, 'search_kind': 'ripgrep', 'search_pattern': 'index_together', 'search_link': 'https://github.com/acme/billing-api/blob/main/docs/upgrade/5.0/searches.md#index-together'}, 'status': 'not_affected', 'classification': 'manual', 'risk': {'runs_in': 'neither', 'blast_radius': 0, 'detectability': 'compile_time'}}], 'unverified': [{'suspected_change': 'Admin changelist row colouring in dark mode looks different on 5.0 in a screenshot from a colleague', 'search_tried': "release notes 5.0 admin section and the django/django changelog grep 'changelist' -- no entry found"}], 'dependent_packages': [{'name': 'djangorestframework', 'current_version': '3.14.0', 'earliest_compatible_version': '3.15.0', 'compatible_release_available': True, 'release_notes_url': 'https://www.django-rest-framework.org/community/release-notes/', 'blocker': False}, {'name': 'django-polymorphic', 'current_version': '3.1.0', 'earliest_compatible_version': 'none', 'compatible_release_available': False, 'release_notes_url': 'https://github.com/jazzband/django-polymorphic/releases', 'blocker': True, 'plan': 'replace', 'plan_detail': 'Replace the two polymorphic models with explicit multi-table inheritance; spike estimated in docs/upgrade/5.0/polymorphic.md'}], 'runtime_prerequisites': [{'kind': 'language', 'name': 'Python', 'target_minimum': '3.10', 'source_url': 'https://docs.djangoproject.com/en/5.0/releases/5.0/#python-compatibility', 'environments': [{'name': 'production', 'current': '3.11.9', 'meets_minimum': True}, {'name': 'staging', 'current': '3.11.9', 'meets_minimum': True}, {'name': 'ci', 'current': '3.11.9', 'meets_minimum': True}], 'blocker': False}, {'kind': 'database', 'name': 'PostgreSQL', 'target_minimum': '12', 'source_url': 'https://docs.djangoproject.com/en/5.0/releases/5.0/#dropped-support-for-postgresql-11', 'environments': [{'name': 'production', 'current': '15.6', 'meets_minimum': True}, {'name': 'staging', 'current': '15.6', 'meets_minimum': True}], 'blocker': False}], 'review': {'status': 'ready_for_review', 'reviewer': 'kim@acme.example', 'upgrade_branch_opened_by_agent': False}}

BAD = {'repository': 'github.com/acme/billing-api', 'framework': {'name': 'Django', 'current_version': '3.2.25', 'target_version': '5.0.6', 'current_major': 3, 'target_major': 5, 'major_gap': 2, 'upgrade_guide_url': 'https://docs.djangoproject.com/en/5.0/howto/upgrade-version/'}, 'deprecation_run': {'command': 'pytest', 'ran_on_version': '3.2.25', 'log_url': 'https://ci.acme.example/billing-api/runs/48000', 'distinct_warnings': 0, 'every_warning_has_an_entry': False}, 'release_notes_covered': [], 'breaking_changes': [{'id': 'bc-form-rendering-div', 'title': 'Default form template changed to div-based rendering', 'vendor_citation': {'url': 'https://someblog.example/django-5-gotchas', 'version': '5.0'}, 'call_sites': {'count': 0, 'search_kind': 'grep', 'search_pattern': 'as_table', 'search_link': 'n/a'}, 'status': 'affected', 'classification': 'codemod', 'risk': {'runs_in': 'production_requests', 'blast_radius': 28, 'detectability': 'runtime_no_test'}}], 'unverified': [], 'dependent_packages': [{'name': 'django-polymorphic', 'current_version': '3.1.0', 'earliest_compatible_version': 'none', 'compatible_release_available': False, 'release_notes_url': 'https://github.com/jazzband/django-polymorphic/releases', 'blocker': False}], 'runtime_prerequisites': [{'kind': 'language', 'name': 'Python', 'target_minimum': '3.10', 'source_url': 'https://docs.djangoproject.com/en/5.0/releases/5.0/#python-compatibility', 'environments': [{'name': 'production', 'current': '3.8.18', 'meets_minimum': False}], 'blocker': True}], 'review': {'status': 'approved', 'upgrade_branch_opened_by_agent': True}}


def _is_type(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        return (isinstance(value, int) and not isinstance(value, bool)) or (
            isinstance(value, float) and value.is_integer())
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    return True


def _check(node, schema, path, errs):
    """Draft-07 subset: required, type, enum, const, pattern, minimum/maximum,
    exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems, uniqueItems,
    items, properties, additionalProperties, allOf/anyOf/oneOf/not, if/then/else."""
    if schema is True:
        return
    if schema is False:
        errs.append(f"{path}: schema forbids any value here")
        return
    if "const" in schema and node != schema["const"]:
        errs.append(f"{path}: must equal {schema['const']!r}, got {node!r}")
    if "enum" in schema and node not in schema["enum"]:
        errs.append(f"{path}: {node!r} not in enum {schema['enum']!r}")
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_is_type(node, x) for x in types):
            errs.append(f"{path}: expected {t}, got {type(node).__name__}")
            return
    if isinstance(node, dict):
        for k in schema.get("required", []):
            if k not in node:
                errs.append(f"{path}.{k}: missing required field")
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in node:
                _check(node[k], sub, f"{path}.{k}", errs)
        addl = schema.get("additionalProperties", True)
        for k in node:
            if k not in props:
                if addl is False:
                    errs.append(f"{path}.{k}: additional property not allowed")
                elif isinstance(addl, dict):
                    _check(node[k], addl, f"{path}.{k}", errs)
    if isinstance(node, list):
        mn, mx = schema.get("minItems"), schema.get("maxItems")
        if mn is not None and len(node) < mn:
            errs.append(f"{path}: {len(node)} items, minItems={mn}")
        if mx is not None and len(node) > mx:
            errs.append(f"{path}: {len(node)} items, maxItems={mx}")
        if schema.get("uniqueItems"):
            seen = [json.dumps(x, sort_keys=True) for x in node]
            if len(seen) != len(set(seen)):
                errs.append(f"{path}: items must be unique")
        items = schema.get("items")
        if isinstance(items, dict):
            for i, item in enumerate(node):
                _check(item, items, f"{path}[{i}]", errs)
    if isinstance(node, str):
        mn, mx = schema.get("minLength"), schema.get("maxLength")
        if mn is not None and len(node) < mn:
            errs.append(f"{path}: length {len(node)} below minLength={mn}")
        if mx is not None and len(node) > mx:
            errs.append(f"{path}: length {len(node)} above maxLength={mx}")
        pat = schema.get("pattern")
        if pat is not None and not re.search(pat, node):
            errs.append(f"{path}: {node!r} does not match pattern {pat!r}")
    if isinstance(node, (int, float)) and not isinstance(node, bool):
        for key, bad in (("minimum", lambda v: node < v), ("maximum", lambda v: node > v),
                         ("exclusiveMinimum", lambda v: node <= v),
                         ("exclusiveMaximum", lambda v: node >= v)):
            if key in schema and bad(schema[key]):
                errs.append(f"{path}: {node!r} violates {key}={schema[key]!r}")
    for sub in schema.get("allOf", []):
        _check(node, sub, path, errs)
    if "anyOf" in schema:
        if not any(not _probe(node, s) for s in schema["anyOf"]):
            errs.append(f"{path}: matches none of anyOf")
    if "oneOf" in schema:
        hits = sum(1 for s in schema["oneOf"] if not _probe(node, s))
        if hits != 1:
            errs.append(f"{path}: matches {hits} of oneOf, need exactly 1")
    if "not" in schema and not _probe(node, schema["not"]):
        errs.append(f"{path}: matches forbidden 'not' schema")
    if "if" in schema:
        branch = "then" if not _probe(node, schema["if"]) else "else"
        if branch in schema:
            _check(node, schema[branch], path, errs)


def _probe(node, schema):
    tmp: list[str] = []
    _check(node, schema, "$", tmp)
    return tmp


def validate(obj) -> list[str]:
    errs: list[str] = []
    _check(obj, SCHEMA, "$", errs)
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
        prog="validate-framework-major-upgrade-inventory.py",
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
