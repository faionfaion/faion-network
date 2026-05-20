---
slug: dormant-lead-reactivation
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5e4a389171a579f4"
summary: Dormant Lead Reactivation delivers a concrete, testable methodology that turns the recurring task of 'Quarterly portfolio rebalance (cash, clients, capacity)' into an auditable artefact, addressing the gap: Reactivation sequence specifically for service-business dormant pipelines
tags: [marketing, pro, method, methodology]
---
# Dormant Lead Reactivation

## Summary

**One-sentence:** Dormant Lead Reactivation delivers a concrete, testable methodology that turns the recurring task of 'Quarterly portfolio rebalance (cash, clients, capacity)' into an auditable artefact, addressing the gap: Reactivation sequence specifically for service-business dormant pipelines (past clients + lost proposals + nurture leads) — different beat from B2C reactivation.

**One-paragraph:** Reactivation sequence specifically for service-business dormant pipelines (past clients + lost proposals + nurture leads) — different beat from B2C reactivation. Dormant Lead Reactivation closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Quarterly portfolio rebalance (cash, clients, capacity)' (p3-technical-freelancer, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Quarterly portfolio rebalance (cash, clients, capacity)' (role: p3-technical-freelancer) is in your current workload at least once per cycle.
- You have authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the artefact — human reviewer OR downstream agent.
- An auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems / dashboards / docs that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `dormant_lead_reactivation_template_fill` | haiku | Template fill, no judgment |
| `dormant_lead_reactivation_evidence_check` | sonnet | Bounded comparison + judgment |
| `dormant_lead_reactivation_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/marketing/` (see neighbouring methodologies)
- triggering activity: `p3-technical-freelancer/Quarterly portfolio rebalance (cash, clients, capacity)`
- external: industry references cited inline in `content/01-core-rules.xml`
