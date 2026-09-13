#!/usr/bin/env python3
"""validate-hipaa-phi-data-flow-design.py

Validate the PHI data-flow design produced by the hipaa-phi-data-flow-design methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/hipaa-phi-data-flow-design.json', 'title': 'HIPAA PHI data-flow design', 'type': 'object', 'required': ['system', 'hops', 'links', 'audit_log', 'log_scrubbing', 'deletion_propagation', 'media_disposal_procedure', 'review'], 'additionalProperties': False, 'definitions': {'identifier_class': {'type': 'string', 'enum': ['names', 'geographic_subdivisions_smaller_than_state', 'dates_except_year', 'phone_numbers', 'fax_numbers', 'email_addresses', 'social_security_numbers', 'medical_record_numbers', 'health_plan_beneficiary_numbers', 'account_numbers', 'certificate_license_numbers', 'vehicle_identifiers', 'device_identifiers', 'web_urls', 'ip_addresses', 'biometric_identifiers', 'full_face_photos', 'other_unique_identifying_number']}}, 'properties': {'system': {'type': 'string', 'minLength': 3}, 'hops': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['id', 'name', 'kind', 'operations', 'external', 'identifier_classes', 'fields', 'purpose', 'deidentified', 'access', 'retention'], 'properties': {'id': {'type': 'string', 'pattern': '^hop-[a-z0-9-]+$'}, 'name': {'type': 'string', 'minLength': 2}, 'kind': {'type': 'string', 'enum': ['service', 'database', 'queue', 'cache', 'search_index', 'log_pipeline', 'error_tracker', 'analytics', 'machine_learning', 'llm_or_embeddings_api', 'email_or_sms_gateway', 'support_desk', 'backup', 'export', 'object_storage', 'third_party_api', 'other']}, 'operations': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['stores', 'processes', 'transmits']}}, 'external': {'type': 'boolean'}, 'identifier_classes': {'type': 'array', 'uniqueItems': True, 'items': {'$ref': '#/definitions/identifier_class'}}, 'fields': {'type': 'array', 'items': {'type': 'object', 'required': ['name', 'justification'], 'properties': {'name': {'type': 'string', 'minLength': 1}, 'justification': {'type': 'string', 'minLength': 10}}}}, 'purpose': {'type': 'string', 'minLength': 10}, 'deidentified': {'type': 'boolean'}, 'deidentification_method': {'type': 'string', 'enum': ['safe_harbor_164_514_b_2', 'expert_determination_164_514_b_1']}, 'identified_use_documented_at': {'type': 'string', 'minLength': 3}, 'baa': {'type': 'object', 'required': ['executed', 'vendor', 'plan', 'covered_service', 'link'], 'properties': {'executed': {'const': True}, 'vendor': {'type': 'string', 'minLength': 2}, 'plan': {'type': 'string', 'minLength': 2}, 'covered_service': {'type': 'string', 'minLength': 2}, 'link': {'type': 'string', 'minLength': 3}, 'executed_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}}, 'encryption_at_rest': {'type': 'object', 'required': ['enabled', 'kms', 'key_rotation_enabled'], 'properties': {'enabled': {'const': True}, 'standard': {'type': 'string'}, 'kms': {'type': 'string', 'minLength': 3}, 'key_rotation_enabled': {'const': True}}}, 'access': {'type': 'object', 'required': ['roles', 'shared_accounts', 'auto_logoff_minutes', 'break_glass'], 'properties': {'roles': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['role', 'operations'], 'properties': {'role': {'type': 'string', 'minLength': 2}, 'operations': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'enum': ['read', 'write', 'export', 'delete', 'admin']}}}}}, 'shared_accounts': {'const': False}, 'auto_logoff_minutes': {'type': 'integer', 'minimum': 1}, 'break_glass': {'type': 'object', 'required': ['documented_at', 'audit_alert'], 'properties': {'documented_at': {'type': 'string', 'minLength': 3}, 'audit_alert': {'type': 'string', 'minLength': 3}}}}}, 'retention': {'type': 'object', 'required': ['period_days', 'deletion_mechanism'], 'properties': {'period_days': {'type': 'integer', 'minimum': 0}, 'deletion_mechanism': {'type': 'string', 'minLength': 5}}}}, 'allOf': [{'if': {'properties': {'operations': {'contains': {'const': 'stores'}}}}, 'then': {'required': ['encryption_at_rest']}}, {'if': {'properties': {'deidentified': {'const': True}}}, 'then': {'required': ['deidentification_method']}}, {'if': {'properties': {'external': {'const': True}, 'deidentified': {'const': False}}}, 'then': {'required': ['baa']}}, {'if': {'properties': {'kind': {'enum': ['analytics', 'machine_learning', 'llm_or_embeddings_api']}, 'deidentified': {'const': False}}}, 'then': {'required': ['baa', 'identified_use_documented_at']}}, {'if': {'properties': {'deidentified': {'const': False}}}, 'then': {'properties': {'identifier_classes': {'minItems': 1}, 'fields': {'minItems': 1}}}}]}}, 'links': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['from', 'to', 'tls_version', 'tls_terminates_at', 'identifier_classes'], 'properties': {'from': {'type': 'string', 'pattern': '^hop-[a-z0-9-]+$'}, 'to': {'type': 'string', 'pattern': '^hop-[a-z0-9-]+$'}, 'tls_version': {'type': 'string', 'enum': ['1.2', '1.3']}, 'tls_terminates_at': {'type': 'string', 'minLength': 2}, 'identifier_classes': {'type': 'array', 'uniqueItems': True, 'items': {'$ref': '#/definitions/identifier_class'}}}}}, 'audit_log': {'type': 'object', 'required': ['store', 'append_only', 'contains_phi_field_values', 'retention_years', 'event_fields', 'bulk_access_alert'], 'properties': {'store': {'type': 'string', 'minLength': 3}, 'append_only': {'const': True}, 'contains_phi_field_values': {'const': False}, 'retention_years': {'type': 'integer', 'minimum': 6}, 'event_fields': {'type': 'array', 'uniqueItems': True, 'allOf': [{'contains': {'const': 'identity'}}, {'contains': {'const': 'timestamp'}}, {'contains': {'const': 'record_id'}}, {'contains': {'const': 'action'}}, {'contains': {'const': 'originating_system'}}], 'items': {'type': 'string'}}, 'bulk_access_alert': {'type': 'string', 'minLength': 3}}}, 'log_scrubbing': {'type': 'object', 'required': ['allow_list_scrubber_at', 'phi_in_urls_or_query_strings', 'synthetic_record_test'], 'properties': {'allow_list_scrubber_at': {'type': 'string', 'minLength': 3}, 'phi_in_urls_or_query_strings': {'const': False}, 'synthetic_record_test': {'type': 'object', 'required': ['path', 'covers_every_request_path', 'asserts_no_identifier_in_logs_errors_traces', 'runs_in_ci'], 'properties': {'path': {'type': 'string', 'minLength': 3}, 'covers_every_request_path': {'const': True}, 'asserts_no_identifier_in_logs_errors_traces': {'const': True}, 'runs_in_ci': {'const': True}}}}}, 'deletion_propagation': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['trigger', 'propagates_to', 'mechanism'], 'properties': {'trigger': {'type': 'string', 'minLength': 5}, 'propagates_to': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'pattern': '^hop-[a-z0-9-]+$'}}, 'mechanism': {'type': 'string', 'minLength': 5}}}}, 'media_disposal_procedure': {'type': 'string', 'minLength': 5}, 'review': {'type': 'object', 'required': ['status', 'approved_by_agent'], 'properties': {'status': {'type': 'string', 'enum': ['draft', 'ready_for_review', 'approved']}, 'security_officer': {'type': 'string', 'minLength': 3}, 'signed_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'approved_by_agent': {'const': False}}, 'if': {'properties': {'status': {'const': 'approved'}}}, 'then': {'required': ['security_officer', 'signed_on']}}}}

OK = {'system': 'careportal-api', 'hops': [{'id': 'hop-api', 'name': 'careportal-api (FastAPI)', 'kind': 'service', 'operations': ['processes', 'transmits'], 'external': False, 'identifier_classes': ['names', 'dates_except_year', 'medical_record_numbers', 'email_addresses'], 'fields': [{'name': 'patient.name', 'justification': 'shown on the encounter screen the clinician is authorised to view'}, {'name': 'patient.mrn', 'justification': 'record lookup key'}, {'name': 'encounter.date', 'justification': 'encounter timeline'}, {'name': 'patient.email', 'justification': 'appointment reminders'}], 'purpose': 'serve clinician encounter views and appointment scheduling', 'deidentified': False, 'access': {'roles': [{'role': 'clinician', 'operations': ['read', 'write']}, {'role': 'scheduler', 'operations': ['read']}], 'shared_accounts': False, 'auto_logoff_minutes': 15, 'break_glass': {'documented_at': 'runbooks/break-glass.md', 'audit_alert': 'pagerduty:phi-break-glass'}}, 'retention': {'period_days': 0, 'deletion_mechanism': 'stateless; no PHI persisted in the service'}}, {'id': 'hop-postgres', 'name': 'patients PostgreSQL (RDS)', 'kind': 'database', 'operations': ['stores'], 'external': False, 'identifier_classes': ['names', 'dates_except_year', 'medical_record_numbers', 'email_addresses', 'phone_numbers'], 'fields': [{'name': 'patients.*', 'justification': 'system of record for the patient chart'}], 'purpose': 'system of record', 'deidentified': False, 'encryption_at_rest': {'enabled': True, 'standard': 'NIST SP 800-111', 'kms': 'aws-kms:alias/careportal-phi', 'key_rotation_enabled': True}, 'access': {'roles': [{'role': 'api-service-principal', 'operations': ['read', 'write', 'delete']}, {'role': 'dba', 'operations': ['admin']}], 'shared_accounts': False, 'auto_logoff_minutes': 10, 'break_glass': {'documented_at': 'runbooks/break-glass.md', 'audit_alert': 'pagerduty:phi-break-glass'}}, 'retention': {'period_days': 2190, 'deletion_mechanism': 'nightly job deletes rows past retention and on patient deletion request; cascades to encounters'}}, {'id': 'hop-backup', 'name': 'RDS snapshots to S3', 'kind': 'backup', 'operations': ['stores'], 'external': False, 'identifier_classes': ['names', 'dates_except_year', 'medical_record_numbers', 'email_addresses', 'phone_numbers'], 'fields': [{'name': 'full snapshot', 'justification': 'disaster recovery of the system of record'}], 'purpose': 'disaster recovery', 'deidentified': False, 'encryption_at_rest': {'enabled': True, 'standard': 'NIST SP 800-111', 'kms': 'aws-kms:alias/careportal-phi', 'key_rotation_enabled': True}, 'access': {'roles': [{'role': 'sre', 'operations': ['read', 'admin']}], 'shared_accounts': False, 'auto_logoff_minutes': 10, 'break_glass': {'documented_at': 'runbooks/break-glass.md', 'audit_alert': 'pagerduty:phi-break-glass'}}, 'retention': {'period_days': 35, 'deletion_mechanism': 'S3 lifecycle rule expires snapshots at 35 days; deletion requests replay against restored snapshots per runbooks/deletion.md'}}, {'id': 'hop-error-tracker', 'name': 'Sentry (Business plan, HIPAA add-on)', 'kind': 'error_tracker', 'operations': ['stores', 'processes'], 'external': True, 'identifier_classes': ['medical_record_numbers'], 'fields': [{'name': 'request.path with mrn', 'justification': 'needed to reproduce failures on a specific record; body and headers scrubbed'}], 'purpose': 'error triage', 'deidentified': False, 'baa': {'executed': True, 'vendor': 'Sentry', 'plan': 'Business', 'covered_service': 'Error Monitoring with PII scrubbing enabled', 'link': 'contracts/sentry-baa-2026-01.pdf', 'executed_on': '2026-01-14'}, 'encryption_at_rest': {'enabled': True, 'kms': 'vendor-managed per BAA section 4', 'key_rotation_enabled': True}, 'access': {'roles': [{'role': 'on-call-engineer', 'operations': ['read']}], 'shared_accounts': False, 'auto_logoff_minutes': 30, 'break_glass': {'documented_at': 'runbooks/break-glass.md', 'audit_alert': 'pagerduty:phi-break-glass'}}, 'retention': {'period_days': 30, 'deletion_mechanism': 'vendor retention set to 30 days; per-event deletion API called on deletion request'}}, {'id': 'hop-embeddings', 'name': 'Hosted embeddings API for note search', 'kind': 'llm_or_embeddings_api', 'operations': ['processes'], 'external': True, 'identifier_classes': [], 'fields': [{'name': 'note.text_deidentified', 'justification': 'semantic search over clinical notes; all 18 identifiers removed before the call'}], 'purpose': 'semantic search over clinical notes', 'deidentified': True, 'deidentification_method': 'safe_harbor_164_514_b_2', 'access': {'roles': [{'role': 'search-service-principal', 'operations': ['write']}], 'shared_accounts': False, 'auto_logoff_minutes': 5, 'break_glass': {'documented_at': 'runbooks/break-glass.md', 'audit_alert': 'pagerduty:phi-break-glass'}}, 'retention': {'period_days': 0, 'deletion_mechanism': 'vendor zero-retention endpoint; nothing persisted'}}], 'links': [{'from': 'hop-api', 'to': 'hop-postgres', 'tls_version': '1.2', 'tls_terminates_at': 'RDS endpoint (rds.force_ssl=1)', 'identifier_classes': ['names', 'dates_except_year', 'medical_record_numbers', 'email_addresses', 'phone_numbers']}, {'from': 'hop-postgres', 'to': 'hop-backup', 'tls_version': '1.2', 'tls_terminates_at': 'S3 endpoint', 'identifier_classes': ['names', 'dates_except_year', 'medical_record_numbers', 'email_addresses', 'phone_numbers']}, {'from': 'hop-api', 'to': 'hop-error-tracker', 'tls_version': '1.3', 'tls_terminates_at': 'sentry.io ingest', 'identifier_classes': ['medical_record_numbers']}, {'from': 'hop-api', 'to': 'hop-embeddings', 'tls_version': '1.3', 'tls_terminates_at': 'vendor API gateway', 'identifier_classes': []}], 'audit_log': {'store': 'CloudWatch Logs group /careportal/phi-audit with retention lock', 'append_only': True, 'contains_phi_field_values': False, 'retention_years': 7, 'event_fields': ['identity', 'timestamp', 'record_id', 'action', 'originating_system'], 'bulk_access_alert': 'CloudWatch alarm: >200 distinct record_ids read by one identity in 10 minutes -> pagerduty:phi-bulk-access'}, 'log_scrubbing': {'allow_list_scrubber_at': 'careportal/logging/scrubber.py (allow-list of 14 safe keys)', 'phi_in_urls_or_query_strings': False, 'synthetic_record_test': {'path': 'tests/compliance/test_no_phi_in_logs.py', 'covers_every_request_path': True, 'asserts_no_identifier_in_logs_errors_traces': True, 'runs_in_ci': True}}, 'deletion_propagation': [{'trigger': 'patient deletion request or retention expiry in hop-postgres', 'propagates_to': ['hop-backup', 'hop-error-tracker'], 'mechanism': 'deletion job writes a tombstone; backup restore replays tombstones (runbooks/deletion.md); Sentry per-event deletion API by mrn'}], 'media_disposal_procedure': 'runbooks/media-disposal.md: NIST SP 800-88 purge for any drive or device that held PHI; cloud volumes are KMS-encrypted and keys are destroyed on decommission', 'review': {'status': 'ready_for_review', 'security_officer': 'security-officer@careportal.example', 'approved_by_agent': False}}

BAD = {'system': 'careportal-api', 'hops': [{'id': 'hop-api', 'name': 'careportal-api (FastAPI)', 'kind': 'service', 'operations': ['processes', 'transmits'], 'external': False, 'identifier_classes': ['names', 'medical_record_numbers'], 'fields': [{'name': 'patient.*', 'justification': 'everything, simpler than selecting columns'}], 'purpose': 'serve clinician encounter views', 'deidentified': False, 'access': {'roles': [{'role': 'ops', 'operations': ['admin']}], 'shared_accounts': True, 'auto_logoff_minutes': 0, 'break_glass': {'documented_at': 'runbooks/break-glass.md', 'audit_alert': 'pagerduty:phi-break-glass'}}, 'retention': {'period_days': 0, 'deletion_mechanism': 'stateless'}}, {'id': 'hop-postgres', 'name': 'patients PostgreSQL (RDS)', 'kind': 'database', 'operations': ['stores'], 'external': False, 'identifier_classes': ['names', 'medical_record_numbers'], 'fields': [{'name': 'patients.*', 'justification': 'system of record for the patient chart'}], 'purpose': 'system of record', 'deidentified': False, 'access': {'roles': [{'role': 'api-service-principal', 'operations': ['read', 'write']}], 'shared_accounts': False, 'auto_logoff_minutes': 10, 'break_glass': {'documented_at': 'runbooks/break-glass.md', 'audit_alert': 'pagerduty:phi-break-glass'}}, 'retention': {'period_days': 2190, 'deletion_mechanism': 'nightly job deletes rows past retention'}}, {'id': 'hop-embeddings', 'name': 'Hosted embeddings API for note search', 'kind': 'llm_or_embeddings_api', 'operations': ['processes'], 'external': True, 'identifier_classes': ['names', 'medical_record_numbers', 'dates_except_year'], 'fields': [{'name': 'note.text', 'justification': 'full clinical note for semantic search'}], 'purpose': 'semantic search over clinical notes', 'deidentified': False, 'access': {'roles': [{'role': 'search-service-principal', 'operations': ['write']}], 'shared_accounts': False, 'auto_logoff_minutes': 5, 'break_glass': {'documented_at': 'runbooks/break-glass.md', 'audit_alert': 'pagerduty:phi-break-glass'}}, 'retention': {'period_days': 30, 'deletion_mechanism': 'vendor default'}}], 'links': [{'from': 'hop-api', 'to': 'hop-postgres', 'tls_version': '1.0', 'tls_terminates_at': 'load balancer only; plaintext inside the VPC', 'identifier_classes': ['names', 'medical_record_numbers']}, {'from': 'hop-api', 'to': 'hop-embeddings', 'tls_version': '1.3', 'tls_terminates_at': 'vendor API gateway', 'identifier_classes': ['names', 'medical_record_numbers', 'dates_except_year']}], 'audit_log': {'store': 'application log', 'append_only': False, 'contains_phi_field_values': True, 'retention_years': 1, 'event_fields': ['timestamp', 'action'], 'bulk_access_alert': 'none'}, 'log_scrubbing': {'allow_list_scrubber_at': 'none', 'phi_in_urls_or_query_strings': True, 'synthetic_record_test': {'path': 'tests/compliance/test_no_phi_in_logs.py', 'covers_every_request_path': False, 'asserts_no_identifier_in_logs_errors_traces': True, 'runs_in_ci': False}}, 'deletion_propagation': [], 'media_disposal_procedure': 'n/a', 'review': {'status': 'approved', 'approved_by_agent': True}}


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
        prog="validate-hipaa-phi-data-flow-design.py",
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
