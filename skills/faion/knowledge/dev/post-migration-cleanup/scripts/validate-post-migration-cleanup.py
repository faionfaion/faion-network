#!/usr/bin/env python3
"""validate-post-migration-cleanup.py

Validate the cleanup checklist produced by the post-migration-cleanup methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/post-migration-cleanup.json', 'title': 'Post-migration cleanup checklist', 'type': 'object', 'required': ['migration', 'dual_write', 'legacy_read_path', 'flags', 'shims', 'schema_drop', 'docs', 'observability', 'infrastructure', 'deferred_items', 'review'], 'additionalProperties': False, 'properties': {'migration': {'type': 'object', 'required': ['name', 'legacy_component', 'new_component', 'cutover_date', 'parity_window', 'delivery_cycle_days', 'cleanup_deadline'], 'properties': {'name': {'type': 'string', 'minLength': 3}, 'legacy_component': {'type': 'string', 'minLength': 2}, 'new_component': {'type': 'string', 'minLength': 2}, 'cutover_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'parity_window': {'type': 'object', 'required': ['start', 'end', 'days', 'includes_full_weekly_cycle'], 'properties': {'start': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'end': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'days': {'type': 'integer', 'minimum': 7}, 'includes_full_weekly_cycle': {'const': True}}}, 'delivery_cycle_days': {'type': 'integer', 'minimum': 1, 'maximum': 30}, 'cleanup_deadline': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}}, 'dual_write': {'type': 'object', 'required': ['reconciliation_report_url', 'consecutive_days_zero_mismatch', 'mismatches', 'legacy_write_removed_by', 'deletion_pr_url'], 'properties': {'reconciliation_report_url': {'type': 'string', 'pattern': '^https?://'}, 'consecutive_days_zero_mismatch': {'type': 'integer', 'minimum': 7}, 'mismatches': {'const': 0}, 'legacy_write_removed_by': {'const': 'code_deletion'}, 'deletion_pr_url': {'type': 'string', 'pattern': '^https?://'}}}, 'legacy_read_path': {'type': 'object', 'required': ['counter_name', 'zero_for_days', 'includes_batch_window', 'evidence_url', 'deletion_pr_url'], 'properties': {'counter_name': {'type': 'string', 'minLength': 3}, 'zero_for_days': {'type': 'integer', 'minimum': 7}, 'includes_batch_window': {'const': True}, 'evidence_url': {'type': 'string', 'pattern': '^https?://'}, 'deletion_pr_url': {'type': 'string', 'pattern': '^https?://'}}}, 'flags': {'type': 'array', 'items': {'type': 'object', 'required': ['key', 'removal_pr_url', 'key_deleted_from_flag_service', 'branches_collapsed'], 'properties': {'key': {'type': 'string', 'minLength': 2}, 'removal_pr_url': {'type': 'string', 'pattern': '^https?://'}, 'key_deleted_from_flag_service': {'const': True}, 'branches_collapsed': {'const': True}}}}, 'shims': {'type': 'array', 'items': {'type': 'object', 'required': ['name', 'kind', 'consumers', 'disposition'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'kind': {'type': 'string', 'enum': ['adapter', 'column_alias', 'endpoint_proxy', 'event_schema_translator', 'redirect', 'other']}, 'consumers': {'type': 'array', 'items': {'type': 'string', 'minLength': 2}}, 'disposition': {'type': 'string', 'enum': ['deleted_in_this_cleanup', 'retained']}, 'deletion_pr_url': {'type': 'string', 'pattern': '^https?://'}, 'removal_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'consumer_counter': {'type': 'string', 'minLength': 3}}, 'allOf': [{'if': {'properties': {'disposition': {'const': 'retained'}}}, 'then': {'properties': {'consumers': {'minItems': 1}}, 'anyOf': [{'required': ['removal_date']}, {'required': ['consumer_counter']}]}}, {'if': {'properties': {'disposition': {'const': 'deleted_in_this_cleanup'}}}, 'then': {'required': ['deletion_pr_url']}}]}}, 'schema_drop': {'type': 'object', 'required': ['objects', 'separate_change_from_code_deletion', 'snapshot', 'reference_scan'], 'properties': {'objects': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 2}}, 'separate_change_from_code_deletion': {'const': True}, 'snapshot': {'type': 'object', 'required': ['url', 'retention_until'], 'properties': {'url': {'type': 'string', 'minLength': 5}, 'retention_until': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}}, 'reference_scan': {'type': 'object', 'required': ['command', 'repositories_scanned', 'query_log_searched', 'hits'], 'properties': {'command': {'type': 'string', 'minLength': 5}, 'repositories_scanned': {'type': 'integer', 'minimum': 1}, 'query_log_searched': {'const': True}, 'hits': {'const': 0}}}, 'drop_change_url': {'type': 'string', 'pattern': '^https?://'}}}, 'docs': {'type': 'object', 'required': ['search_command', 'hits_before', 'hits_after_outside_archive', 'archive_location'], 'properties': {'search_command': {'type': 'string', 'minLength': 5}, 'hits_before': {'type': 'integer', 'minimum': 0}, 'hits_after_outside_archive': {'const': 0}, 'archive_location': {'type': 'string', 'minLength': 2}}}, 'observability': {'type': 'array', 'items': {'type': 'object', 'required': ['name', 'kind', 'disposition', 'target_or_change_url'], 'properties': {'name': {'type': 'string', 'minLength': 2}, 'kind': {'type': 'string', 'enum': ['alert', 'dashboard', 'slo', 'synthetic_check']}, 'disposition': {'type': 'string', 'enum': ['retargeted', 'deleted']}, 'target_or_change_url': {'type': 'string', 'minLength': 3}}}}, 'infrastructure': {'type': 'array', 'items': {'type': 'object', 'required': ['resource', 'kind', 'still_running', 'monthly_cost_removed'], 'properties': {'resource': {'type': 'string', 'minLength': 2}, 'kind': {'type': 'string', 'enum': ['instance', 'database', 'queue', 'dns_record', 'iam_role', 'service_account', 'secret', 'bucket', 'other']}, 'decommission_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'monthly_cost_removed': {'type': 'number', 'minimum': 0}, 'still_running': {'type': 'boolean'}, 'reason': {'type': 'string', 'minLength': 10}, 'end_date': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}, 'if': {'properties': {'still_running': {'const': True}}}, 'then': {'required': ['reason', 'end_date']}, 'else': {'required': ['decommission_date']}}}, 'deferred_items': {'type': 'array', 'items': {'type': 'object', 'required': ['item', 'ticket_url', 'owner'], 'properties': {'item': {'type': 'string', 'minLength': 3}, 'ticket_url': {'type': 'string', 'pattern': '^https?://'}, 'owner': {'type': 'string', 'minLength': 2}}}}, 'review': {'type': 'object', 'required': ['status', 'drop_or_decommission_executed_by_agent'], 'properties': {'status': {'type': 'string', 'enum': ['draft', 'ready_for_review', 'approved']}, 'reviewer': {'type': 'string', 'minLength': 2}, 'reviewer_read_snapshot_and_scan_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'drop_or_decommission_executed_by_agent': {'const': False}}, 'if': {'properties': {'status': {'const': 'approved'}}}, 'then': {'required': ['reviewer', 'reviewer_read_snapshot_and_scan_on']}}}}

OK = {'migration': {'name': 'orders-service: orders_v1 schema to orders_v2', 'legacy_component': 'orders_v1 (Postgres schema + /v1/orders endpoint)', 'new_component': 'orders_v2 schema + /v2/orders', 'cutover_date': '2026-04-01', 'parity_window': {'start': '2026-04-03', 'end': '2026-04-10', 'days': 8, 'includes_full_weekly_cycle': True}, 'delivery_cycle_days': 14, 'cleanup_deadline': '2026-04-24'}, 'dual_write': {'reconciliation_report_url': 'https://reports.acme.example/orders-reconciliation/2026-04-03_2026-04-10', 'consecutive_days_zero_mismatch': 8, 'mismatches': 0, 'legacy_write_removed_by': 'code_deletion', 'deletion_pr_url': 'https://github.com/acme/orders-service/pull/8812'}, 'legacy_read_path': {'counter_name': 'orders_v1_reads_total', 'zero_for_days': 9, 'includes_batch_window': True, 'evidence_url': 'https://grafana.acme.example/d/orders/v1-reads?from=2026-04-03&to=2026-04-12', 'deletion_pr_url': 'https://github.com/acme/orders-service/pull/8820'}, 'flags': [{'key': 'orders.dual_write', 'removal_pr_url': 'https://github.com/acme/orders-service/pull/8812', 'key_deleted_from_flag_service': True, 'branches_collapsed': True}, {'key': 'orders.read_from_v2', 'removal_pr_url': 'https://github.com/acme/orders-service/pull/8820', 'key_deleted_from_flag_service': True, 'branches_collapsed': True}, {'key': 'orders.v2_shadow_compare', 'removal_pr_url': 'https://github.com/acme/orders-service/pull/8821', 'key_deleted_from_flag_service': True, 'branches_collapsed': True}], 'shims': [{'name': '/v1/orders -> /v2/orders proxy', 'kind': 'endpoint_proxy', 'consumers': ['mobile-app <= 4.12 (2.1% of sessions)'], 'disposition': 'retained', 'removal_date': '2026-07-01', 'consumer_counter': 'orders_v1_proxy_requests_total{client="mobile"}'}, {'name': 'orders.customer_ref column alias', 'kind': 'column_alias', 'consumers': [], 'disposition': 'deleted_in_this_cleanup', 'deletion_pr_url': 'https://github.com/acme/orders-service/pull/8824'}], 'schema_drop': {'objects': ['schema orders_v1', 'index orders_v1_customer_idx'], 'separate_change_from_code_deletion': True, 'snapshot': {'url': 's3://acme-backups/orders_v1-2026-04-12.dump', 'retention_until': '2026-10-01'}, 'reference_scan': {'command': "gh search code 'orders_v1' --owner acme; grep -c orders_v1 /var/log/postgresql/slow.log", 'repositories_scanned': 41, 'query_log_searched': True, 'hits': 0}, 'drop_change_url': 'https://github.com/acme/orders-service/pull/8830'}, 'docs': {'search_command': "grep -ril 'orders_v1\\|/v1/orders' docs/ runbooks/ adr/", 'hits_before': 14, 'hits_after_outside_archive': 0, 'archive_location': 'docs/archive/orders-v1/'}, 'observability': [{'name': 'OrdersV1WriteErrors', 'kind': 'alert', 'disposition': 'deleted', 'target_or_change_url': 'https://github.com/acme/monitoring/pull/2210'}, {'name': 'Orders overview', 'kind': 'dashboard', 'disposition': 'retargeted', 'target_or_change_url': 'orders_v2_* metrics, https://github.com/acme/monitoring/pull/2211'}, {'name': 'orders-latency-slo', 'kind': 'slo', 'disposition': 'retargeted', 'target_or_change_url': 'http_request_duration_seconds{route="/v2/orders"}'}], 'infrastructure': [{'resource': 'orders-v1-reader replica (RDS)', 'kind': 'database', 'decommission_date': '2026-04-15', 'monthly_cost_removed': 420, 'still_running': False}, {'resource': 'orders-v1-sync SQS queue', 'kind': 'queue', 'decommission_date': '2026-04-14', 'monthly_cost_removed': 12, 'still_running': False}, {'resource': 'iam role orders-v1-writer', 'kind': 'iam_role', 'decommission_date': '2026-04-14', 'monthly_cost_removed': 0, 'still_running': False}, {'resource': 'orders-v1.internal DNS record', 'kind': 'dns_record', 'monthly_cost_removed': 0, 'still_running': True, 'reason': "mobile-app <= 4.12 resolves it for the proxy shim until the shim's removal date", 'end_date': '2026-07-01'}], 'deferred_items': [{'item': 'delete /v1/orders proxy shim and orders-v1.internal DNS record', 'ticket_url': 'https://jira.acme.example/browse/ORD-1188', 'owner': 'dana@acme.example'}], 'review': {'status': 'ready_for_review', 'reviewer': 'kim@acme.example', 'drop_or_decommission_executed_by_agent': False}}

BAD = {'migration': {'name': 'orders-service: orders_v1 schema to orders_v2', 'legacy_component': 'orders_v1', 'new_component': 'orders_v2', 'cutover_date': '2026-04-01', 'parity_window': {'start': '2026-04-01', 'end': '2026-04-03', 'days': 2, 'includes_full_weekly_cycle': False}, 'delivery_cycle_days': 90, 'cleanup_deadline': '2026-12-31'}, 'dual_write': {'reconciliation_report_url': 'https://reports.acme.example/orders-reconciliation/2026-04-01_2026-04-03', 'consecutive_days_zero_mismatch': 2, 'mismatches': 17, 'legacy_write_removed_by': 'flag_set_false', 'deletion_pr_url': 'https://github.com/acme/orders-service/pull/8812'}, 'legacy_read_path': {'counter_name': 'none', 'zero_for_days': 0, 'includes_batch_window': False, 'evidence_url': 'https://grafana.acme.example/d/orders', 'deletion_pr_url': 'https://github.com/acme/orders-service/pull/8820'}, 'flags': [{'key': 'orders.dual_write', 'removal_pr_url': 'https://github.com/acme/orders-service/pull/8812', 'key_deleted_from_flag_service': False, 'branches_collapsed': False}], 'shims': [{'name': '/v1/orders -> /v2/orders proxy', 'kind': 'endpoint_proxy', 'consumers': [], 'disposition': 'retained'}], 'schema_drop': {'objects': ['schema orders_v1'], 'separate_change_from_code_deletion': False, 'snapshot': {'url': 'none', 'retention_until': '2026-04-03'}, 'reference_scan': {'command': 'grep orders_v1 src/', 'repositories_scanned': 1, 'query_log_searched': False, 'hits': 3}, 'drop_change_url': 'https://github.com/acme/orders-service/pull/8812'}, 'docs': {'search_command': 'grep -ril orders_v1 docs/', 'hits_before': 14, 'hits_after_outside_archive': 9, 'archive_location': 'docs/archive/'}, 'observability': [], 'infrastructure': [{'resource': 'orders-v1-reader replica (RDS)', 'kind': 'database', 'monthly_cost_removed': 0, 'still_running': True}], 'deferred_items': [], 'review': {'status': 'approved', 'drop_or_decommission_executed_by_agent': True}}


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
        prog="validate-post-migration-cleanup.py",
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
