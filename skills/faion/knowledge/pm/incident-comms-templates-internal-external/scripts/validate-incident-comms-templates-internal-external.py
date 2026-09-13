#!/usr/bin/env python3
"""validate-incident-comms-templates-internal-external.py

Validate the IncidentCommsBundle produced by the incident-comms-templates-internal-external methodology against the
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
import datetime as dt
import json
import re
import sys
from pathlib import Path

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/incident-comms-bundle.json', 'title': 'IncidentCommsBundle', 'type': 'object', 'required': ['service', 'header', 'severity_matrix', 'token_list', 'templates', 'incidents'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'datetime_tz': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2})?(Z|[+-][0-9]{2}:[0-9]{2})$'}, 'person': {'type': 'string', 'minLength': 2, 'not': {'pattern': '(?i)^(team|on-call|tbd|everyone|n/a)$'}}, 'audience': {'enum': ['status_page', 'customer_email', 'exec_brief', 'internal_channel']}, 'severity': {'type': 'string', 'pattern': '^(P[1-4]|SEV[1-4])$'}, 'filled_text': {'type': 'string', 'minLength': 20, 'not': {'pattern': '\\{\\{[a-z_]+\\}\\}|<!--'}}, 'template': {'type': 'object', 'required': ['body', 'last_drilled'], 'properties': {'body': {'type': 'string', 'minLength': 40}, 'last_drilled': {'$ref': '#/definitions/date'}}}, 'external_review': {'type': 'object', 'required': ['unconfirmed_cause', 'blame', 'internal_names', 'customer_pii'], 'properties': {'unconfirmed_cause': {'const': False}, 'blame': {'const': False}, 'internal_names': {'const': False}, 'customer_pii': {'const': False}}}}, 'properties': {'__faion_header__': {'type': 'object'}, 'service': {'type': 'string', 'minLength': 2}, 'header': {'type': 'object', 'required': ['owner', 'version', 'last_reviewed'], 'properties': {'owner': {'type': 'string', 'pattern': '^[a-z][a-z0-9-]*:[a-z0-9._-]+$'}, 'version': {'type': 'string', 'pattern': '^[0-9]+\\.[0-9]+\\.[0-9]+$'}, 'last_reviewed': {'$ref': '#/definitions/date'}}}, 'severity_matrix': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['severity', 'audiences', 'first_post_deadline_minutes', 'update_interval_minutes', 'post_incident_email_deadline_hours'], 'properties': {'severity': {'$ref': '#/definitions/severity'}, 'audiences': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'$ref': '#/definitions/audience'}}, 'first_post_deadline_minutes': {'type': 'integer', 'minimum': 1, 'maximum': 240}, 'update_interval_minutes': {'type': 'integer', 'minimum': 5, 'maximum': 240}, 'post_incident_email_deadline_hours': {'type': 'integer', 'minimum': 1, 'maximum': 240}}}}, 'token_list': {'type': 'array', 'minItems': 4, 'uniqueItems': True, 'items': {'type': 'string', 'pattern': '^[a-z][a-z_]*$'}}, 'templates': {'type': 'object', 'required': ['status_page', 'customer_email', 'exec_brief', 'internal_channel'], 'additionalProperties': False, 'properties': {'status_page': {'allOf': [{'$ref': '#/definitions/template'}, {'properties': {'body': {'allOf': [{'pattern': '\\{\\{state\\}\\}'}, {'pattern': '\\{\\{timestamp\\}\\}'}, {'pattern': '\\{\\{impact\\}\\}'}, {'pattern': '\\{\\{next_update_at\\}\\}'}]}}}]}, 'customer_email': {'allOf': [{'$ref': '#/definitions/template'}, {'properties': {'body': {'allOf': [{'pattern': '\\{\\{impact\\}\\}'}, {'pattern': '\\{\\{next_update_at\\}\\}'}]}}}]}, 'exec_brief': {'allOf': [{'$ref': '#/definitions/template'}, {'properties': {'body': {'allOf': [{'pattern': '\\{\\{customer_impact\\}\\}'}, {'pattern': '\\{\\{eta\\}\\}'}, {'pattern': '\\{\\{decisions_needed\\}\\}'}, {'pattern': '\\{\\{what_is_being_done\\}\\}'}, {'pattern': '\\{\\{next_update_at\\}\\}'}]}}}]}, 'internal_channel': {'allOf': [{'$ref': '#/definitions/template'}, {'properties': {'body': {'allOf': [{'pattern': '\\{\\{severity\\}\\}'}, {'pattern': '\\{\\{commander\\}\\}'}, {'pattern': '\\{\\{comms_lead\\}\\}'}, {'pattern': '\\{\\{blast_radius\\}\\}'}, {'pattern': '\\{\\{hypothesis\\}\\}'}, {'pattern': '\\{\\{actions\\}\\}'}, {'pattern': '\\{\\{incident_link\\}\\}'}, {'pattern': '\\{\\{next_checkpoint_at\\}\\}'}]}}}]}}}, 'incidents': {'type': 'array', 'items': {'type': 'object', 'required': ['incident_id', 'severity', 'declared_at', 'audiences_sent', 'updates', 'internal_post'], 'additionalProperties': False, 'properties': {'incident_id': {'type': 'string', 'pattern': '^INC-[0-9]+$'}, 'severity': {'$ref': '#/definitions/severity'}, 'declared_at': {'$ref': '#/definitions/datetime_tz'}, 'audiences_sent': {'type': 'array', 'uniqueItems': True, 'items': {'$ref': '#/definitions/audience'}}, 'updates': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['channel', 'posted_at', 'minutes_after_declaration', 'text', 'next_update_at', 'approved_by'], 'properties': {'channel': {'enum': ['status_page', 'customer_email']}, 'state': {'enum': ['Investigating', 'Identified', 'Monitoring', 'Resolved']}, 'posted_at': {'$ref': '#/definitions/datetime_tz'}, 'minutes_after_declaration': {'type': 'integer', 'minimum': 0}, 'text': {'$ref': '#/definitions/filled_text'}, 'impact': {'type': 'string', 'minLength': 10}, 'component_status_matches_text': {'type': 'boolean'}, 'next_update_at': {'anyOf': [{'$ref': '#/definitions/datetime_tz'}, {'type': 'null'}]}, 'review': {'$ref': '#/definitions/external_review'}, 'approved_by': {'$ref': '#/definitions/person'}}, 'allOf': [{'if': {'properties': {'channel': {'const': 'status_page'}}}, 'then': {'required': ['state', 'impact', 'component_status_matches_text'], 'properties': {'component_status_matches_text': {'const': True}}}}, {'if': {'properties': {'state': {'const': 'Resolved'}}, 'required': ['state']}, 'else': {'required': ['review'], 'properties': {'next_update_at': {'type': 'string'}, 'text': {'allOf': [{'pattern': '(?i)next update (by|at) '}, {'not': {'pattern': '(?i)(we believe|likely caused|appears to be|root cause (is|was)|caused by)'}}]}}}}]}}, 'internal_post': {'type': 'object', 'required': ['severity', 'commander', 'comms_lead', 'blast_radius', 'current_hypothesis', 'actions_in_flight', 'incident_link', 'next_checkpoint_at'], 'properties': {'severity': {'$ref': '#/definitions/severity'}, 'commander': {'$ref': '#/definitions/person'}, 'comms_lead': {'$ref': '#/definitions/person'}, 'blast_radius': {'$ref': '#/definitions/filled_text'}, 'current_hypothesis': {'type': 'string', 'minLength': 5, 'not': {'pattern': '\\{\\{[a-z_]+\\}\\}'}}, 'actions_in_flight': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['action', 'owner'], 'properties': {'action': {'type': 'string', 'minLength': 5}, 'owner': {'$ref': '#/definitions/person'}}}}, 'incident_link': {'type': 'string', 'pattern': '^https?://\\S+$'}, 'next_checkpoint_at': {'$ref': '#/definitions/datetime_tz'}}}, 'exec_brief': {'type': 'object', 'required': ['customer_impact', 'eta', 'decisions_needed', 'what_is_being_done', 'next_update_at', 'word_count', 'technical_narrative'], 'additionalProperties': False, 'properties': {'customer_impact': {'type': 'object', 'required': ['customers_affected', 'revenue_at_risk', 'sla_credits_exposed'], 'properties': {'customers_affected': {'type': 'string', 'minLength': 2}, 'revenue_at_risk': {'type': 'string', 'minLength': 2}, 'sla_credits_exposed': {'type': 'string', 'minLength': 2}}}, 'eta': {'type': 'string', 'minLength': 5, 'pattern': '(?i)(^[0-9]{4}-|unknown, next update at )'}, 'decisions_needed': {'type': 'array', 'items': {'type': 'string', 'minLength': 5}}, 'what_is_being_done': {'$ref': '#/definitions/filled_text'}, 'next_update_at': {'$ref': '#/definitions/datetime_tz'}, 'word_count': {'type': 'integer', 'minimum': 20, 'maximum': 150}, 'technical_narrative': {'const': False}}}, 'resolved': {'type': 'object', 'required': ['start_at', 'end_at', 'affected_scope', 'fix_applied', 'postmortem_due', 'post_incident_email_sent_at'], 'properties': {'start_at': {'$ref': '#/definitions/datetime_tz'}, 'end_at': {'$ref': '#/definitions/datetime_tz'}, 'affected_scope': {'$ref': '#/definitions/filled_text'}, 'fix_applied': {'$ref': '#/definitions/filled_text'}, 'postmortem_due': {'$ref': '#/definitions/date'}, 'post_incident_email_sent_at': {'anyOf': [{'$ref': '#/definitions/datetime_tz'}, {'type': 'null'}]}}}}}}}}

OK = {'service': 'checkout-api', 'header': {'owner': 'pm:olena.k', 'version': '1.3.0', 'last_reviewed': '2026-05-04'}, 'severity_matrix': [{'severity': 'P1', 'audiences': ['status_page', 'customer_email', 'exec_brief', 'internal_channel'], 'first_post_deadline_minutes': 15, 'update_interval_minutes': 30, 'post_incident_email_deadline_hours': 72}, {'severity': 'P2', 'audiences': ['status_page', 'exec_brief', 'internal_channel'], 'first_post_deadline_minutes': 30, 'update_interval_minutes': 60, 'post_incident_email_deadline_hours': 120}, {'severity': 'P3', 'audiences': ['internal_channel'], 'first_post_deadline_minutes': 60, 'update_interval_minutes': 120, 'post_incident_email_deadline_hours': 240}], 'token_list': ['incident_id', 'state', 'timestamp', 'impact', 'next_update_at', 'customer_impact', 'eta', 'decisions_needed', 'what_is_being_done', 'severity', 'commander', 'comms_lead', 'blast_radius', 'hypothesis', 'actions', 'incident_link', 'next_checkpoint_at', 'start_at', 'end_at', 'fix_applied', 'postmortem_due'], 'templates': {'status_page': {'body': '{{state}} ({{timestamp}}): {{impact}}. We will post the next update by {{next_update_at}}.', 'last_drilled': '2026-04-20'}, 'customer_email': {'body': 'Subject: {{incident_id}} service disruption. We are aware of an issue affecting {{impact}}. Our team is working on it; next update by {{next_update_at}}. We will share a full report at {{postmortem_due}}.', 'last_drilled': '2026-04-20'}, 'exec_brief': {'body': 'Impact: {{customer_impact}}. ETA: {{eta}}. Decisions needed from you: {{decisions_needed}}. In progress: {{what_is_being_done}}. Next update: {{next_update_at}}.', 'last_drilled': '2026-04-20'}, 'internal_channel': {'body': 'Sev {{severity}} | IC {{commander}} | Comms {{comms_lead}} | Blast radius: {{blast_radius}} | Hypothesis: {{hypothesis}} | In flight: {{actions}} | Channel: {{incident_link}} | Next checkpoint {{next_checkpoint_at}}', 'last_drilled': '2026-04-20'}}, 'incidents': [{'incident_id': 'INC-2041', 'severity': 'P1', 'declared_at': '2026-05-12T09:02+02:00', 'audiences_sent': ['status_page', 'customer_email', 'exec_brief', 'internal_channel'], 'updates': [{'channel': 'status_page', 'state': 'Investigating', 'posted_at': '2026-05-12T09:10+02:00', 'minutes_after_declaration': 8, 'impact': 'Checkout for EU customers returns errors; browsing and cart are unaffected', 'text': 'Investigating (2026-05-12 09:10 CEST): checkout for EU customers returns errors; browsing and cart are unaffected. We will post the next update by 09:40 CEST.', 'component_status_matches_text': True, 'next_update_at': '2026-05-12T09:40+02:00', 'review': {'unconfirmed_cause': False, 'blame': False, 'internal_names': False, 'customer_pii': False}, 'approved_by': 'dana.r'}, {'channel': 'customer_email', 'posted_at': '2026-05-12T09:14+02:00', 'minutes_after_declaration': 12, 'text': 'We are aware of an issue affecting checkout for EU customers since 09:02 CEST. Browsing and cart are unaffected. Our team is working on it; next update by 09:40 CEST.', 'next_update_at': '2026-05-12T09:40+02:00', 'review': {'unconfirmed_cause': False, 'blame': False, 'internal_names': False, 'customer_pii': False}, 'approved_by': 'dana.r'}, {'channel': 'status_page', 'state': 'Identified', 'posted_at': '2026-05-12T09:38+02:00', 'minutes_after_declaration': 36, 'impact': 'Checkout for EU customers returns errors; browsing and cart are unaffected', 'text': 'Identified (2026-05-12 09:38 CEST): the fault is isolated and a fix is being applied; checkout for EU customers still returns errors. Next update by 10:08 CEST.', 'component_status_matches_text': True, 'next_update_at': '2026-05-12T10:08+02:00', 'review': {'unconfirmed_cause': False, 'blame': False, 'internal_names': False, 'customer_pii': False}, 'approved_by': 'dana.r'}, {'channel': 'status_page', 'state': 'Monitoring', 'posted_at': '2026-05-12T10:05+02:00', 'minutes_after_declaration': 63, 'impact': 'Checkout for EU customers recovering; error rate back to normal since 10:01 CEST', 'text': 'Monitoring (2026-05-12 10:05 CEST): a fix has been applied and checkout for EU customers is recovering; error rate back to normal since 10:01 CEST. Next update by 10:35 CEST.', 'component_status_matches_text': True, 'next_update_at': '2026-05-12T10:35+02:00', 'review': {'unconfirmed_cause': False, 'blame': False, 'internal_names': False, 'customer_pii': False}, 'approved_by': 'dana.r'}, {'channel': 'status_page', 'state': 'Resolved', 'posted_at': '2026-05-12T10:33+02:00', 'minutes_after_declaration': 91, 'impact': 'Checkout for EU customers, 09:02 to 10:01 CEST', 'text': 'Resolved (2026-05-12 10:33 CEST): between 09:02 and 10:01 CEST checkout for EU customers returned errors. A configuration change in our payment routing was rolled back. A post-incident report will be published by 2026-05-15.', 'component_status_matches_text': True, 'next_update_at': None, 'approved_by': 'dana.r'}], 'internal_post': {'severity': 'P1', 'commander': 'ihor.m', 'comms_lead': 'dana.r', 'blast_radius': 'EU checkout, roughly 38% of daily order volume; US and APAC unaffected', 'current_hypothesis': 'payment-router config push at 08:58 changed the EU PSP endpoint; rollback in progress', 'actions_in_flight': [{'action': 'Roll back payment-router config to 08:40 revision', 'owner': 'taras.v'}, {'action': 'Pull EU error-rate graph into the incident channel', 'owner': 'maksym.d'}], 'incident_link': 'https://acme.slack.com/archives/C0INC2041', 'next_checkpoint_at': '2026-05-12T09:30+02:00'}, 'exec_brief': {'customer_impact': {'customers_affected': 'EU customers, about 38% of daily orders', 'revenue_at_risk': 'about 41k EUR per hour of outage', 'sla_credits_exposed': '3 enterprise contracts with 99.9% monthly SLA'}, 'eta': 'unknown, next update at 09:40 CEST', 'decisions_needed': ['Approve proactive credit note to the 3 enterprise accounts if outage exceeds 2 hours'], 'what_is_being_done': 'Rolling back a payment routing change; customer email and status page posted at 09:14 CEST', 'next_update_at': '2026-05-12T09:40+02:00', 'word_count': 78, 'technical_narrative': False}, 'resolved': {'start_at': '2026-05-12T09:02+02:00', 'end_at': '2026-05-12T10:01+02:00', 'affected_scope': 'Checkout for EU customers; browsing and cart unaffected; US and APAC unaffected', 'fix_applied': 'Payment-router configuration rolled back to the 08:40 revision', 'postmortem_due': '2026-05-15', 'post_incident_email_sent_at': '2026-05-14T16:00+02:00'}}]}

BAD = {'service': 'checkout-api', 'header': {'owner': 'pm:olena.k', 'version': '1.3.0', 'last_reviewed': '2026-05-04'}, 'severity_matrix': [{'severity': 'P1', 'audiences': ['customer_email', 'exec_brief', 'internal_channel'], 'first_post_deadline_minutes': 15, 'update_interval_minutes': 30, 'post_incident_email_deadline_hours': 72}], 'token_list': ['incident_id', 'state', 'timestamp', 'impact', 'next_update_at'], 'templates': {'status_page': {'body': '{{state}} ({{timestamp}}): {{impact}}. We will post the next update by {{next_update_at}}.', 'last_drilled': '2025-11-03'}, 'customer_email': {'body': 'We are aware of an issue affecting {{impact}}. We will keep you posted.', 'last_drilled': '2025-11-03'}, 'exec_brief': {'body': 'Impact: {{customer_impact}}. ETA: {{eta}}. Decisions needed: {{decisions_needed}}. In progress: {{what_is_being_done}}. Next update: {{next_update_at}}.', 'last_drilled': '2025-11-03'}, 'internal_channel': {'body': 'Sev {{severity}} | IC {{commander}} | Comms {{comms_lead}} | Blast radius: {{blast_radius}} | Hypothesis: {{hypothesis}} | In flight: {{actions}} | Channel: {{incident_link}} | Next checkpoint {{next_checkpoint_at}}', 'last_drilled': '2025-11-03'}}, 'incidents': [{'incident_id': 'INC-2041', 'severity': 'P1', 'declared_at': '2026-05-12T09:02+02:00', 'audiences_sent': ['status_page', 'internal_channel'], 'updates': [{'channel': 'status_page', 'state': 'Investigating', 'posted_at': '2026-05-12T09:50+02:00', 'minutes_after_declaration': 48, 'impact': 'Checkout errors', 'text': 'We are investigating an issue affecting {{impact}} customers. We believe the database cluster db-eu-1 is the cause.', 'component_status_matches_text': False, 'next_update_at': None, 'review': {'unconfirmed_cause': True, 'blame': False, 'internal_names': True, 'customer_pii': False}, 'approved_by': 'on-call'}, {'channel': 'status_page', 'state': 'Resolved', 'posted_at': '2026-05-12T12:40+02:00', 'minutes_after_declaration': 218, 'impact': 'Checkout errors', 'text': 'The issue has been resolved. Thank you for your patience while we worked on this.', 'component_status_matches_text': True, 'next_update_at': None, 'approved_by': 'dana.r'}], 'internal_post': {'severity': 'P1', 'commander': 'team', 'comms_lead': 'dana.r', 'blast_radius': 'EU checkout, roughly 38% of daily order volume', 'current_hypothesis': 'payment-router config push changed the EU PSP endpoint', 'actions_in_flight': [], 'incident_link': 'https://acme.slack.com/archives/C0INC2041', 'next_checkpoint_at': '2026-05-12T09:30+02:00'}, 'exec_brief': {'customer_impact': {'customers_affected': 'EU customers', 'revenue_at_risk': 'significant', 'sla_credits_exposed': 'some'}, 'eta': 'soon', 'decisions_needed': [], 'what_is_being_done': 'At 08:58 a configuration push to the payment router changed the EU PSP endpoint; the connection pool then exhausted because retries doubled; we are rolling back and also considering a hotfix to the pool sizing which needs a restart of the three router pods in eu-west-1', 'next_update_at': '2026-05-12T09:40+02:00', 'word_count': 240, 'technical_narrative': True}}]}


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


_STATES = ["Investigating", "Identified", "Monitoring", "Resolved"]
_TOKEN_RE = re.compile(r"\{\{([a-z_]+)\}\}")


def _dt(s):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (TypeError, ValueError, AttributeError):
        return None


def _date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _sev_rank(s):
    return int(s[-1]) if s and s[-1].isdigit() else 9


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    rows = {r.get("severity"): r for r in obj.get("severity_matrix") or []}
    if rows:
        top = min(rows, key=_sev_rank)
        if "status_page" not in rows[top].get("audiences", []):
            errs.append(f"severity_matrix[{top}]: the highest severity must include status_page (r-severity-audience-matrix)")
    tokens = set(obj.get("token_list") or [])
    templates = obj.get("templates") or {}
    for name, t in templates.items():
        for tok in sorted(set(_TOKEN_RE.findall((t or {}).get("body", "")))):
            if tok not in tokens:
                errs.append(f"templates.{name}: token {{{{{tok}}}}} is not in token_list (r-placeholders-resolved-before-send)")
    for i, inc in enumerate(obj.get("incidents") or []):
        sev, row = inc.get("severity"), rows.get(inc.get("severity"))
        if row is None:
            errs.append(f"incidents[{i}]: no severity_matrix row for {sev!r} (r-severity-audience-matrix)")
            continue
        want, sent = set(row.get("audiences", [])), set(inc.get("audiences_sent") or [])
        for a in sorted(sent - want):
            errs.append(f"incidents[{i}]: {a} was sent but the {sev} row does not list it (r-severity-audience-matrix)")
        for a in sorted(want - sent):
            errs.append(f"incidents[{i}]: {a} is in the {sev} row and received nothing (r-severity-audience-matrix)")
        declared = _dt(inc.get("declared_at"))
        updates = inc.get("updates") or []
        external = [u for u in updates if u.get("channel") in ("status_page", "customer_email")]
        if external:
            first = min(u.get("minutes_after_declaration", 0) for u in external)
            if first > row.get("first_post_deadline_minutes", 0):
                errs.append(f"incidents[{i}]: first external post at {first} min, deadline for {sev} is {row.get('first_post_deadline_minutes')} (r-first-post-deadline-and-cadence)")
        page = [u for u in updates if u.get("channel") == "status_page"]
        for prev, cur in zip(page, page[1:]):
            gap = cur.get("minutes_after_declaration", 0) - prev.get("minutes_after_declaration", 0)
            if gap > row.get("update_interval_minutes", 0):
                errs.append(f"incidents[{i}]: {gap} min between status-page updates, interval for {sev} is {row.get('update_interval_minutes')}; post 'no change' instead (r-first-post-deadline-and-cadence)")
            if _STATES.index(cur.get("state", "Investigating")) < _STATES.index(prev.get("state", "Investigating")):
                errs.append(f"incidents[{i}]: status-page state went from {prev.get('state')} to {cur.get('state')}; states only move forward (r-status-page-lifecycle-states)")
        ip = inc.get("internal_post") or {}
        if ip.get("severity") != sev:
            errs.append(f"incidents[{i}].internal_post.severity {ip.get('severity')!r} != incident severity {sev!r} (r-internal-post-fields)")
        if "exec_brief" in want and "exec_brief" not in inc:
            errs.append(f"incidents[{i}]: {sev} row lists exec_brief and none was written (r-exec-brief-one-screen)")
        if any(u.get("state") == "Resolved" for u in page):
            res = inc.get("resolved")
            if not isinstance(res, dict):
                errs.append(f"incidents[{i}]: status page says Resolved but no resolved block with start, end, scope, fix and postmortem date (r-resolution-and-postmortem-commitment)")
            else:
                s, e, pm = _dt(res.get("start_at")), _dt(res.get("end_at")), _date(res.get("postmortem_due"))
                if s and e and e <= s:
                    errs.append(f"incidents[{i}].resolved: end_at is not after start_at (r-resolution-and-postmortem-commitment)")
                if e and pm and pm <= e.date():
                    errs.append(f"incidents[{i}].resolved: postmortem_due {pm} is not after the incident end (r-resolution-and-postmortem-commitment)")
                sent_at = _dt(res.get("post_incident_email_sent_at"))
                if e and sent_at and (sent_at - e).total_seconds() > row.get("post_incident_email_deadline_hours", 0) * 3600:
                    errs.append(f"incidents[{i}].resolved: post-incident email sent {(sent_at - e).total_seconds() / 3600:.0f}h after the end, deadline for {sev} is {row.get('post_incident_email_deadline_hours')}h (r-resolution-and-postmortem-commitment)")
        if declared:
            for a in sorted(sent):
                ld = _date((templates.get(a) or {}).get("last_drilled"))
                if ld and (declared.date() - ld).days > 90:
                    errs.append(f"incidents[{i}]: templates.{a} last drilled {(declared.date() - ld).days} days before the incident; stale over 90 (r-quarterly-drill)")
    return errs


def validate(obj) -> list[str]:
    errs: list[str] = []
    _check(obj, SCHEMA, "$", errs)
    if not errs and isinstance(obj, dict):
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
        prog="validate-incident-comms-templates-internal-external.py",
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
