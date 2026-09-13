#!/usr/bin/env python3
"""validate-pr-pattern-mining-for-feedback.py

Validate the feedback report produced by the pr-pattern-mining-for-feedback methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/pr-pattern-mining-for-feedback.json', 'title': 'PR pattern-mining feedback report', 'type': 'object', 'required': ['scope', 'corpus', 'ranking_basis', 'top_patterns', 'appendix_patterns', 'single_occurrence', 'automation_gap', 'suggested_rules', 'notes', 'review'], 'additionalProperties': False, 'definitions': {'pattern': {'type': 'object', 'required': ['id', 'behaviour', 'before_example', 'after_example', 'distinct_prs', 'distinct_reviewers', 'comment_urls', 'count', 'cost', 'score', 'baseline_count', 'remeasure_date', 'formatter_coverable'], 'properties': {'id': {'type': 'string', 'pattern': '^p[0-9]+$'}, 'behaviour': {'type': 'string', 'minLength': 20, 'pattern': '^(?!.*\\b(careless|lazy|sloppy|does not think|lacks rigou?r)\\b).*$'}, 'before_example': {'type': 'string', 'minLength': 5}, 'after_example': {'type': 'string', 'minLength': 5}, 'distinct_prs': {'type': 'integer', 'minimum': 3}, 'distinct_reviewers': {'type': 'integer', 'minimum': 1}, 'comment_urls': {'type': 'array', 'minItems': 3, 'items': {'type': 'string', 'pattern': '^https?://.+#(discussion_r|issuecomment-|note_)[0-9]+'}}, 'count': {'type': 'integer', 'minimum': 3}, 'cost': {'type': 'number', 'minimum': 0}, 'score': {'type': 'number', 'minimum': 0}, 'baseline_count': {'type': 'integer', 'minimum': 0}, 'remeasure_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'delta_vs_previous': {'type': 'integer'}, 'formatter_coverable': {'const': False}}, 'anyOf': [{'properties': {'distinct_reviewers': {'minimum': 2}}}, {'properties': {'distinct_reviewers': {'const': 1}, 'distinct_prs': {'minimum': 5}}}]}}, 'properties': {'scope': {'type': 'object', 'required': ['kind', 'per_author_counts_listed'], 'properties': {'kind': {'type': 'string', 'enum': ['team', 'mentee']}, 'mentee_handle': {'type': 'string', 'minLength': 2}, 'mentee_is_primary_reader': {'type': 'boolean'}, 'feeds_performance_evaluation': {'type': 'boolean'}, 'per_author_counts_listed': {'type': 'boolean'}}, 'if': {'properties': {'kind': {'const': 'mentee'}}}, 'then': {'required': ['mentee_handle', 'mentee_is_primary_reader', 'feeds_performance_evaluation'], 'properties': {'mentee_is_primary_reader': {'const': True}}}, 'else': {'properties': {'per_author_counts_listed': {'const': False}}}}, 'corpus': {'type': 'object', 'required': ['repositories', 'window_start', 'window_end', 'merged_prs', 'review_comments', 'query', 'sufficient_sample'], 'properties': {'repositories': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 3}}, 'window_start': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'window_end': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'merged_prs': {'type': 'integer', 'minimum': 0}, 'review_comments': {'type': 'integer', 'minimum': 0}, 'query': {'type': 'string', 'minLength': 10}, 'sufficient_sample': {'type': 'boolean'}}, 'if': {'properties': {'sufficient_sample': {'const': True}}}, 'then': {'properties': {'merged_prs': {'minimum': 20}, 'review_comments': {'minimum': 100}}}}, 'previous_report_url': {'type': 'string', 'pattern': '^https?://'}, 'ranking_basis': {'type': 'string', 'enum': ['review_round_trips', 'label_severity']}, 'top_patterns': {'type': 'array', 'maxItems': 5, 'items': {'$ref': '#/definitions/pattern'}}, 'appendix_patterns': {'type': 'array', 'items': {'$ref': '#/definitions/pattern'}}, 'single_occurrence': {'type': 'array', 'items': {'type': 'object', 'required': ['behaviour', 'comment_urls'], 'properties': {'behaviour': {'type': 'string', 'minLength': 10}, 'comment_urls': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'pattern': '^https?://'}}}}}, 'automation_gap': {'type': 'object', 'required': ['comments_excluded'], 'properties': {'comments_excluded': {'type': 'integer', 'minimum': 0}, 'tool': {'type': 'string', 'minLength': 2}, 'config_change': {'type': 'string', 'minLength': 3}}, 'if': {'properties': {'comments_excluded': {'minimum': 1}}}, 'then': {'required': ['tool', 'config_change']}}, 'suggested_rules': {'type': 'array', 'items': {'type': 'object', 'required': ['pattern_id', 'rule', 'channel', 'status', 'cycles_without_drop'], 'properties': {'pattern_id': {'type': 'string', 'pattern': '^p[0-9]+$'}, 'rule': {'type': 'string', 'minLength': 15}, 'channel': {'type': 'string', 'enum': ['linter_or_formatter_rule', 'ci_check_or_test', 'pr_template_checkbox', 'written_guideline']}, 'channel_id': {'type': 'string', 'minLength': 2}, 'why_not_earlier_channels': {'type': 'string', 'minLength': 10}, 'status': {'type': 'string', 'enum': ['new', 'active', 'ineffective', 'withdrawn']}, 'cycles_without_drop': {'type': 'integer', 'minimum': 0}}, 'allOf': [{'if': {'properties': {'channel': {'enum': ['linter_or_formatter_rule', 'ci_check_or_test']}}}, 'then': {'required': ['channel_id']}}, {'if': {'properties': {'channel': {'enum': ['ci_check_or_test', 'pr_template_checkbox', 'written_guideline']}}}, 'then': {'required': ['why_not_earlier_channels']}}, {'if': {'properties': {'cycles_without_drop': {'minimum': 2}}}, 'then': {'properties': {'status': {'enum': ['ineffective', 'withdrawn']}}}}]}}, 'notes': {'type': 'array', 'items': {'type': 'object', 'required': ['observation'], 'properties': {'observation': {'type': 'string', 'minLength': 10}, 'pattern_id': {'type': 'string'}}}}, 'review': {'type': 'object', 'required': ['status', 'shared_by_agent'], 'properties': {'status': {'type': 'string', 'enum': ['draft', 'ready_for_owner_check', 'checked_and_shared']}, 'owner': {'type': 'string', 'minLength': 2}, 'owner_checked_urls_and_scope_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'shared_by_agent': {'const': False}}, 'if': {'properties': {'status': {'const': 'checked_and_shared'}}}, 'then': {'required': ['owner', 'owner_checked_urls_and_scope_on']}}}, 'if': {'properties': {'corpus': {'properties': {'sufficient_sample': {'const': False}}, 'required': ['sufficient_sample']}}}, 'then': {'properties': {'top_patterns': {'maxItems': 0}, 'suggested_rules': {'maxItems': 0}}}}

OK = {'scope': {'kind': 'team', 'per_author_counts_listed': False}, 'corpus': {'repositories': ['acme/billing-api', 'acme/billing-worker'], 'window_start': '2026-04-01', 'window_end': '2026-06-30', 'merged_prs': 64, 'review_comments': 412, 'query': 'gh api graphql -f query=\'{ repository(owner:"acme", name:"billing-api") { pullRequests(states:MERGED, first:100, orderBy:{field:UPDATED_AT, direction:DESC}) { nodes { number mergedAt reviewThreads(first:100) { nodes { comments(first:50) { nodes { author { login } body url } } } } } } } }\' (both repos, filtered to mergedAt in window)', 'sufficient_sample': True}, 'ranking_basis': 'review_round_trips', 'top_patterns': [{'id': 'p1', 'behaviour': 'HTTP client call without a timeout: `requests.get(url)` blocks the worker indefinitely when the upstream hangs', 'before_example': 'resp = requests.get(url)', 'after_example': 'resp = requests.get(url, timeout=(3, 10))', 'distinct_prs': 11, 'distinct_reviewers': 4, 'comment_urls': ['https://github.com/acme/billing-api/pull/402#discussion_r1890011', 'https://github.com/acme/billing-api/pull/417#discussion_r1890877', 'https://github.com/acme/billing-worker/pull/88#discussion_r1891204'], 'count': 14, 'cost': 2.1, 'score': 29.4, 'baseline_count': 14, 'remeasure_date': '2026-09-30', 'formatter_coverable': False}, {'id': 'p2', 'behaviour': 'Test asserts only the HTTP status code; the response body and the side effect (row written, event published) are not asserted', 'before_example': 'assert resp.status_code == 200', 'after_example': 'assert resp.status_code == 200\nassert resp.json()["invoice_id"] == invoice.id\nassert Invoice.objects.filter(id=invoice.id, status="sent").exists()', 'distinct_prs': 7, 'distinct_reviewers': 3, 'comment_urls': ['https://github.com/acme/billing-api/pull/399#discussion_r1889120', 'https://github.com/acme/billing-api/pull/408#discussion_r1890340', 'https://github.com/acme/billing-api/pull/421#discussion_r1891560'], 'count': 9, 'cost': 1.8, 'score': 16.2, 'baseline_count': 9, 'remeasure_date': '2026-09-30', 'formatter_coverable': False}, {'id': 'p3', 'behaviour': 'N+1 query in list endpoints: related rows loaded per item inside the serializer loop', 'before_example': 'for inv in Invoice.objects.all(): inv.customer.name', 'after_example': 'for inv in Invoice.objects.select_related("customer"): inv.customer.name', 'distinct_prs': 5, 'distinct_reviewers': 2, 'comment_urls': ['https://github.com/acme/billing-api/pull/404#discussion_r1890205', 'https://github.com/acme/billing-api/pull/411#discussion_r1890733', 'https://github.com/acme/billing-api/pull/425#discussion_r1891902'], 'count': 6, 'cost': 2.5, 'score': 15.0, 'baseline_count': 6, 'remeasure_date': '2026-09-30', 'formatter_coverable': False}], 'appendix_patterns': [], 'single_occurrence': [{'behaviour': 'Retry loop without jitter on the payment-provider client', 'comment_urls': ['https://github.com/acme/billing-worker/pull/91#discussion_r1891330']}], 'automation_gap': {'comments_excluded': 38, 'tool': 'ruff', 'config_change': 'enable I001 (isort) and Q000 (quotes) in pyproject.toml [tool.ruff.lint] select; run ruff format in pre-commit'}, 'suggested_rules': [{'pattern_id': 'p1', 'rule': 'Every requests call passes an explicit timeout', 'channel': 'linter_or_formatter_rule', 'channel_id': 'flake8-bandit S113 (request-without-timeout) via ruff S113', 'status': 'new', 'cycles_without_drop': 0}, {'pattern_id': 'p2', 'rule': 'Endpoint tests assert body and side effect, not only status', 'channel': 'pr_template_checkbox', 'why_not_earlier_channels': 'No linter can judge assertion sufficiency; a CI check on assertion count would be gamed; the checkbox puts the question in front of the author at the moment it matters', 'status': 'new', 'cycles_without_drop': 0}, {'pattern_id': 'p3', 'rule': 'List endpoints use select_related or prefetch_related for every relation the serializer touches', 'channel': 'ci_check_or_test', 'channel_id': 'django-test-plus assertNumQueries on every list endpoint test', 'why_not_earlier_channels': "No static rule can see the serializer's relation access; a query-count assertion in CI catches the regression on the exact endpoint", 'status': 'new', 'cycles_without_drop': 0}], 'notes': [{'observation': 'Reviewers ask for ADR links on schema changes in 4 PRs; no channel yet, revisit when the ADR template lands', 'pattern_id': 'p4'}], 'review': {'status': 'ready_for_owner_check', 'owner': 'eng-manager@acme.example', 'shared_by_agent': False}}

BAD = {'scope': {'kind': 'team', 'per_author_counts_listed': True}, 'corpus': {'repositories': ['acme/billing-api'], 'window_start': '2026-06-20', 'window_end': '2026-06-30', 'merged_prs': 9, 'review_comments': 41, 'query': 'looked through recent PRs', 'sufficient_sample': True}, 'ranking_basis': 'review_round_trips', 'top_patterns': [{'id': 'p1', 'behaviour': 'Authors are careless about error handling', 'before_example': 'n/a', 'after_example': 'n/a', 'distinct_prs': 2, 'distinct_reviewers': 1, 'comment_urls': ['https://github.com/acme/billing-api/pull/430#discussion_r1892001'], 'count': 2, 'cost': 1, 'score': 2, 'baseline_count': 2, 'remeasure_date': '2026-09-30', 'formatter_coverable': False}, {'id': 'p2', 'behaviour': 'Imports are not sorted and quotes are inconsistent across the diff', 'before_example': 'import os\nimport sys\nimport json', 'after_example': 'import json\nimport os\nimport sys', 'distinct_prs': 12, 'distinct_reviewers': 3, 'comment_urls': ['https://github.com/acme/billing-api/pull/402#discussion_r1890011', 'https://github.com/acme/billing-api/pull/417#discussion_r1890877', 'https://github.com/acme/billing-api/pull/421#discussion_r1891560'], 'count': 38, 'cost': 0.3, 'score': 11.4, 'baseline_count': 38, 'remeasure_date': '2026-09-30', 'formatter_coverable': True}], 'appendix_patterns': [], 'single_occurrence': [], 'automation_gap': {'comments_excluded': 0}, 'suggested_rules': [{'pattern_id': 'p1', 'rule': 'Be more careful about error handling', 'channel': 'written_guideline', 'status': 'active', 'cycles_without_drop': 3}], 'notes': [], 'review': {'status': 'checked_and_shared', 'shared_by_agent': True}}


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
    """Draft-07 subset: $ref (local definitions), required, type, enum, const, pattern,
    minimum/maximum, exclusiveMinimum/Maximum, minLength/maxLength, minItems/maxItems,
    uniqueItems, items, contains, properties, additionalProperties, allOf/anyOf/oneOf/not,
    if/then/else."""
    if schema is True:
        return
    if schema is False:
        errs.append(f"{path}: schema forbids any value here")
        return
    if "$ref" in schema:
        target = SCHEMA
        for part in schema["$ref"].lstrip("#/").split("/"):
            target = target[part]
        _check(node, target, path, errs)
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
        if "contains" in schema and not any(not _probe(item, schema["contains"]) for item in node):
            errs.append(f"{path}: no item matches 'contains' {schema['contains']!r}")
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
        prog="validate-pr-pattern-mining-for-feedback.py",
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
