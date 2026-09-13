#!/usr/bin/env python3
"""validate-multi-region-failover-pattern-pack.py

Validate a multi-region failover pattern pack against the JSON Schema (draft-07) embedded in
content/02-output-contract.xml of the multi-region-failover-pattern-pack methodology, plus the
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
 '$id': 'https://faion.net/schemas/multi-region-failover-pattern-pack.json',
 'title': 'Multi-region failover pattern pack',
 'type': 'object',
 'required': ['workload',
              'owner',
              'inputs',
              'pattern',
              'dns',
              'database',
              'object_store',
              'dependencies',
              'drill',
              'failback',
              'decision',
              'evidence',
              'review'],
 'additionalProperties': False,
 'definitions': {'handle': {'type': 'string', 'pattern': '^[a-z-]+:[a-z0-9._-]+$'},
                 'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'},
                 'text': {'type': 'string', 'minLength': 8}},
 'properties': {'__faion_header__': {'type': 'object'},
                'workload': {'type': 'object',
                             'required': ['name', 'tier', 'business_owner'],
                             'additionalProperties': False,
                             'properties': {'name': {'type': 'string', 'minLength': 2},
                                            'tier': {'type': 'string',
                                                     'enum': ['tier-0',
                                                              'tier-1',
                                                              'tier-2',
                                                              'tier-3']},
                                            'business_owner': {'$ref': '#/definitions/handle'}}},
                'owner': {'$ref': '#/definitions/handle'},
                'inputs': {'type': 'array',
                           'minItems': 2,
                           'allOf': [{'contains': {'properties': {'name': {'const': 'rpo_minutes'}}}},
                                     {'contains': {'properties': {'name': {'const': 'rto_minutes'}}}}],
                           'items': {'type': 'object',
                                     'required': ['name', 'value'],
                                     'additionalProperties': False,
                                     'properties': {'name': {'type': 'string',
                                                             'enum': ['rpo_minutes',
                                                                      'rto_minutes',
                                                                      'primary_region',
                                                                      'secondary_region']},
                                                    'value': {}},
                                     'allOf': [{'if': {'properties': {'name': {'enum': ['rpo_minutes',
                                                                                        'rto_minutes']}}},
                                                'then': {'properties': {'value': {'type': 'integer',
                                                                                  'minimum': 0}}}},
                                               {'if': {'properties': {'name': {'enum': ['primary_region',
                                                                                        'secondary_region']}}},
                                                'then': {'properties': {'value': {'type': 'string',
                                                                                  'minLength': 3}}}}]}},
                'pattern': {'type': 'object',
                            'required': ['chosen',
                                         'achievable_rpo_minutes',
                                         'achievable_rto_minutes',
                                         'secondary_capacity'],
                            'additionalProperties': False,
                            'properties': {'chosen': {'type': 'string',
                                                      'enum': ['backup-and-restore',
                                                               'pilot-light',
                                                               'warm-standby',
                                                               'active-passive-hot-standby',
                                                               'active-active']},
                                           'achievable_rpo_minutes': {'type': 'integer',
                                                                      'minimum': 0},
                                           'achievable_rto_minutes': {'type': 'integer',
                                                                      'minimum': 0},
                                           'secondary_capacity': {'type': 'object',
                                                                  'required': ['mode',
                                                                               'percent_of_primary',
                                                                               'quotas_verified'],
                                                                  'additionalProperties': False,
                                                                  'properties': {'mode': {'type': 'string',
                                                                                          'enum': ['pre-provisioned',
                                                                                                   'scale-up']},
                                                                                 'percent_of_primary': {'type': 'integer',
                                                                                                        'minimum': 0,
                                                                                                        'maximum': 200},
                                                                                 'scale_up_minutes': {'type': 'integer',
                                                                                                      'minimum': 0},
                                                                                 'quotas_verified': {'type': 'boolean',
                                                                                                     'const': True}},
                                                                  'if': {'properties': {'mode': {'const': 'scale-up'}}},
                                                                  'then': {'required': ['scale_up_minutes']}}}},
                'dns': {'type': 'object',
                        'required': ['mechanism', 'ttl_ignoring_clients'],
                        'additionalProperties': False,
                        'properties': {'mechanism': {'type': 'string',
                                                     'enum': ['dns-failover',
                                                              'global-load-balancer',
                                                              'anycast',
                                                              'none']},
                                       'ttl_seconds': {'type': 'integer',
                                                       'minimum': 1,
                                                       'maximum': 60},
                                       'health_check': {'type': 'object',
                                                        'required': ['endpoint',
                                                                     'interval_seconds',
                                                                     'failure_threshold'],
                                                        'additionalProperties': False,
                                                        'properties': {'endpoint': {'type': 'string',
                                                                                    'minLength': 4},
                                                                       'interval_seconds': {'type': 'integer',
                                                                                            'minimum': 1},
                                                                       'failure_threshold': {'type': 'integer',
                                                                                             'minimum': 1}}},
                                       'observed_propagation_seconds': {'type': 'integer',
                                                                        'minimum': 0},
                                       'ttl_ignoring_clients': {'type': 'array',
                                                                'items': {'type': 'object',
                                                                          'required': ['client',
                                                                                       'fallback'],
                                                                          'additionalProperties': False,
                                                                          'properties': {'client': {'type': 'string',
                                                                                                    'minLength': 2},
                                                                                         'fallback': {'type': 'string',
                                                                                                      'enum': ['global-load-balancer',
                                                                                                               'anycast',
                                                                                                               'client-side-retry-to-secondary']}}}}},
                        'if': {'properties': {'mechanism': {'const': 'dns-failover'}}},
                        'then': {'required': ['ttl_seconds',
                                              'health_check',
                                              'observed_propagation_seconds']}},
                'database': {'type': 'object',
                             'required': ['engine',
                                          'replication',
                                          'p99_lag_seconds_30d',
                                          'promotion_procedure',
                                          'fencing',
                                          'single_writer_enforcement'],
                             'additionalProperties': False,
                             'properties': {'engine': {'type': 'string', 'minLength': 2},
                                            'replication': {'type': 'string',
                                                            'enum': ['synchronous',
                                                                     'asynchronous']},
                                            'p99_lag_seconds_30d': {'type': 'number', 'minimum': 0},
                                            'promotion_procedure': {'$ref': '#/definitions/text'},
                                            'fencing': {'$ref': '#/definitions/text'},
                                            'single_writer_enforcement': {'$ref': '#/definitions/text'}}},
                'object_store': {'type': 'object',
                                 'required': ['provider',
                                              'replication_enabled',
                                              'versioning',
                                              'backlog_metric',
                                              'replication_time_alert',
                                              'existing_objects_backfilled'],
                                 'additionalProperties': False,
                                 'properties': {'provider': {'type': 'string', 'minLength': 2},
                                                'replication_enabled': {'type': 'boolean',
                                                                        'const': True},
                                                'versioning': {'type': 'boolean', 'const': True},
                                                'backlog_metric': {'type': 'string',
                                                                   'minLength': 4},
                                                'replication_time_alert': {'type': 'string',
                                                                           'minLength': 4},
                                                'existing_objects_backfilled': {'type': 'boolean'},
                                                'backfill_job': {'type': 'string', 'minLength': 4}},
                                 'if': {'properties': {'existing_objects_backfilled': {'const': True}}},
                                 'then': {'required': ['backfill_job']}},
                'dependencies': {'type': 'array',
                                 'minItems': 3,
                                 'allOf': [{'contains': {'properties': {'kind': {'const': 'identity-provider'}}}},
                                           {'contains': {'properties': {'kind': {'const': 'dns-provider'}}}},
                                           {'contains': {'properties': {'kind': {'const': 'ci-cd'}}}}],
                                 'items': {'type': 'object',
                                           'required': ['name', 'kind', 'reachable_from_secondary'],
                                           'additionalProperties': False,
                                           'properties': {'name': {'type': 'string',
                                                                   'minLength': 2},
                                                          'kind': {'type': 'string',
                                                                   'enum': ['identity-provider',
                                                                            'secrets-manager',
                                                                            'ci-cd',
                                                                            'dns-provider',
                                                                            'certificate-issuance',
                                                                            'payments',
                                                                            'email',
                                                                            'cloud-control-plane',
                                                                            'other']},
                                                          'reachable_from_secondary': {'type': 'boolean'},
                                                          'bypass': {'$ref': '#/definitions/text'}},
                                           'if': {'properties': {'reachable_from_secondary': {'const': False}}},
                                           'then': {'required': ['bypass']}}},
                'drill': {'type': 'object',
                          'required': ['checklist', 'mechanics_last_changed_at', 'last'],
                          'additionalProperties': False,
                          'properties': {'checklist': {'type': 'array',
                                                       'minItems': 5,
                                                       'items': {'$ref': '#/definitions/text'}},
                                         'mechanics_last_changed_at': {'$ref': '#/definitions/date'},
                                         'last': {'oneOf': [{'type': 'null'},
                                                            {'type': 'object',
                                                             'required': ['date',
                                                                          'scope_services',
                                                                          'traffic_percent',
                                                                          'measured_rto_minutes',
                                                                          'measured_rpo_minutes',
                                                                          'manual_steps'],
                                                             'additionalProperties': False,
                                                             'properties': {'date': {'$ref': '#/definitions/date'},
                                                                            'scope_services': {'type': 'array',
                                                                                               'minItems': 1,
                                                                                               'items': {'type': 'string',
                                                                                                         'minLength': 2}},
                                                                            'traffic_percent': {'type': 'number',
                                                                                                'minimum': 0,
                                                                                                'maximum': 100},
                                                                            'measured_rto_minutes': {'type': 'number',
                                                                                                     'minimum': 0},
                                                                            'measured_rpo_minutes': {'type': 'number',
                                                                                                     'minimum': 0},
                                                                            'manual_steps': {'type': 'array',
                                                                                             'items': {'$ref': '#/definitions/text'}}}}]}}},
                'failback': {'type': 'object',
                             'required': ['trigger',
                                          'rpo_minutes',
                                          'rto_minutes',
                                          'reconciliation_step',
                                          'procedure'],
                             'additionalProperties': False,
                             'properties': {'trigger': {'$ref': '#/definitions/text'},
                                            'rpo_minutes': {'type': 'integer', 'minimum': 0},
                                            'rto_minutes': {'type': 'integer', 'minimum': 0},
                                            'reconciliation_step': {'$ref': '#/definitions/text'},
                                            'procedure': {'$ref': '#/definitions/text'}}},
                'decision': {'type': 'string',
                             'minLength': 20,
                             'pattern': '(backup-and-restore|pilot-light|warm-standby|active-passive-hot-standby|active-active)'},
                'evidence': {'type': 'array',
                             'minItems': 1,
                             'items': {'type': 'string', 'pattern': '^https://'}},
                'review': {'type': 'object',
                           'required': ['cadence', 'next_review_at'],
                           'additionalProperties': False,
                           'properties': {'cadence': {'type': 'string',
                                                      'enum': ['monthly', 'quarterly']},
                                          'next_review_at': {'$ref': '#/definitions/date'}}}}}

OK = {'workload': {'name': 'payments-api', 'tier': 'tier-1', 'business_owner': 'product:maria'},
 'owner': 'arch:alice',
 'inputs': [{'name': 'rpo_minutes', 'value': 5},
            {'name': 'rto_minutes', 'value': 30},
            {'name': 'primary_region', 'value': 'eu-west-1'},
            {'name': 'secondary_region', 'value': 'eu-central-1'}],
 'pattern': {'chosen': 'warm-standby',
             'achievable_rpo_minutes': 1,
             'achievable_rto_minutes': 22,
             'secondary_capacity': {'mode': 'scale-up',
                                    'percent_of_primary': 40,
                                    'scale_up_minutes': 12,
                                    'quotas_verified': True}},
 'dns': {'mechanism': 'dns-failover',
         'ttl_seconds': 60,
         'health_check': {'endpoint': 'https://api.payments.example.com/healthz',
                          'interval_seconds': 10,
                          'failure_threshold': 3},
         'observed_propagation_seconds': 95,
         'ttl_ignoring_clients': [{'client': 'ios-sdk 4.x (caches resolved IP for process '
                                             'lifetime)',
                                   'fallback': 'client-side-retry-to-secondary'}]},
 'database': {'engine': 'PostgreSQL 16 (RDS)',
              'replication': 'asynchronous',
              'p99_lag_seconds_30d': 12,
              'promotion_procedure': 'runbook RB-114: promote eu-central-1 read replica via aws '
                                     'rds promote-read-replica, then rotate the writer endpoint in '
                                     'Secrets Manager',
              'fencing': "revoke the app role's write grant on the old primary and set "
                         'default_transaction_read_only=on before promotion',
              'single_writer_enforcement': 'writer endpoint resolved from Secrets Manager only; '
                                           "the old primary's security group drops port 5432 from "
                                           'app subnets after fencing'},
 'object_store': {'provider': 'Amazon S3',
                  'replication_enabled': True,
                  'versioning': True,
                  'backlog_metric': 'AWS/S3 OperationsPendingReplication on payments-docs',
                  'replication_time_alert': 'ReplicationLatency above 900 s for 15 min pages '
                                            'sre-primary',
                  'existing_objects_backfilled': True,
                  'backfill_job': 'S3 Batch Replication job 7f2e9c (2026-03-04), 1.2 M objects'},
 'dependencies': [{'name': 'Okta', 'kind': 'identity-provider', 'reachable_from_secondary': True},
                  {'name': 'AWS Secrets Manager (replicated secret)',
                   'kind': 'secrets-manager',
                   'reachable_from_secondary': True},
                  {'name': 'GitHub Actions self-hosted runners',
                   'kind': 'ci-cd',
                   'reachable_from_secondary': False,
                   'bypass': 'failover script is also runnable from the break-glass bastion in '
                             'eu-central-1: runbook RB-114 step 2'},
                  {'name': 'Route 53', 'kind': 'dns-provider', 'reachable_from_secondary': True},
                  {'name': 'ACM certificates',
                   'kind': 'certificate-issuance',
                   'reachable_from_secondary': True},
                  {'name': 'Adyen', 'kind': 'payments', 'reachable_from_secondary': True}],
 'drill': {'checklist': ['announce drill window and freeze deploys',
                         'fence the primary database (RB-114 step 1)',
                         'promote the eu-central-1 replica and rotate the writer secret',
                         'flip the Route 53 failover record and start the propagation timer',
                         'scale the secondary ASG to 100 percent and confirm quota headroom',
                         'run the synthetic checkout and record measured RTO and RPO',
                         'list every step that needed a human'],
           'mechanics_last_changed_at': '2026-07-14',
           'last': {'date': '2026-08-20',
                    'scope_services': ['payments-api', 'payments-worker'],
                    'traffic_percent': 5,
                    'measured_rto_minutes': 22,
                    'measured_rpo_minutes': 0.5,
                    'manual_steps': ['writer secret rotation required a human approval in Secrets '
                                     'Manager']}},
 'failback': {'trigger': 'primary region healthy for 60 minutes and replication from secondary to '
                         'primary caught up (lag under 5 s)',
              'rpo_minutes': 0,
              'rto_minutes': 45,
              'reconciliation_step': 'replay writes accepted in eu-central-1 from the logical '
                                     'replication slot into the rebuilt primary; verify row counts '
                                     'per table',
              'procedure': 'runbook RB-115: rebuild eu-west-1 as replica of the promoted primary, '
                           're-fence, promote back during a change window, flip DNS'},
 'decision': 'Adopt warm-standby for payments-api: achievable RTO 22 min against required 30, '
             'achievable RPO 1 min against required 5; verified by the 2026-08-20 drill at 5 '
             'percent of traffic.',
 'evidence': ['https://wiki.example.com/dr/drills/2026-08-20-payments',
              'https://grafana.example.com/d/rds-replication?from=1751328000000&to=1753920000000',
              'https://console.aws.amazon.com/servicequotas/home/requests/abc123'],
 'review': {'cadence': 'quarterly', 'next_review_at': '2026-11-20'}}

BAD = {'workload': {'name': 'payments-api', 'tier': 'tier-1', 'business_owner': 'product:maria'},
 'owner': 'arch:alice',
 'inputs': [{'name': 'rpo_minutes', 'value': 0}, {'name': 'rto_minutes', 'value': 30}],
 'pattern': {'chosen': 'pilot-light',
             'achievable_rpo_minutes': 0,
             'achievable_rto_minutes': 90,
             'secondary_capacity': {'mode': 'scale-up',
                                    'percent_of_primary': 10,
                                    'scale_up_minutes': 60,
                                    'quotas_verified': True}},
 'dns': {'mechanism': 'dns-failover',
         'ttl_seconds': 3600,
         'health_check': {'endpoint': 'https://api.payments.example.com/healthz',
                          'interval_seconds': 30,
                          'failure_threshold': 3},
         'observed_propagation_seconds': 0,
         'ttl_ignoring_clients': []},
 'database': {'engine': 'PostgreSQL 16 (RDS)',
              'replication': 'asynchronous',
              'p99_lag_seconds_30d': 40,
              'promotion_procedure': 'promote the replica in the console',
              'fencing': 'n/a',
              'single_writer_enforcement': 'n/a'},
 'object_store': {'provider': 'Amazon S3',
                  'replication_enabled': True,
                  'versioning': True,
                  'backlog_metric': 'none yet',
                  'replication_time_alert': 'none yet',
                  'existing_objects_backfilled': False},
 'dependencies': [{'name': 'Okta', 'kind': 'identity-provider', 'reachable_from_secondary': True},
                  {'name': 'GitHub Actions self-hosted runners',
                   'kind': 'ci-cd',
                   'reachable_from_secondary': False},
                  {'name': 'Route 53', 'kind': 'dns-provider', 'reachable_from_secondary': True}],
 'drill': {'checklist': ['announce drill window and freeze deploys',
                         'promote the replica',
                         'flip DNS',
                         'scale up the secondary',
                         'run the synthetic checkout'],
           'mechanics_last_changed_at': '2026-07-14',
           'last': None},
 'failback': {'trigger': 'when the primary is back',
              'rpo_minutes': 0,
              'rto_minutes': 45,
              'reconciliation_step': 'to be defined',
              'procedure': 'reverse the failover'},
 'decision': 'Adopt pilot-light for payments-api with zero data loss.',
 'evidence': ['https://wiki.example.com/dr/payments-plan'],
 'review': {'cadence': 'quarterly', 'next_review_at': '2026-11-20'}}


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


_PATTERNS = ("backup-and-restore", "pilot-light", "warm-standby", "active-passive-hot-standby", "active-active")


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    inputs = {i.get("name"): i.get("value") for i in obj.get("inputs") or [] if isinstance(i, dict)}
    rpo, rto = inputs.get("rpo_minutes", 0), inputs.get("rto_minutes", 0)
    pat = obj.get("pattern") or {}
    if pat.get("achievable_rto_minutes", 0) > rto:
        errs.append(f"pattern.achievable_rto_minutes {pat.get('achievable_rto_minutes')} exceeds required rto_minutes {rto} (r-pattern-chosen-from-rpo-rto-and-cost)")
    if pat.get("achievable_rpo_minutes", 0) > rpo:
        errs.append(f"pattern.achievable_rpo_minutes {pat.get('achievable_rpo_minutes')} exceeds required rpo_minutes {rpo} (r-pattern-chosen-from-rpo-rto-and-cost)")
    cap = pat.get("secondary_capacity") or {}
    if cap.get("mode") == "scale-up" and cap.get("scale_up_minutes", 0) > rto:
        errs.append(f"pattern.secondary_capacity.scale_up_minutes {cap.get('scale_up_minutes')} exceeds rto_minutes {rto} (fm-07)")
    db = obj.get("database") or {}
    if db.get("replication") == "asynchronous" and db.get("p99_lag_seconds_30d", 0) > rpo * 60:
        errs.append(f"database.p99_lag_seconds_30d {db.get('p99_lag_seconds_30d')} exceeds rpo_minutes {rpo} x 60 with asynchronous replication (r-database-replication-mode-and-promotion)")
    decision = obj.get("decision", "")
    named = [p for p in _PATTERNS if p in decision]
    if len(named) != 1:
        errs.append(f"decision names {len(named)} patterns; exactly one required (r-pattern-chosen-from-rpo-rto-and-cost)")
    elif named[0] != pat.get("chosen"):
        errs.append(f"decision names {named[0]} but pattern.chosen is {pat.get('chosen')} (r-pattern-chosen-from-rpo-rto-and-cost)")
    drill = obj.get("drill") or {}
    last = drill.get("last")
    stale = last is None or (last or {}).get("date", "") < drill.get("mechanics_last_changed_at", "")
    if stale and "unverified" not in decision:
        errs.append("drill.last is missing or older than mechanics_last_changed_at and decision is not labelled unverified (r-drill-live-with-measured-results)")
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
        prog="validate-multi-region-failover-pattern-pack.py",
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
