#!/usr/bin/env python3
"""validate-ios-signing-and-provisioning.py

Validate the signing document produced by the ios-signing-and-provisioning methodology against the
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/ios-signing-and-provisioning.json', 'title': 'iOS signing and provisioning document', 'type': 'object', 'required': ['app', 'secret_store', 'private_keys_outside_secret_store', 'certificates', 'profiles', 'asc_api_keys', 'push', 'build_configs', 'rotation_calendar', 'revocation_runbook', 'review'], 'additionalProperties': False, 'properties': {'app': {'type': 'object', 'required': ['name', 'bundle_id', 'built_for_client', 'owning_account', 'owning_team_id'], 'properties': {'name': {'type': 'string', 'minLength': 1}, 'bundle_id': {'type': 'string', 'pattern': '^[A-Za-z0-9.-]+\\.[A-Za-z0-9-]+$'}, 'built_for_client': {'type': 'boolean'}, 'owning_account': {'type': 'string', 'enum': ['client', 'agency', 'own']}, 'owning_team_id': {'type': 'string', 'pattern': '^[A-Z0-9]{10}$'}, 'agency_role_on_client_account': {'type': 'string', 'enum': ['Admin', 'App Manager', 'Developer', 'Marketing', 'Customer Support']}, 'transfer_plan': {'type': 'string', 'minLength': 10}}, 'if': {'properties': {'built_for_client': {'const': True}}}, 'then': {'anyOf': [{'properties': {'owning_account': {'const': 'client'}}, 'required': ['agency_role_on_client_account']}, {'properties': {'owning_account': {'const': 'agency'}}, 'required': ['transfer_plan']}]}}, 'secret_store': {'type': 'object', 'required': ['kind', 'location', 'readers'], 'properties': {'kind': {'type': 'string', 'enum': ['ci_secrets', 'fastlane_match', 'password_manager']}, 'location': {'type': 'string', 'minLength': 3}, 'readers': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 2}}}}, 'private_keys_outside_secret_store': {'const': False}, 'certificates': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['type', 'identifier', 'expiry', 'storage_location', 'shared_by_team'], 'properties': {'type': {'type': 'string', 'enum': ['development', 'distribution', 'apns']}, 'identifier': {'type': 'string', 'minLength': 4}, 'expiry': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'storage_location': {'type': 'string', 'minLength': 3}, 'shared_by_team': {'type': 'boolean'}, 'per_developer_reason': {'type': 'string', 'minLength': 10}}, 'if': {'properties': {'type': {'const': 'distribution'}, 'shared_by_team': {'const': False}}}, 'then': {'required': ['per_developer_reason']}}}, 'profiles': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['name', 'bundle_id', 'type', 'uuid', 'expiry', 'storage_location'], 'properties': {'name': {'type': 'string', 'minLength': 1}, 'bundle_id': {'type': 'string', 'minLength': 3}, 'type': {'type': 'string', 'enum': ['development', 'ad_hoc', 'app_store', 'enterprise']}, 'uuid': {'type': 'string', 'minLength': 8}, 'expiry': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'storage_location': {'type': 'string', 'minLength': 3}}}}, 'asc_api_keys': {'type': 'array', 'items': {'type': 'object', 'required': ['key_id', 'issuer_id', 'role', 'used_by', 'p8_storage_location', 'p8_stored_at_issue'], 'properties': {'key_id': {'type': 'string', 'pattern': '^[A-Z0-9]{10}$'}, 'issuer_id': {'type': 'string', 'minLength': 8}, 'role': {'type': 'string', 'enum': ['Developer', 'App Manager']}, 'used_by': {'type': 'string', 'minLength': 2}, 'p8_storage_location': {'type': 'string', 'minLength': 3}, 'p8_stored_at_issue': {'const': True}}}}, 'push': {'type': 'object', 'required': ['auth'], 'properties': {'auth': {'type': 'string', 'enum': ['token_key', 'certificate']}, 'key_id': {'type': 'string', 'pattern': '^[A-Z0-9]{10}$'}, 'team_id': {'type': 'string', 'pattern': '^[A-Z0-9]{10}$'}, 'p8_storage_location': {'type': 'string', 'minLength': 3}, 'certificate_constraint': {'type': 'string', 'minLength': 10}, 'certificate_expiry': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}}, 'allOf': [{'if': {'properties': {'auth': {'const': 'token_key'}}}, 'then': {'required': ['key_id', 'team_id', 'p8_storage_location']}}, {'if': {'properties': {'auth': {'const': 'certificate'}}}, 'then': {'required': ['certificate_constraint', 'certificate_expiry']}}]}, 'build_configs': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['name', 'aps_environment', 'apns_host'], 'properties': {'name': {'type': 'string', 'enum': ['debug', 'testflight', 'app_store', 'ad_hoc', 'enterprise']}, 'aps_environment': {'type': 'string', 'enum': ['development', 'production']}, 'apns_host': {'type': 'string', 'enum': ['api.sandbox.push.apple.com', 'api.push.apple.com']}}, 'allOf': [{'if': {'properties': {'aps_environment': {'const': 'development'}}}, 'then': {'properties': {'apns_host': {'const': 'api.sandbox.push.apple.com'}}}}, {'if': {'properties': {'aps_environment': {'const': 'production'}}}, 'then': {'properties': {'apns_host': {'const': 'api.push.apple.com'}}}}]}}, 'rotation_calendar': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['asset', 'expiry', 'rotate_by', 'lead_days', 'owner'], 'properties': {'asset': {'type': 'string', 'minLength': 4}, 'expiry': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'rotate_by': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'lead_days': {'type': 'integer', 'minimum': 30}, 'owner': {'type': 'string', 'minLength': 3}}}}, 'revocation_runbook': {'type': 'object', 'required': ['who_may_revoke', 'impact', 'regeneration_order', 'verified_against'], 'properties': {'who_may_revoke': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 3}}, 'impact': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['certificate_type', 'installed_builds', 'pipelines_broken'], 'properties': {'certificate_type': {'type': 'string', 'enum': ['development', 'distribution_app_store', 'distribution_ad_hoc', 'distribution_enterprise', 'apns']}, 'installed_builds': {'type': 'string', 'enum': ['keep_launching', 'stop_launching', 'not_applicable']}, 'pipelines_broken': {'type': 'array', 'items': {'type': 'string'}}}}}, 'regeneration_order': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 3}}, 'verified_against': {'type': 'string', 'pattern': '^https://developer\\.apple\\.com/'}}}, 'review': {'type': 'object', 'required': ['status', 'binding_action_performed_by_agent'], 'properties': {'status': {'type': 'string', 'enum': ['draft', 'ready_for_review', 'approved']}, 'reviewer': {'type': 'string', 'minLength': 3}, 'approved_on': {'type': 'string', 'pattern': '^\\d{4}-\\d{2}-\\d{2}$'}, 'binding_action_performed_by_agent': {'const': False}}, 'if': {'properties': {'status': {'const': 'approved'}}}, 'then': {'required': ['reviewer', 'approved_on']}}}}

OK = {'app': {'name': 'Northwind Field', 'bundle_id': 'com.northwind.field', 'built_for_client': True, 'owning_account': 'client', 'owning_team_id': 'A1B2C3D4E5', 'agency_role_on_client_account': 'App Manager'}, 'secret_store': {'kind': 'fastlane_match', 'location': 'git@github.com:northwind/ios-certificates.git (match, encrypted)', 'readers': ['ci:github-actions/northwind-field', 'maria@agency.example', 'release-lead@northwind.example']}, 'private_keys_outside_secret_store': False, 'certificates': [{'type': 'distribution', 'identifier': 'Apple Distribution: Northwind Ltd (A1B2C3D4E5), serial 6F3A9C2E', 'expiry': '2027-02-14', 'storage_location': 'match: certs/distribution/6F3A9C2E.p12', 'shared_by_team': True}, {'type': 'development', 'identifier': 'Apple Development: CI (A1B2C3D4E5), serial 1D8B44A0', 'expiry': '2027-02-14', 'storage_location': 'match: certs/development/1D8B44A0.p12', 'shared_by_team': True}], 'profiles': [{'name': 'match AppStore com.northwind.field', 'bundle_id': 'com.northwind.field', 'type': 'app_store', 'uuid': 'c4d1a2e6-7f3b-4a9c-9d2e-0b1f5a6c7d8e', 'expiry': '2027-02-14', 'storage_location': 'match: profiles/appstore/'}, {'name': 'match Development com.northwind.field', 'bundle_id': 'com.northwind.field', 'type': 'development', 'uuid': '9a8b7c6d-5e4f-4a3b-8c2d-1e0f9a8b7c6d', 'expiry': '2027-02-14', 'storage_location': 'match: profiles/development/'}], 'asc_api_keys': [{'key_id': 'K7M2P9Q4RS', 'issuer_id': '69a6de8e-1234-47e3-e053-5b8c7c11a4d1', 'role': 'App Manager', 'used_by': 'github-actions/northwind-field upload-testflight', 'p8_storage_location': 'GitHub Actions secret ASC_KEY_P8 (org: northwind)', 'p8_stored_at_issue': True}], 'push': {'auth': 'token_key', 'key_id': 'T3N8V5W2XY', 'team_id': 'A1B2C3D4E5', 'p8_storage_location': 'backend vault: secret/apns/northwind-field.p8'}, 'build_configs': [{'name': 'debug', 'aps_environment': 'development', 'apns_host': 'api.sandbox.push.apple.com'}, {'name': 'testflight', 'aps_environment': 'production', 'apns_host': 'api.push.apple.com'}, {'name': 'app_store', 'aps_environment': 'production', 'apns_host': 'api.push.apple.com'}], 'rotation_calendar': [{'asset': 'Apple Distribution serial 6F3A9C2E', 'expiry': '2027-02-14', 'rotate_by': '2027-01-10', 'lead_days': 35, 'owner': 'maria@agency.example'}, {'asset': 'Apple Development serial 1D8B44A0', 'expiry': '2027-02-14', 'rotate_by': '2027-01-10', 'lead_days': 35, 'owner': 'maria@agency.example'}, {'asset': 'profile c4d1a2e6 (App Store)', 'expiry': '2027-02-14', 'rotate_by': '2027-01-10', 'lead_days': 35, 'owner': 'maria@agency.example'}, {'asset': 'profile 9a8b7c6d (Development)', 'expiry': '2027-02-14', 'rotate_by': '2027-01-10', 'lead_days': 35, 'owner': 'maria@agency.example'}], 'revocation_runbook': {'who_may_revoke': ['release-lead@northwind.example', 'maria@agency.example'], 'impact': [{'certificate_type': 'distribution_app_store', 'installed_builds': 'keep_launching', 'pipelines_broken': ['github-actions/northwind-field release']}, {'certificate_type': 'development', 'installed_builds': 'stop_launching', 'pipelines_broken': ['github-actions/northwind-field pr-build']}, {'certificate_type': 'apns', 'installed_builds': 'not_applicable', 'pipelines_broken': ['backend push sender']}], 'regeneration_order': ['revoke in the portal', 'fastlane match nuke <type> then match <type>', 'regenerate profiles for the bundle id', 'rotate CI secrets', 'run a TestFlight build and a push smoke test'], 'verified_against': 'https://developer.apple.com/help/account/certificates/revoke-a-certificate/'}, 'review': {'status': 'ready_for_review', 'reviewer': 'release-lead@northwind.example', 'binding_action_performed_by_agent': False}}

BAD = {'app': {'name': 'Northwind Field', 'bundle_id': 'com.northwind.field', 'built_for_client': True, 'owning_account': 'agency', 'owning_team_id': 'Z9Y8X7W6V5'}, 'secret_store': {'kind': 'password_manager', 'location': '1Password vault iOS', 'readers': ['maria@agency.example']}, 'private_keys_outside_secret_store': True, 'certificates': [{'type': 'distribution', 'identifier': 'Apple Distribution: Agency (Z9Y8X7W6V5), serial 0AAA1111', 'expiry': '2026-09-20', 'storage_location': 'repo: ios/certs/dist.p12', 'shared_by_team': False}, {'type': 'distribution', 'identifier': 'Apple Distribution: Agency (Z9Y8X7W6V5), serial 0BBB2222', 'expiry': '2026-11-02', 'storage_location': 'Slack thread #ios-release', 'shared_by_team': False}], 'profiles': [{'name': 'Northwind AppStore', 'bundle_id': 'com.northwind.field', 'type': 'app_store', 'uuid': 'c4d1a2e6-7f3b-4a9c-9d2e-0b1f5a6c7d8e', 'expiry': '2026-09-20', 'storage_location': 'ask Maria'}], 'asc_api_keys': [{'key_id': 'K7M2P9Q4RS', 'issuer_id': '69a6de8e-1234-47e3-e053-5b8c7c11a4d1', 'role': 'Admin', 'used_by': 'all pipelines and the analytics vendor', 'p8_storage_location': "Maria's laptop", 'p8_stored_at_issue': False}], 'push': {'auth': 'certificate'}, 'build_configs': [{'name': 'testflight', 'aps_environment': 'production', 'apns_host': 'api.sandbox.push.apple.com'}], 'rotation_calendar': [{'asset': 'Apple Distribution serial 0AAA1111', 'expiry': '2026-09-20', 'rotate_by': '2026-09-18', 'lead_days': 2, 'owner': 'someone on the team'}], 'revocation_runbook': {'who_may_revoke': ['anyone in Xcode'], 'impact': [], 'regeneration_order': [], 'verified_against': 'https://someblog.example/ios-signing'}, 'review': {'status': 'approved', 'binding_action_performed_by_agent': True}}


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
        prog="validate-ios-signing-and-provisioning.py",
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
