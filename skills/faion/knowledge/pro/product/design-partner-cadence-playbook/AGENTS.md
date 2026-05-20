---
slug: design-partner-cadence-playbook
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4966a9ca2c4bbcb2"
summary: Design Partner Cadence Playbook delivers a concrete, testable methodology that turns the recurring task of 'Customer demo / sneak-peek session' into an auditable artefact, addressing the gap: Pro/geek-tier B2B PMs need a methodology for running an ongoing design-partner cohort (c
tags: [product, pro, template, methodology]
---
# Design Partner Cadence Playbook

## Summary

**One-sentence:** Design Partner Cadence Playbook delivers a concrete, testable methodology that turns the recurring task of 'Customer demo / sneak-peek session' into an auditable artefact, addressing the gap: Pro/geek-tier B2B PMs need a methodology for running an ongoing design-partner cohort (cadence, incentives, NDAs, escalation path).

**One-paragraph:** Pro/geek-tier B2B PMs need a methodology for running an ongoing design-partner cohort (cadence, incentives, NDAs, escalation path). Design Partner Cadence Playbook closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Customer demo / sneak-peek session' (role-product-manager, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Customer demo / sneak-peek session' (role: role-product-manager) is in your current workload at least once per cycle.
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
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
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
| `design_partner_cadence_playbook_template_fill` | haiku | Template fill, no judgment |
| `design_partner_cadence_playbook_evidence_check` | sonnet | Bounded comparison + judgment |
| `design_partner_cadence_playbook_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/product/` (see neighbouring methodologies)
- triggering activity: `role-product-manager/Customer demo / sneak-peek session`
- external: industry references cited inline in `content/01-core-rules.xml`
