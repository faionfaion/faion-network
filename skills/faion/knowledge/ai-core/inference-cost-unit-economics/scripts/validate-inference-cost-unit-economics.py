#!/usr/bin/env python3
"""validate-inference-cost-unit-economics.py

Validate the unit-economics report produced by the inference-cost-unit-economics methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/inference-cost-unit-economics.json', 'title': 'Inference cost unit-economics report', 'type': 'object', 'required': ['report_id', 'as_of', 'author', 'window', 'token_source', 'headline_metric', 'price_sheet', 'features', 'over_ceiling'], 'additionalProperties': False, 'properties': {'report_id': {'type': 'string', 'pattern': '^[a-z0-9-]+$'}, 'as_of': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'author': {'type': 'string', 'minLength': 3}, 'window': {'type': 'object', 'required': ['start', 'end', 'days'], 'properties': {'start': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'end': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'days': {'type': 'integer', 'minimum': 7}}}, 'token_source': {'const': 'provider_usage'}, 'headline_metric': {'const': 'cost_per_successful_outcome'}, 'price_sheet': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['provider', 'model_id', 'sheet_date', 'input_price_per_1m', 'output_price_per_1m', 'discount_pct'], 'properties': {'provider': {'type': 'string', 'minLength': 2}, 'model_id': {'type': 'string', 'minLength': 3}, 'sheet_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'sheet_url': {'type': 'string'}, 'input_price_per_1m': {'type': 'number', 'minimum': 0}, 'output_price_per_1m': {'type': 'number', 'minimum': 0}, 'cached_input_price_per_1m': {'type': 'number', 'minimum': 0}, 'batch_price_per_1m': {'type': 'number', 'minimum': 0}, 'discount_pct': {'type': 'number', 'minimum': 0, 'maximum': 100}, 'discount_kind': {'type': 'string', 'enum': ['none', 'negotiated', 'committed_use', 'batch']}}}}, 'features': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['feature_id', 'success_definition', 'successful_outcomes', 'cost_lines', 'cost_per_outcome', 'retry_share_pct', 'first_action', 'revenue_basis', 'revenue_per_outcome', 'gross_margin_pct', 'target_gross_margin_pct', 'cost_ceiling_per_outcome', 'tail_dominated', 'daily_spend_alert'], 'properties': {'feature_id': {'type': 'string', 'pattern': '^[a-z0-9-]+$'}, 'success_definition': {'type': 'string', 'minLength': 10}, 'successful_outcomes': {'type': 'integer', 'minimum': 1}, 'cost_lines': {'type': 'object', 'required': ['input_tokens', 'output_tokens', 'retrieval', 'tools'], 'properties': {'input_tokens': {'type': 'number', 'minimum': 0}, 'output_tokens': {'type': 'number', 'minimum': 0}, 'cached_input_tokens': {'type': 'number', 'minimum': 0}, 'retrieval': {'type': 'number', 'minimum': 0}, 'tools': {'type': 'number', 'minimum': 0}}}, 'cost_per_call': {'type': 'number', 'minimum': 0}, 'cost_per_outcome': {'type': 'object', 'required': ['p50', 'p95', 'mean'], 'properties': {'p50': {'type': 'number', 'minimum': 0}, 'p95': {'type': 'number', 'minimum': 0}, 'mean': {'type': 'number', 'minimum': 0}}}, 'retry_share_pct': {'type': 'number', 'minimum': 0, 'maximum': 100}, 'retry_cause': {'type': 'string', 'minLength': 5}, 'first_action': {'type': 'string', 'enum': ['retry_policy', 'prompt', 'model', 'retrieval', 'tools', 'pricing', 'none']}, 'revenue_basis': {'type': 'object', 'required': ['kind'], 'properties': {'kind': {'type': 'string', 'enum': ['attributed_revenue', 'allocation_rule', 'value_proxy']}, 'allocation_key': {'type': 'string', 'minLength': 3}, 'derivation': {'type': 'string', 'minLength': 10}}, 'allOf': [{'if': {'properties': {'kind': {'const': 'allocation_rule'}}}, 'then': {'required': ['allocation_key']}}, {'if': {'properties': {'kind': {'const': 'value_proxy'}}}, 'then': {'required': ['derivation']}}]}, 'revenue_per_outcome': {'type': 'number', 'minimum': 0}, 'gross_margin_pct': {'type': 'number', 'maximum': 100}, 'target_gross_margin_pct': {'type': 'number', 'minimum': 0, 'maximum': 100}, 'cost_ceiling_per_outcome': {'type': 'number', 'minimum': 0}, 'tail_dominated': {'type': 'boolean'}, 'tail_driver': {'type': 'string', 'enum': ['long_context', 'agent_loops', 'tool_retries', 'large_model_fallback', 'other']}, 'daily_spend_alert': {'type': 'object', 'required': ['threshold_kind', 'threshold', 'wired_to'], 'properties': {'threshold_kind': {'type': 'string', 'enum': ['absolute_per_day', 'pct_over_trailing_7d']}, 'threshold': {'type': 'number', 'exclusiveMinimum': 0}, 'wired_to': {'type': 'string', 'minLength': 3}}}}, 'allOf': [{'if': {'properties': {'retry_share_pct': {'exclusiveMinimum': 15}}}, 'then': {'required': ['retry_cause'], 'properties': {'first_action': {'const': 'retry_policy'}}}}, {'if': {'properties': {'tail_dominated': {'const': True}}}, 'then': {'required': ['tail_driver']}}]}}, 'over_ceiling': {'type': 'array', 'items': {'type': 'object', 'required': ['feature_id', 'gap_per_outcome', 'action_owner'], 'properties': {'feature_id': {'type': 'string'}, 'gap_per_outcome': {'type': 'number', 'exclusiveMinimum': 0}, 'action_owner': {'type': 'string', 'minLength': 3}}}}}}

OK = {'report_id': 'support-agent-unit-economics-2026q2', 'as_of': '2026-06-30', 'author': 'ml-finance@acme.example', 'window': {'start': '2026-06-01', 'end': '2026-06-28', 'days': 28}, 'token_source': 'provider_usage', 'headline_metric': 'cost_per_successful_outcome', 'price_sheet': [{'provider': 'anthropic', 'model_id': 'claude-sonnet-4-20250514', 'sheet_date': '2026-06-01', 'sheet_url': 'https://www.anthropic.com/pricing', 'input_price_per_1m': 3.0, 'output_price_per_1m': 15.0, 'cached_input_price_per_1m': 0.3, 'discount_pct': 10, 'discount_kind': 'committed_use'}], 'features': [{'feature_id': 'support-agent', 'success_definition': 'ticket marked resolved by the customer within 24h of the last bot turn, no reopen within 7 days', 'successful_outcomes': 41280, 'cost_lines': {'input_tokens': 0.19, 'output_tokens': 0.12, 'cached_input_tokens': 0.02, 'retrieval': 0.06, 'tools': 0.05}, 'cost_per_call': 0.04, 'cost_per_outcome': {'p50': 0.31, 'p95': 0.97, 'mean': 0.44}, 'retry_share_pct': 12, 'first_action': 'prompt', 'revenue_basis': {'kind': 'value_proxy', 'derivation': 'blended human-agent cost per resolved ticket from the Q1 support P&L, $4.10, used as value delivered'}, 'revenue_per_outcome': 4.1, 'gross_margin_pct': 89.3, 'target_gross_margin_pct': 85, 'cost_ceiling_per_outcome': 0.62, 'tail_dominated': False, 'daily_spend_alert': {'threshold_kind': 'pct_over_trailing_7d', 'threshold': 30, 'wired_to': 'grafana:alerts/llm-spend-support-agent'}}, {'feature_id': 'contract-summariser', 'success_definition': 'summary accepted by the reviewer without edits to the obligations table', 'successful_outcomes': 2140, 'cost_lines': {'input_tokens': 1.84, 'output_tokens': 0.41, 'retrieval': 0.0, 'tools': 0.09}, 'cost_per_outcome': {'p50': 1.9, 'p95': 11.6, 'mean': 3.35}, 'retry_share_pct': 22, 'retry_cause': 'JSON schema validation failures on the obligations table trigger up to 3 re-generations of the full summary', 'first_action': 'retry_policy', 'revenue_basis': {'kind': 'allocation_rule', 'allocation_key': 'share of enterprise-tier ARR by feature usage minutes'}, 'revenue_per_outcome': 6.2, 'gross_margin_pct': 46.0, 'target_gross_margin_pct': 70, 'cost_ceiling_per_outcome': 1.86, 'tail_dominated': True, 'tail_driver': 'long_context', 'daily_spend_alert': {'threshold_kind': 'absolute_per_day', 'threshold': 400, 'wired_to': 'pagerduty:llm-spend'}}], 'over_ceiling': [{'feature_id': 'contract-summariser', 'gap_per_outcome': 1.49, 'action_owner': 'kim@acme.example'}]}

BAD = {'report_id': 'support-agent-unit-economics-2026q2', 'as_of': '2026-06-30', 'author': 'ml-finance@acme.example', 'window': {'start': '2026-06-26', 'end': '2026-06-28', 'days': 3}, 'token_source': 'estimated_from_chars', 'headline_metric': 'cost_per_call', 'price_sheet': [{'provider': 'anthropic', 'model_id': 'claude-sonnet', 'sheet_date': '2026-06-01', 'input_price_per_1m': 3.0, 'output_price_per_1m': 15.0, 'discount_pct': 0}], 'features': [{'feature_id': 'support-agent', 'success_definition': 'ticket marked resolved by the customer within 24h of the last bot turn', 'successful_outcomes': 41280, 'cost_lines': {'llm': 0.33, 'retrieval': 0.06, 'tools': 0.05}, 'cost_per_outcome': {'mean': 0.44}, 'retry_share_pct': 40, 'first_action': 'prompt', 'revenue_basis': {'kind': 'allocation_rule'}, 'revenue_per_outcome': 4.1, 'gross_margin_pct': 89.3, 'target_gross_margin_pct': 85, 'cost_ceiling_per_outcome': 0.62, 'tail_dominated': True, 'daily_spend_alert': {'threshold_kind': 'pct_over_trailing_7d', 'threshold': 30, 'wired_to': 'grafana:alerts/llm-spend-support-agent'}}], 'over_ceiling': []}


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
        prog="validate-inference-cost-unit-economics.py",
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
