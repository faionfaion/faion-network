---
slug: devops-elk-index-management
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces ES index management config: index templates (mappings + settings) + ILM policy (hot→warm→cold→delete via rollover) + write alias for time-series logs.
content_id: "89ddd06ae458f015"
complexity: medium
produces: config
est_tokens: 4200
tags: [elasticsearch, ilm, index-management, logging, devops]
---

# Elasticsearch Index Lifecycle Management and Templates

## Summary

**One-sentence:** Produces ES index management config: index templates (mappings + settings) + ILM policy (hot→warm→cold→delete via rollover) + write alias for time-series logs.

**One-paragraph:** Without ILM, engineers manually delete old indices, causing accidental data loss or cluster-red from disk exhaustion. Without index templates, each new index inherits ES defaults (too many shards + wrong field types). Rollover aliases decouple write target from physical index name. This methodology produces the three artefacts: component templates + index template, an ILM policy with hot/warm/cold/delete phases driven by max_age + max_size, and a write alias bound to the policy. Output replaces all manual index management.

**Ефективно для:**

- Production ES cluster з time-series logs + retention period.
- New log source — index growing beyond one index.
- Migration з daily-naming (logs-2025.01.15) → size-based rollover.
- Storage cost reduction — aging data → warm/cold tiers.

## Applies If (ALL must hold)

- Data is time-series (logs / metrics / traces with @timestamp).
- Retention policy is defined (days or storage cap).
- Cluster has multiple tiers (hot-warm-cold) OR plans to add them.

## Skip If (ANY kills it)

- Dev / throwaway cluster — plain indices simpler.
- Static dataset (imported once, never updated) — use snapshot/restore.
- Single-tier cluster + retention < 7 days — ILM overhead not justified.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Retention policy | days per data stream | GRC / app team |
| Tier topology | hot/warm/cold node availability | see devops-elk-architecture |
| Index name pattern | logs-*, metrics-* etc. | naming convention |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[devops-elk-architecture]] | Tier topology comes from there |
| [[devops-elk-beats-collection]] | Ingest agents write into the alias |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: index-template-before-data, ilm-policy-required, rollover-by-size-or-age, write-alias-bound, shard-count-bounded, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for ILM + template config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: no-template-default-mapping, daily-index-without-rollover, no-ilm-manual-delete, oversharded-cluster | 800 |
| `content/04-procedure.xml` | essential | 5 steps: template → ILM policy → write alias → bootstrap first index → verify rollover | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on retention + volume → policy phases | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-template` | sonnet | Component + index template composition. |
| `design-ilm` | sonnet | Phase config + transitions. |
| `validate-shards` | haiku | Shard count math against best-practice. |

## Templates

| File | Purpose |
|------|---------|
| `templates/index-template.json` | Index template + component templates for logs-* |
| `templates/ilm-policy.json` | ILM policy: hot (rollover 50G or 7d) → warm 30d → cold 60d → delete 90d |
| `templates/bootstrap.sh` | Bootstrap script: create policy + template + initial index + write alias |
| `templates/_smoke-test.json` | Minimum config used by validate-devops-elk-index-management.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-elk-index-management.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[devops-elk-architecture]]
- [[devops-elk-beats-collection]]
- [[devops-elk-logstash-pipeline]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when wiring index management on a new ES cluster.
