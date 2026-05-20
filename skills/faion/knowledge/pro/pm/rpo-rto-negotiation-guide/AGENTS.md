---
slug: rpo-rto-negotiation-guide
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: RPO/RTO Negotiation Guide: structures the product-vs-cost conversation between architect and business stakeholders so DR targets are chosen by the buyer, not invented by engineering.
content_id: "c6bc454256fe2ef2"
tags: [rpo-rto-negotiation-guide, pm, pro]
---
# RPO/RTO Negotiation Guide

## Summary

**One-sentence:** A scripted negotiation framework that turns Recovery Point Objective and Recovery Time Objective from an engineering invention into an explicit product-vs-cost trade-off owned by the stakeholder who actually pays for downtime.

**One-paragraph:** RPO/RTO is a business decision dressed up as a technical one. When the architect picks the numbers alone, the team builds expensive infrastructure for a tolerance the business never asked for, or — worse — builds cheap infrastructure for a tolerance the business cannot survive. This methodology gives the architect the conversation: a four-step structure (impact-quantification → cost-curve presentation → tier-banding → signed acceptance) plus the specific questions that force the stakeholder to own the chosen number. Output is a signed RPO/RTO commitment record per system, with the cost-curve evidence attached, that downstream design and procurement decisions can cite as authority.

## Applies If (ALL must hold)

- a new system, major rearchitecture, or DR plan refresh is in scope and needs explicit RPO/RTO numbers
- there is at least one named business stakeholder with budget authority for the system
- the architect can produce or sketch a cost-curve (cost as a function of RPO/RTO target)
- tier == pro or higher

## Skip If (ANY kills it)

- regulated context (banking, healthcare) where regulator-mandated RPO/RTO supersedes any negotiation — adopt the mandate and document
- the system is a throwaway prototype with no production users
- there is no budget authority present — defer the conversation; do not negotiate against an empty chair

## Prerequisites

- list of systems in scope and their current observed RPO/RTO (if measured)
- rough cost curve: at least three points (current, +1 tier, +2 tiers) with annual cost delta
- impact data: revenue/hour-of-downtime estimate or proxy (transactions/hour, support cost, SLA penalty)
- named stakeholder with budget authority and at least 60 minutes booked

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill |
| `pro/infra/dr-drill-scenario-library` | the drill mechanics the negotiated numbers will be validated against |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: stakeholder-owns-number, impact-before-cost, tier-banded-options, signed-acceptance-record, refresh-cadence | ~1150 |

## Related

- parent skill: `pro/pm/project-manager`
- upstream playbook: `role-software-architect/Disaster-recovery plan + live drill`
- sibling methodology: `pro/infra/rto-rpo-measurement-template`
