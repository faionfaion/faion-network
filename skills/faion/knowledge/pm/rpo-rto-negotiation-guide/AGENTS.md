# RPO/RTO Negotiation Guide

## Summary

**One-sentence:** A scripted four-step negotiation framework (impact-quantification → cost-curve → tier-banding → signed acceptance) that turns RPO/RTO from engineering invention into an explicit product-vs-cost decision owned by the stakeholder who actually pays for downtime.

**One-paragraph:** RPO/RTO is a business decision dressed up as a technical one. When the architect picks the numbers alone, the team either over-spends on infrastructure or under-protects the business. This methodology forces the conversation: present cost-of-downtime BEFORE infrastructure cost, present ≥3 banded options each with RPO/RTO + cost delta + operational impact, force a signed acceptance record with stakeholder's own words, refresh annually. Output is a typed `AcceptanceRecord` per system carrying system_id, chosen_rpo, chosen_rto, cost_band, stakeholder_handle, evidence_link, refresh_due.

**Ефективно для:**

- New system / major rearchitecture / DR plan refresh needing explicit RPO/RTO numbers.
- Architect-vs-stakeholder negotiation with budget authority present.
- Decision audit trail for cost-of-downtime + agreed targets.
- Annual refresh as customer expectations + infra unit economics change.

## Applies If (ALL must hold)

- New system / rearchitecture / DR plan refresh is in scope and needs explicit RPO/RTO numbers.
- ≥ 1 named business stakeholder with budget authority for the system.
- Architect can sketch a cost-curve (cost as function of RPO/RTO target).
- Tier == pro or higher.

## Skip If (ANY kills it)

- Regulated context (banking, healthcare) with regulator-mandated RPO/RTO — adopt mandate and document.
- Throwaway prototype with no production users.
- No budget authority present — defer; do not negotiate against an empty chair.
- No cost-curve data — instrument first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Systems in scope + current observed RPO/RTO | YAML | architect |
| Cost-curve ≥ 3 points (current, +1 tier, +2 tier) | YAML | finance + architect |
| Impact data (revenue/hour, transactions/hour, SLA penalty) | CSV / analytics export | finance |
| Stakeholder w/ budget authority + 60 min | calendar | sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[regulatory-uncertainty-buffer]] | Regulated systems mandate RPO/RTO floor before negotiation. |
| [[rag-policy-thresholds]] | RPO/RTO breaches feed Red signal in status reporting. |
| [[saas-stack-audit-micro-agency]] | Cost-band tier choices interact with SaaS spend. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: stakeholder-owns-number, impact-before-cost, tier-banded-options, signed-acceptance-record, refresh-cadence | ~1150 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `AcceptanceRecord` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 4-step negotiation + 1-step refresh: impact → cost-curve → options → signed → annual refresh | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: regulatory mandate? stakeholder present? cost-curve data? → mandate-adopt / negotiate / defer | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `quantify-impact` | sonnet | Revenue / SLA penalty math + sponsor-facing copy. |
| `present-tier-bands` | sonnet | 3 banded options synthesis with cost delta + operational impact. |
| `capture-acceptance` | haiku | Mechanical transcribe of stakeholder's own words + signature. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | AcceptanceRecord skeleton with default tier-bands |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `AcceptanceRecord` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rpo-rto-negotiation-guide.py` | Validate `AcceptanceRecord`: ≥3 options presented, stakeholder echo, refresh ≤12mo, signed | Pre-merge |
| `scripts/staleness-check.py` | Flag records whose `refresh_due` passed | Weekly cron |

## Related

- [[regulatory-uncertainty-buffer]]
- [[rag-policy-thresholds]]
- [[saas-stack-audit-micro-agency]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps presence of regulator mandate, stakeholder availability, cost-curve data, and refresh status to mandate-adopt / negotiate / defer / refresh. Every leaf references a rule from `01-core-rules.xml`.
