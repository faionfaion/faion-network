#!/usr/bin/env python3
"""validate-latency-budget-allocation.py

Validate the latency budget allocation produced by the latency-budget-allocation methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/latency-budget-allocation.json', 'title': 'Latency budget allocation', 'type': 'object', 'required': ['slo', 'composition', 'hops', 'reserve_ms', 'ci_gate', 'review'], 'additionalProperties': False, 'properties': {'slo': {'type': 'object', 'required': ['name', 'metric', 'percentile', 'threshold_ms', 'measurement_point', 'window_days', 'budget_measurement_point_matches'], 'properties': {'name': {'type': 'string', 'minLength': 3}, 'metric': {'type': 'string', 'minLength': 3}, 'percentile': {'type': 'string', 'enum': ['p90', 'p95', 'p99', 'p999']}, 'threshold_ms': {'type': 'integer', 'exclusiveMinimum': 0}, 'measurement_point': {'type': 'string', 'enum': ['client', 'edge', 'load_balancer', 'server']}, 'window_days': {'type': 'integer', 'minimum': 1}, 'budget_measurement_point_matches': {'type': 'boolean'}, 'difference_hop_id': {'type': 'string', 'pattern': '^hop-[a-z0-9-]+$'}}, 'if': {'properties': {'budget_measurement_point_matches': {'const': False}}}, 'then': {'required': ['difference_hop_id']}}, 'composition': {'type': 'object', 'required': ['model', 'sum_of_hop_budgets_ms', 'percentiles_added_as_proof', 'verified_against'], 'properties': {'model': {'type': 'string', 'enum': ['sequential_sum_plus_headroom', 'critical_path_with_parallel_stages']}, 'sum_of_hop_budgets_ms': {'type': 'integer', 'minimum': 0}, 'percentiles_added_as_proof': {'const': False}, 'verified_against': {'type': 'object', 'required': ['end_to_end_histogram', 'measured_percentile_ms', 'window_days', 'request_count'], 'properties': {'end_to_end_histogram': {'type': 'string', 'minLength': 3}, 'measured_percentile_ms': {'type': 'integer', 'minimum': 0}, 'window_days': {'type': 'integer', 'minimum': 1}, 'request_count': {'type': 'integer', 'minimum': 1000}}}}}, 'hops': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['id', 'service', 'owner_team', 'metric', 'measured_side', 'budget_ms', 'measured_p95_ms', 'reconciliation', 'bucket_boundary_within_10pct_of_budget', 'timeout_and_retry', 'deadline_propagated'], 'properties': {'id': {'type': 'string', 'pattern': '^hop-[a-z0-9-]+$'}, 'service': {'type': 'string', 'minLength': 2}, 'owner_team': {'type': 'string', 'minLength': 2}, 'metric': {'type': 'object', 'required': ['histogram', 'labels'], 'properties': {'histogram': {'type': 'string', 'minLength': 3}, 'labels': {'type': 'object'}}}, 'measured_side': {'const': 'caller'}, 'budget_ms': {'type': 'integer', 'exclusiveMinimum': 0}, 'measured_p95_ms': {'type': 'integer', 'minimum': 0}, 'reconciliation': {'type': 'string', 'enum': ['within_budget', 'underwater', 'slack_over_2x']}, 'improvement_ticket': {'type': 'string', 'minLength': 3}, 'improvement_owner': {'type': 'string', 'minLength': 2}, 'slack_justification': {'type': 'string', 'minLength': 10}, 'bucket_boundary_within_10pct_of_budget': {'type': 'boolean'}, 'bucket_change_task': {'type': 'string', 'minLength': 3}, 'timeout_and_retry': {'type': 'object', 'required': ['timeout_ms', 'max_attempts', 'backoff_ms', 'worst_case_ms', 'worst_case_within_budget'], 'properties': {'timeout_ms': {'type': 'integer', 'exclusiveMinimum': 0}, 'max_attempts': {'type': 'integer', 'minimum': 1, 'maximum': 5}, 'backoff_ms': {'type': 'integer', 'minimum': 0}, 'worst_case_ms': {'type': 'integer', 'exclusiveMinimum': 0}, 'worst_case_within_budget': {'const': True}}}, 'deadline_propagated': {'const': True}, 'fan_out': {'type': 'object', 'required': ['n', 'stage_percentile', 'child_percentile', 'mitigation'], 'properties': {'n': {'type': 'integer', 'minimum': 2}, 'stage_percentile': {'type': 'string', 'enum': ['p90', 'p95', 'p99', 'p999']}, 'child_percentile': {'type': 'string', 'enum': ['p99', 'p999', 'p9999']}, 'mitigation': {'type': 'string', 'enum': ['tighter_child_budget', 'hedged_requests', 'partial_results_after_deadline']}}}}, 'allOf': [{'if': {'properties': {'reconciliation': {'const': 'underwater'}}}, 'then': {'required': ['improvement_ticket', 'improvement_owner']}}, {'if': {'properties': {'reconciliation': {'const': 'slack_over_2x'}}}, 'then': {'required': ['slack_justification']}}, {'if': {'properties': {'bucket_boundary_within_10pct_of_budget': {'const': False}}}, 'then': {'required': ['bucket_change_task']}}]}}, 'reserve_ms': {'type': 'integer', 'minimum': 0}, 'ci_gate': {'type': 'object', 'required': ['command', 'environment', 'min_requests_per_run', 'statistic', 'thresholds', 'on_failure', 'blocking_enabled_by_agent'], 'properties': {'command': {'type': 'string', 'minLength': 5}, 'environment': {'type': 'string', 'minLength': 3}, 'min_requests_per_run': {'type': 'integer', 'minimum': 200}, 'statistic': {'type': 'string', 'enum': ['percentile']}, 'thresholds': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['hop_id', 'percentile', 'threshold_ms'], 'properties': {'hop_id': {'type': 'string', 'pattern': '^(hop-[a-z0-9-]+|end-to-end)$'}, 'percentile': {'type': 'string', 'enum': ['p90', 'p95', 'p99', 'p999']}, 'threshold_ms': {'type': 'integer', 'exclusiveMinimum': 0}}}}, 'on_failure': {'type': 'string', 'enum': ['block_merge', 'warn']}, 'warn_owner': {'type': 'string', 'minLength': 2}, 'blocking_enabled_by_agent': {'const': False}}, 'if': {'properties': {'on_failure': {'const': 'warn'}}}, 'then': {'required': ['warn_owner']}}, 'review': {'type': 'object', 'required': ['status'], 'properties': {'status': {'type': 'string', 'enum': ['draft', 'ready_for_review', 'approved']}, 'reviewer': {'type': 'string', 'minLength': 2}, 'approved_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}, 'if': {'properties': {'status': {'const': 'approved'}}}, 'then': {'required': ['reviewer', 'approved_on']}}}}

OK = {'slo': {'name': 'checkout p95 at the edge', 'metric': 'checkout_request_duration_seconds', 'percentile': 'p95', 'threshold_ms': 800, 'measurement_point': 'edge', 'window_days': 28, 'budget_measurement_point_matches': True}, 'composition': {'model': 'critical_path_with_parallel_stages', 'sum_of_hop_budgets_ms': 700, 'percentiles_added_as_proof': False, 'verified_against': {'end_to_end_histogram': 'checkout_request_duration_seconds{point="edge"}', 'measured_percentile_ms': 742, 'window_days': 28, 'request_count': 4180000}}, 'hops': [{'id': 'hop-edge-to-gateway', 'service': 'cdn + api-gateway', 'owner_team': 'platform', 'metric': {'histogram': 'gateway_upstream_duration_seconds', 'labels': {'route': '/checkout'}}, 'measured_side': 'caller', 'budget_ms': 80, 'measured_p95_ms': 61, 'reconciliation': 'within_budget', 'bucket_boundary_within_10pct_of_budget': True, 'timeout_and_retry': {'timeout_ms': 80, 'max_attempts': 1, 'backoff_ms': 0, 'worst_case_ms': 80, 'worst_case_within_budget': True}, 'deadline_propagated': True}, {'id': 'hop-checkout-svc', 'service': 'checkout-service', 'owner_team': 'checkout', 'metric': {'histogram': 'http_client_duration_seconds', 'labels': {'caller': 'api-gateway', 'callee': 'checkout-service'}}, 'measured_side': 'caller', 'budget_ms': 120, 'measured_p95_ms': 98, 'reconciliation': 'within_budget', 'bucket_boundary_within_10pct_of_budget': True, 'timeout_and_retry': {'timeout_ms': 100, 'max_attempts': 1, 'backoff_ms': 0, 'worst_case_ms': 100, 'worst_case_within_budget': True}, 'deadline_propagated': True}, {'id': 'hop-inventory-fanout', 'service': 'inventory-shards', 'owner_team': 'inventory', 'metric': {'histogram': 'grpc_client_duration_seconds', 'labels': {'caller': 'checkout-service', 'callee': 'inventory-shard'}}, 'measured_side': 'caller', 'budget_ms': 250, 'measured_p95_ms': 212, 'reconciliation': 'within_budget', 'bucket_boundary_within_10pct_of_budget': True, 'timeout_and_retry': {'timeout_ms': 110, 'max_attempts': 2, 'backoff_ms': 10, 'worst_case_ms': 230, 'worst_case_within_budget': True}, 'deadline_propagated': True, 'fan_out': {'n': 12, 'stage_percentile': 'p95', 'child_percentile': 'p999', 'mitigation': 'hedged_requests'}}, {'id': 'hop-pricing', 'service': 'pricing-service', 'owner_team': 'pricing', 'metric': {'histogram': 'http_client_duration_seconds', 'labels': {'caller': 'checkout-service', 'callee': 'pricing-service'}}, 'measured_side': 'caller', 'budget_ms': 150, 'measured_p95_ms': 176, 'reconciliation': 'underwater', 'improvement_ticket': 'https://jira.acme.example/browse/PRICE-812', 'improvement_owner': 'pricing', 'bucket_boundary_within_10pct_of_budget': False, 'bucket_change_task': 'https://jira.acme.example/browse/OBS-301 add 0.15s bucket', 'timeout_and_retry': {'timeout_ms': 140, 'max_attempts': 1, 'backoff_ms': 0, 'worst_case_ms': 140, 'worst_case_within_budget': True}, 'deadline_propagated': True}, {'id': 'hop-payment-auth', 'service': 'payment-gateway (external)', 'owner_team': 'payments', 'metric': {'histogram': 'http_client_duration_seconds', 'labels': {'caller': 'checkout-service', 'callee': 'psp'}}, 'measured_side': 'caller', 'budget_ms': 100, 'measured_p95_ms': 38, 'reconciliation': 'slack_over_2x', 'slack_justification': 'PSP contract allows 250 ms p95 on peak days; 100 ms is the floor we can defend without a second provider', 'bucket_boundary_within_10pct_of_budget': True, 'timeout_and_retry': {'timeout_ms': 90, 'max_attempts': 1, 'backoff_ms': 0, 'worst_case_ms': 90, 'worst_case_within_budget': True}, 'deadline_propagated': True}], 'reserve_ms': 100, 'ci_gate': {'command': 'k6 run --vus 40 --duration 3m perf/checkout.js --out json=perf/out.json && perf/check-thresholds.py perf/out.json budget.json', 'environment': 'perf-staging (same instance sizes as production, seeded dataset perf-2026-06)', 'min_requests_per_run': 5000, 'statistic': 'percentile', 'thresholds': [{'hop_id': 'end-to-end', 'percentile': 'p95', 'threshold_ms': 800}, {'hop_id': 'hop-checkout-svc', 'percentile': 'p95', 'threshold_ms': 120}, {'hop_id': 'hop-inventory-fanout', 'percentile': 'p95', 'threshold_ms': 250}, {'hop_id': 'hop-pricing', 'percentile': 'p95', 'threshold_ms': 150}], 'on_failure': 'block_merge', 'blocking_enabled_by_agent': False}, 'review': {'status': 'ready_for_review', 'reviewer': 'checkout-lead@acme.example'}}

BAD = {'slo': {'name': 'checkout p95', 'metric': 'checkout_request_duration_seconds', 'percentile': 'p95', 'threshold_ms': 800, 'measurement_point': 'client', 'window_days': 28, 'budget_measurement_point_matches': False}, 'composition': {'model': 'sequential_sum_plus_headroom', 'sum_of_hop_budgets_ms': 800, 'percentiles_added_as_proof': True, 'verified_against': {'end_to_end_histogram': 'none', 'measured_percentile_ms': 0, 'window_days': 1, 'request_count': 50}}, 'hops': [{'id': 'hop-inventory-fanout', 'service': 'inventory-shards', 'owner_team': 'inventory', 'metric': {'histogram': 'grpc_server_duration_seconds', 'labels': {}}, 'measured_side': 'server', 'budget_ms': 250, 'measured_p95_ms': 212, 'reconciliation': 'within_budget', 'bucket_boundary_within_10pct_of_budget': False, 'timeout_and_retry': {'timeout_ms': 500, 'max_attempts': 3, 'backoff_ms': 100, 'worst_case_ms': 1700, 'worst_case_within_budget': False}, 'deadline_propagated': False, 'fan_out': {'n': 12, 'stage_percentile': 'p95', 'child_percentile': 'p95', 'mitigation': 'tighter_child_budget'}}, {'id': 'hop-pricing', 'service': 'pricing-service', 'owner_team': 'pricing', 'metric': {'histogram': 'http_client_duration_seconds', 'labels': {'callee': 'pricing-service'}}, 'measured_side': 'caller', 'budget_ms': 150, 'measured_p95_ms': 176, 'reconciliation': 'underwater', 'bucket_boundary_within_10pct_of_budget': True, 'timeout_and_retry': {'timeout_ms': 140, 'max_attempts': 1, 'backoff_ms': 0, 'worst_case_ms': 140, 'worst_case_within_budget': True}, 'deadline_propagated': True}], 'reserve_ms': 0, 'ci_gate': {'command': 'run the perf tests', 'environment': "someone's laptop", 'min_requests_per_run': 50, 'statistic': 'mean', 'thresholds': [{'hop_id': 'end-to-end', 'percentile': 'p95', 'threshold_ms': 800}], 'on_failure': 'warn', 'blocking_enabled_by_agent': True}, 'review': {'status': 'approved'}}


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
        prog="validate-latency-budget-allocation.py",
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
