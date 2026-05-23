---
slug: alert-triage-decision-tree
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Deterministic decision tree for on-call alert triage: maps alert signal (severity, blast radius, freshness) to a routing decision (page / async / autosuppress) with named owner and SLA.
content_id: "af9ed17dedc1b034"
complexity: medium
produces: decision-record
est_tokens: 4000
tags: [incident, alerting, on-call, decision-tree, sdlc-ai]
---
# Alert Triage Decision Tree

## Summary

**One-sentence:** Deterministic decision tree for on-call alert triage: maps alert signal (severity, blast radius, freshness) to a routing decision (page / async / autosuppress) with named owner and SLA.

**One-paragraph:** Pager fatigue kills incident response. Most teams either page-everything (humans go numb) or hand-tune alerts forever (drift wins). This methodology installs a deterministic triage tree run by the on-call AI agent (or the on-call human) on every fresh alert: classify severity from signal (saturation, error rate, customer-impact proxy), check blast radius, check freshness, then route — page, async ticket, or auto-suppress with audit. Output is a JSON triage record per alert with route + owner + SLA, written to the audit log.

**Ефективно для:**

- Team operates a production system with a paging surface (PagerDuty, Opsgenie, Splunk On-Call).
- Alert volume exceeds 10/day or pager-skip rate exceeds 20%.
- There is an on-call rotation with a defined SLA per severity tier.

## Applies If (ALL must hold)

- Team operates a production system with a paging surface (PagerDuty, Opsgenie, Splunk On-Call).
- Alert volume exceeds 10/day or pager-skip rate exceeds 20%.
- There is an on-call rotation with a defined SLA per severity tier.

## Skip If (ANY kills it)

- Team has zero paging surface (alerts go to a chat channel that nobody owns).
- Service is not production — staging-only alerts go to logs, not the tree.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Alert payload | json | Alertmanager / Datadog webhook |
| Service catalog | yaml | Team `services.yaml` with owners + severity tiers |
| Runbook index | yaml | Team `runbooks.yaml` with runbook URL per alert name |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-alert-triage-decision-tree` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/triage-record.json` | Triage record skeleton |
| `templates/tree-config.yaml` | Triage tree configuration YAML |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-alert-triage-decision-tree.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
