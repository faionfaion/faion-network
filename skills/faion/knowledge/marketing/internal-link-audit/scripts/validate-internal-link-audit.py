#!/usr/bin/env python3
"""validate-internal-link-audit.py

Validate the internal-link audit report produced by the internal-link-audit methodology against the
draft-07 JSON Schema embedded in content/02-output-contract.xml, plus the
cross-field rules from content/01-core-rules.xml the schema cannot express. Stdlib-only;
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

SCHEMA = {'$schema': 'http://json-schema.org/draft-07/schema#', '$id': 'https://faion.net/schemas/internal-link-audit.json', 'title': 'Internal Link Audit report', 'type': 'object', 'required': ['site', 'audit_period', 'crawl', 'incoming_counts', 'orphans', 'clusters', 'anchor_text', 'hygiene_findings', 'rewire_plan', 'gsc_baseline', 'remeasurement'], 'additionalProperties': False, 'definitions': {'date': {'type': 'string', 'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'}, 'url': {'type': 'string', 'pattern': '^https?://[^ ]+$'}, 'count': {'type': 'integer', 'minimum': 0}, 'generic_anchor': {'enum': ['click here', 'read more', 'this article', 'here', 'link', '']}}, 'properties': {'__faion_header__': {'type': ['object', 'string']}, 'site': {'type': 'string', 'pattern': '^[a-z0-9.-]+\\.[a-z]{2,}$'}, 'audit_period': {'type': 'object', 'required': ['start', 'end'], 'additionalProperties': False, 'properties': {'start': {'$ref': '#/definitions/date'}, 'end': {'$ref': '#/definitions/date'}}}, 'crawl': {'type': 'object', 'required': ['crawler', 'crawl_date', 'javascript_rendered', 'indexable_pages', 'sitemap_urls', 'cms_published_pages', 'discrepancies'], 'additionalProperties': False, 'properties': {'crawler': {'type': 'string', 'minLength': 3}, 'crawl_date': {'$ref': '#/definitions/date'}, 'javascript_rendered': {'const': True}, 'indexable_pages': {'type': 'integer', 'minimum': 30}, 'sitemap_urls': {'type': 'integer', 'minimum': 1}, 'cms_published_pages': {'type': 'integer', 'minimum': 1}, 'discrepancies': {'type': 'array', 'items': {'type': 'object', 'required': ['source', 'gap_pct', 'explanation', 'note'], 'additionalProperties': False, 'properties': {'source': {'type': 'string', 'enum': ['sitemap', 'cms']}, 'gap_pct': {'type': 'number', 'exclusiveMinimum': 5}, 'explanation': {'type': 'string', 'enum': ['robots_blocked', 'paginated', 'js_rendered', 'sitemap_stale', 'noindexed_in_cms', 'other']}, 'note': {'type': 'string', 'minLength': 10}}}}}}, 'incoming_counts': {'type': 'object', 'required': ['basis', 'pages', 'over_linked_hubs'], 'additionalProperties': False, 'properties': {'basis': {'const': 'contextual'}, 'pages': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['url', 'contextual_incoming', 'boilerplate_incoming'], 'additionalProperties': False, 'properties': {'url': {'$ref': '#/definitions/url'}, 'contextual_incoming': {'$ref': '#/definitions/count'}, 'boilerplate_incoming': {'$ref': '#/definitions/count'}}}}, 'over_linked_hubs': {'type': 'array', 'items': {'type': 'object', 'required': ['url', 'contextual_incoming', 'threshold'], 'additionalProperties': False, 'properties': {'url': {'$ref': '#/definitions/url'}, 'contextual_incoming': {'$ref': '#/definitions/count'}, 'threshold': {'type': 'integer', 'minimum': 1}}}}}}, 'orphans': {'type': 'array', 'items': {'type': 'object', 'required': ['url', 'found_via', 'contextual_incoming', 'decision'], 'additionalProperties': False, 'properties': {'url': {'$ref': '#/definitions/url'}, 'found_via': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['sitemap', 'analytics', 'crawl']}}, 'contextual_incoming': {'const': 0}, 'decision': {'type': 'string', 'enum': ['rewire', 'redirect', 'deindex']}, 'source_url': {'$ref': '#/definitions/url'}, 'anchor_text': {'type': 'string', 'minLength': 3}, 'redirect_target': {'$ref': '#/definitions/url'}}, 'allOf': [{'if': {'properties': {'decision': {'const': 'rewire'}}}, 'then': {'required': ['source_url', 'anchor_text']}}, {'if': {'properties': {'decision': {'const': 'redirect'}}}, 'then': {'required': ['redirect_target']}}]}}, 'clusters': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['pillar_url', 'cluster_pages', 'cluster_to_pillar_links', 'structurally_incomplete'], 'additionalProperties': False, 'properties': {'pillar_url': {'$ref': '#/definitions/url'}, 'cluster_pages': {'type': 'array', 'minItems': 5, 'items': {'type': 'object', 'required': ['url', 'links_to_pillar', 'pillar_links_to_it'], 'additionalProperties': False, 'properties': {'url': {'$ref': '#/definitions/url'}, 'links_to_pillar': {'type': 'boolean'}, 'pillar_links_to_it': {'type': 'boolean'}}}}, 'cluster_to_pillar_links': {'$ref': '#/definitions/count'}, 'structurally_incomplete': {'type': 'boolean'}}, 'if': {'properties': {'cluster_to_pillar_links': {'maximum': 4}}}, 'then': {'properties': {'structurally_incomplete': {'const': True}}}, 'else': {'properties': {'structurally_incomplete': {'const': False}}}}}, 'anchor_text': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['url', 'total_links', 'anchors'], 'additionalProperties': False, 'properties': {'url': {'$ref': '#/definitions/url'}, 'total_links': {'type': 'integer', 'minimum': 0}, 'anchors': {'type': 'array', 'items': {'type': 'object', 'required': ['anchor', 'count', 'share', 'generic'], 'additionalProperties': False, 'properties': {'anchor': {'type': 'string'}, 'count': {'type': 'integer', 'minimum': 1}, 'share': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'generic': {'type': 'boolean'}}, 'if': {'properties': {'anchor': {'anyOf': [{'$ref': '#/definitions/generic_anchor'}, {'pattern': '^https?://'}]}}}, 'then': {'properties': {'generic': {'const': True}}}}}}}}, 'hygiene_findings': {'type': 'array', 'items': {'type': 'object', 'required': ['source_url', 'current_target', 'final_url', 'issue'], 'additionalProperties': False, 'properties': {'source_url': {'$ref': '#/definitions/url'}, 'current_target': {'$ref': '#/definitions/url'}, 'final_url': {'$ref': '#/definitions/url'}, 'issue': {'type': 'string', 'enum': ['redirect_3xx', 'client_error_4xx', 'server_error_5xx', 'noindex_target', 'canonical_elsewhere', 'nofollow']}}}}, 'rewire_plan': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['source_url', 'target_url', 'anchor_text', 'placement', 'action', 'owner', 'due_date'], 'additionalProperties': False, 'properties': {'source_url': {'$ref': '#/definitions/url'}, 'target_url': {'$ref': '#/definitions/url'}, 'anchor_text': {'type': 'string', 'minLength': 3, 'not': {'anyOf': [{'$ref': '#/definitions/generic_anchor'}, {'pattern': '^https?://'}]}}, 'placement': {'type': 'string', 'minLength': 20}, 'action': {'type': 'string', 'enum': ['add', 'change_anchor', 'remove', 'redirect']}, 'owner': {'type': 'string', 'minLength': 2, 'not': {'enum': ['team', 'we', 'us', 'content team', 'seo team']}}, 'due_date': {'$ref': '#/definitions/date'}}}}, 'gsc_baseline': {'type': 'array', 'minItems': 1, 'items': {'type': 'object', 'required': ['url', 'clicks', 'impressions', 'average_position', 'contextual_incoming', 'window_days'], 'additionalProperties': False, 'properties': {'url': {'$ref': '#/definitions/url'}, 'clicks': {'$ref': '#/definitions/count'}, 'impressions': {'$ref': '#/definitions/count'}, 'average_position': {'type': 'number', 'minimum': 1}, 'contextual_incoming': {'$ref': '#/definitions/count'}, 'window_days': {'const': 28}}}}, 'remeasurement': {'type': 'object', 'required': ['date', 'metrics'], 'additionalProperties': False, 'properties': {'date': {'$ref': '#/definitions/date'}, 'metrics': {'type': 'array', 'minItems': 3, 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['clicks', 'impressions', 'average_position']}}}}}}

OK = {'site': 'example.com', 'audit_period': {'start': '2026-08-01', 'end': '2026-08-31'}, 'crawl': {'crawler': 'Screaming Frog SEO Spider 21', 'crawl_date': '2026-08-20', 'javascript_rendered': True, 'indexable_pages': 412, 'sitemap_urls': 430, 'cms_published_pages': 445, 'discrepancies': [{'source': 'cms', 'gap_pct': 7.4, 'explanation': 'paginated', 'note': '33 paginated archive pages are published in the CMS but carry noindex, so they are not indexable'}]}, 'incoming_counts': {'basis': 'contextual', 'pages': [{'url': 'https://example.com/guides/email-deliverability', 'contextual_incoming': 21, 'boilerplate_incoming': 412}, {'url': 'https://example.com/guides/spf-records', 'contextual_incoming': 6, 'boilerplate_incoming': 412}, {'url': 'https://example.com/guides/dmarc-setup', 'contextual_incoming': 4, 'boilerplate_incoming': 412}, {'url': 'https://example.com/blog/warmup-schedule-2024', 'contextual_incoming': 0, 'boilerplate_incoming': 412}, {'url': 'https://example.com/blog/2023-deliverability-report', 'contextual_incoming': 0, 'boilerplate_incoming': 412}, {'url': 'https://example.com/blog', 'contextual_incoming': 380, 'boilerplate_incoming': 412}], 'over_linked_hubs': [{'url': 'https://example.com/blog', 'contextual_incoming': 380, 'threshold': 100}]}, 'orphans': [{'url': 'https://example.com/blog/warmup-schedule-2024', 'found_via': ['sitemap', 'analytics'], 'contextual_incoming': 0, 'decision': 'rewire', 'source_url': 'https://example.com/guides/email-deliverability', 'anchor_text': 'a week-by-week domain warm-up schedule'}, {'url': 'https://example.com/blog/2023-deliverability-report', 'found_via': ['sitemap'], 'contextual_incoming': 0, 'decision': 'redirect', 'redirect_target': 'https://example.com/blog/2026-deliverability-report'}], 'clusters': [{'pillar_url': 'https://example.com/guides/email-deliverability', 'cluster_pages': [{'url': 'https://example.com/guides/spf-records', 'links_to_pillar': True, 'pillar_links_to_it': True}, {'url': 'https://example.com/guides/dkim-signing', 'links_to_pillar': True, 'pillar_links_to_it': True}, {'url': 'https://example.com/guides/dmarc-setup', 'links_to_pillar': True, 'pillar_links_to_it': False}, {'url': 'https://example.com/guides/bounce-handling', 'links_to_pillar': True, 'pillar_links_to_it': True}, {'url': 'https://example.com/guides/list-hygiene', 'links_to_pillar': True, 'pillar_links_to_it': True}, {'url': 'https://example.com/guides/feedback-loops', 'links_to_pillar': False, 'pillar_links_to_it': True}], 'cluster_to_pillar_links': 5, 'structurally_incomplete': False}], 'anchor_text': [{'url': 'https://example.com/guides/email-deliverability', 'total_links': 21, 'anchors': [{'anchor': 'email deliverability guide', 'count': 12, 'share': 0.571, 'generic': False}, {'anchor': 'read more', 'count': 6, 'share': 0.286, 'generic': True}, {'anchor': 'how inbox placement works', 'count': 3, 'share': 0.143, 'generic': False}]}, {'url': 'https://example.com/guides/dmarc-setup', 'total_links': 4, 'anchors': [{'anchor': 'setting up DMARC', 'count': 4, 'share': 1, 'generic': False}]}, {'url': 'https://example.com/blog/warmup-schedule-2024', 'total_links': 0, 'anchors': []}], 'hygiene_findings': [{'source_url': 'https://example.com/guides/spf-records', 'current_target': 'https://example.com/blog/old-dmarc-post', 'final_url': 'https://example.com/guides/dmarc-setup', 'issue': 'redirect_3xx'}, {'source_url': 'https://example.com/guides/list-hygiene', 'current_target': 'https://example.com/tools/bounce-checker', 'final_url': 'https://example.com/tools/bounce-checker', 'issue': 'nofollow'}], 'rewire_plan': [{'source_url': 'https://example.com/guides/email-deliverability', 'target_url': 'https://example.com/guides/dmarc-setup', 'anchor_text': 'configure a DMARC policy', 'placement': 'paragraph 4 of the Authentication section, sentence on policy enforcement', 'action': 'add', 'owner': 'Olena K.', 'due_date': '2026-09-30'}, {'source_url': 'https://example.com/guides/feedback-loops', 'target_url': 'https://example.com/guides/email-deliverability', 'anchor_text': 'the wider deliverability picture', 'placement': 'introduction, second sentence, where the pillar topic is first mentioned', 'action': 'add', 'owner': 'Olena K.', 'due_date': '2026-09-30'}, {'source_url': 'https://example.com/guides/email-deliverability', 'target_url': 'https://example.com/blog/warmup-schedule-2024', 'anchor_text': 'a week-by-week domain warm-up schedule', 'placement': 'Warm-up section, end of the first paragraph on sending volume ramps', 'action': 'add', 'owner': 'Olena K.', 'due_date': '2026-09-30'}, {'source_url': 'https://example.com/guides/spf-records', 'target_url': 'https://example.com/guides/dmarc-setup', 'anchor_text': 'setting up DMARC after SPF', 'placement': 'Next steps section, replace the link to the old DMARC post', 'action': 'change_anchor', 'owner': 'Olena K.', 'due_date': '2026-09-30'}], 'gsc_baseline': [{'url': 'https://example.com/guides/dmarc-setup', 'clicks': 410, 'impressions': 18200, 'average_position': 8.4, 'contextual_incoming': 4, 'window_days': 28}, {'url': 'https://example.com/guides/email-deliverability', 'clicks': 1930, 'impressions': 61000, 'average_position': 5.1, 'contextual_incoming': 21, 'window_days': 28}, {'url': 'https://example.com/blog/warmup-schedule-2024', 'clicks': 12, 'impressions': 900, 'average_position': 31.2, 'contextual_incoming': 0, 'window_days': 28}], 'remeasurement': {'date': '2026-11-30', 'metrics': ['clicks', 'impressions', 'average_position']}}

BAD = {'site': 'example.com', 'audit_period': {'start': '2026-08-01', 'end': '2026-08-31'}, 'crawl': {'crawler': 'in-house', 'crawl_date': '2026-05-02', 'javascript_rendered': False, 'indexable_pages': 250, 'sitemap_urls': 430, 'cms_published_pages': 445, 'discrepancies': []}, 'incoming_counts': {'basis': 'total', 'pages': [{'url': 'https://example.com/guides/email-deliverability', 'contextual_incoming': 433, 'boilerplate_incoming': 0}], 'over_linked_hubs': [{'url': 'https://example.com/blog', 'contextual_incoming': 380, 'threshold': 100}]}, 'orphans': [{'url': 'https://example.com/blog/warmup-schedule-2024', 'found_via': ['sitemap'], 'contextual_incoming': 0, 'decision': 'leave'}, {'url': 'https://example.com/blog/2023-deliverability-report', 'found_via': ['sitemap'], 'contextual_incoming': 0, 'decision': 'rewire'}], 'clusters': [{'pillar_url': 'https://example.com/guides/email-deliverability', 'cluster_pages': [{'url': 'https://example.com/guides/spf-records', 'links_to_pillar': True, 'pillar_links_to_it': False}, {'url': 'https://example.com/guides/dkim-signing', 'links_to_pillar': True, 'pillar_links_to_it': False}, {'url': 'https://example.com/guides/dmarc-setup', 'links_to_pillar': True, 'pillar_links_to_it': False}, {'url': 'https://example.com/guides/bounce-handling', 'links_to_pillar': False, 'pillar_links_to_it': False}, {'url': 'https://example.com/guides/list-hygiene', 'links_to_pillar': False, 'pillar_links_to_it': False}], 'cluster_to_pillar_links': 3, 'structurally_incomplete': False}], 'anchor_text': [{'url': 'https://example.com/guides/email-deliverability', 'total_links': 120, 'anchors': [{'anchor': 'read more', 'count': 84, 'share': 0.7, 'generic': False}, {'anchor': 'https://example.com/guides/email-deliverability', 'count': 12, 'share': 0.1, 'generic': False}]}], 'hygiene_findings': [{'source_url': 'https://example.com/guides/spf-records', 'current_target': 'https://example.com/blog/old-dmarc-post', 'final_url': 'https://example.com/guides/dmarc-setup', 'issue': 'redirect_3xx'}], 'rewire_plan': [{'source_url': 'https://example.com/guides/spf-records', 'target_url': 'https://example.com/blog', 'anchor_text': 'read more', 'placement': 'somewhere', 'action': 'strengthen', 'owner': 'team', 'due_date': '2026-09-30'}, {'source_url': 'https://example.com/guides/dkim-signing', 'target_url': 'https://example.com/blog/old-dmarc-post', 'anchor_text': 'DMARC', 'placement': 'add more links to the DMARC page where it fits', 'action': 'add', 'owner': 'content team', 'due_date': '2026-09-30'}], 'gsc_baseline': [{'url': 'https://example.com/guides/email-deliverability', 'clicks': 1930, 'impressions': 61000, 'average_position': 5.1, 'contextual_incoming': 433, 'window_days': 90}], 'remeasurement': {'date': '2026-10-05', 'metrics': ['clicks']}}


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


from datetime import date as _date


def _d(s):
    try:
        return _date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def extra(obj: dict) -> list[str]:
    """Cross-field rules from content/01-core-rules.xml the schema cannot state."""
    errs: list[str] = []
    per = obj.get("audit_period") or {}
    start, end = _d(per.get("start")), _d(per.get("end"))
    cr = obj.get("crawl") or {}
    cd = _d(cr.get("crawl_date"))
    if start and end and cd and not (start <= cd <= end):
        errs.append(f"crawl.crawl_date {cr['crawl_date']} is outside audit_period {per['start']}..{per['end']} (r-crawl-scope-reconciled)")
    idx = cr.get("indexable_pages")
    explained = {d.get("source"): d for d in cr.get("discrepancies") or [] if isinstance(d, dict)}
    for source, key in (("sitemap", "sitemap_urls"), ("cms", "cms_published_pages")):
        n = cr.get(key)
        if _num(idx) and _num(n) and n > 0:
            gap = abs(idx - n) / n * 100
            if gap > 5 and source not in explained:
                errs.append(f"crawl: indexable_pages {idx} vs {key} {n} is a {gap:.1f} percent gap with no discrepancies[] entry for {source} (r-crawl-scope-reconciled)")
            elif source in explained and _num(explained[source].get("gap_pct")) and abs(explained[source]["gap_pct"] - gap) > 0.15:
                errs.append(f"crawl.discrepancies[{source}].gap_pct {explained[source]['gap_pct']} is not |{idx} - {n}| / {n} = {gap:.1f} (r-crawl-scope-reconciled)")
    plan = [i for i in obj.get("rewire_plan") or [] if isinstance(i, dict)]
    edges = {(i.get("source_url"), i.get("target_url")) for i in plan}
    targets = {i.get("target_url") for i in plan}
    for n, o in enumerate(obj.get("orphans") or []):
        if o.get("decision") == "rewire" and (o.get("source_url"), o.get("url")) not in edges:
            errs.append(f"orphans[{n}] {o.get('url')}: decision rewire but no rewire_plan item from {o.get('source_url')} to it (r-orphan-gets-a-decision)")
    for n, c in enumerate(obj.get("clusters") or []):
        pages = [p for p in c.get("cluster_pages") or [] if isinstance(p, dict)]
        got = sum(1 for p in pages if p.get("links_to_pillar") is True)
        if c.get("cluster_to_pillar_links") != got:
            errs.append(f"clusters[{n}].cluster_to_pillar_links {c.get('cluster_to_pillar_links')} is not the count of links_to_pillar true = {got} (r-pillar-cluster-reciprocity)")
        for p in pages:
            if p.get("links_to_pillar") is False and (p.get("url"), c.get("pillar_url")) not in edges:
                errs.append(f"clusters[{n}]: {p.get('url')} does not link to the pillar and no rewire_plan item adds that edge (r-pillar-cluster-reciprocity)")
            if p.get("pillar_links_to_it") is False and (c.get("pillar_url"), p.get("url")) not in edges:
                errs.append(f"clusters[{n}]: the pillar does not link to {p.get('url')} and no rewire_plan item adds that edge (r-pillar-cluster-reciprocity)")
    anchors_for = {a.get("url"): a for a in obj.get("anchor_text") or [] if isinstance(a, dict)}
    for url, a in anchors_for.items():
        total = a.get("total_links")
        for k, row in enumerate(a.get("anchors") or []):
            if _num(total) and total > 0 and _num(row.get("count")) and _num(row.get("share")) and abs(row["share"] - row["count"] / total) > 0.0051:
                errs.append(f"anchor_text[{url}].anchors[{k}].share {row['share']} is not count / total_links = {row['count'] / total:.3f} (r-anchor-text-descriptive)")
    for t in sorted(x for x in targets if isinstance(x, str)):
        if t not in anchors_for:
            errs.append(f"rewire target {t} has no anchor_text entry (r-anchor-text-descriptive)")
        new = [i.get("anchor_text") for i in plan if i.get("target_url") == t and i.get("action") == "add"]
        if len(new) >= 2 and len(set(new)) == 1:
            errs.append(f"rewire target {t}: {len(new)} new links all carry the identical anchor {new[0]!r} (r-anchor-text-descriptive)")
    bad_targets = {h.get("current_target") for h in obj.get("hygiene_findings") or [] if isinstance(h, dict)}
    hubs = {h.get("url") for h in (obj.get("incoming_counts") or {}).get("over_linked_hubs") or [] if isinstance(h, dict)}
    for n, i in enumerate(plan):
        if i.get("target_url") in bad_targets:
            errs.append(f"rewire_plan[{n}].target_url {i['target_url']} is a hygiene finding's current_target; link to the final URL (r-link-targets-final-url)")
        if i.get("target_url") in hubs:
            errs.append(f"rewire_plan[{n}].target_url {i['target_url']} is an over-linked hub (r-rewire-item-fully-specified)")
    baselined = {b.get("url") for b in obj.get("gsc_baseline") or [] if isinstance(b, dict)}
    for t in sorted(x for x in targets if isinstance(x, str)):
        if t not in baselined:
            errs.append(f"rewire target {t} has no gsc_baseline row (r-pre-post-search-console-baseline)")
    dues = [d for d in (_d(i.get("due_date")) for i in plan) if d]
    rm = _d((obj.get("remeasurement") or {}).get("date"))
    if dues and rm and (rm - max(dues)).days < 56:
        errs.append(f"remeasurement.date {rm} is {(rm - max(dues)).days} days after the last due_date {max(dues)}; at least 56 required (r-pre-post-search-console-baseline)")
    return errs


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    _check(obj, SCHEMA, "$", errs)
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
        prog="validate-internal-link-audit.py",
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
