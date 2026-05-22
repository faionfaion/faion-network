---
slug: incident-comms-templates-internal-external
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Ships ready-to-edit incident comms templates (status page + customer email + exec brief + internal channel) so outage minute-cost is not template-authoring time."
content_id: "a1ea8f0787cbf863"
complexity: light
produces: spec
est_tokens: 3200
tags: [pm, incident-management, comms-templates, outage, status-page]
---
# Incident Comms Templates Internal External

## Summary

**One-sentence:** Ships ready-to-edit incident comms templates (status page + customer email + exec brief + internal channel) so outage minute-cost is not template-authoring time.

**One-paragraph:** Ships ready-to-edit incident comms templates (status page + customer email + exec brief + internal channel) so outage minute-cost is not template-authoring time. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM/IM-у під час інциденту — шаблони готові, не треба писати з нуля під тиском.

## Applies If (ALL must hold)

- Org runs a service with paying customers OR a published SLA.
- Incidents happen often enough that ad-hoc comms cost is real (>=1 P1/P2 per quarter).
- An incident-commander role exists (named, on a rotation).
- Status-page tool and customer-comms channel are in place.

## Skip If (ANY kills it)

- Pre-launch product with no SLA — defer until customers exist.
- No on-call rotation — templates without a commander rot.
- Org has a regulated template (banking, healthcare) — use the regulator's instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Status-page tool access | API/UI | Statuspage / Atlassian Statuspage / equivalent |
| Customer comms list | CRM export | support tool |
| Exec brief recipients | list | leadership roster |
| Severity definitions | doc | incident-management runbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/distressed-project-diagnostic-script` | Project-level rescue — incident templates plug into it. |
| `geek/pm/exception-driven-standup-protocol` | Companion ritual for post-incident standups. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-template-bundle` | haiku | Boilerplate fill across the four templates. |
| `severity-audience-mapping` | sonnet | Bounded judgement: which placeholders per severity. |
| `post-incident-narrative` | opus | Cross-channel synthesis for customer + exec. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Four-template bundle: status-page update, customer email, exec brief, internal channel — each with severity-aware placeholders. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-incident-comms-templates-internal-external.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[distressed-project-diagnostic-script]]
- [[exception-driven-standup-protocol]]
- [[delivery-maturity-rubric]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to ship the template bundle (paid service + recurring incidents + commander), block until commander rotation exists, or skip (pre-launch / no incidents). Run before authoring any template.
