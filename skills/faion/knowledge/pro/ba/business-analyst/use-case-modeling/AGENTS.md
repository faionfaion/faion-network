---
slug: use-case-modeling
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use case modeling captures WHO interacts with a system, WHAT they do with it, and WHY — as a sequence of actor-system interactions that yields observable value.
content_id: "a8b8106842b7d773"
tags: [use-case-modeling, requirements, uml, specifications, enterprise-ba]
---
# Use Case Modeling

## Summary

**One-sentence:** Use case modeling captures WHO interacts with a system, WHAT they do with it, and WHY — as a sequence of actor-system interactions that yields observable value.

**One-paragraph:** Use case modeling captures WHO interacts with a system, WHAT they do with it, and WHY — as a sequence of actor-system interactions that yields observable value. Each use case has a name (Verb + Noun), a primary actor, a main flow (5-9 steps), at least one alternative flow, and at least one exception flow. The deliverable is a UC spec plus a UC diagram showing actor-system boundaries. Use-case-driven BA is contractual: the UC catalog becomes the apples-to-apples grid for vendor evaluation and the traceability anchor for regulated-industry audits.

## Applies If (ALL must hold)

- Enterprise kickoffs requiring a UML UC diagram + UC specs as SoW deliverables (SAP, Salesforce, Dynamics rollouts, banking core upgrades)
- RFP/RFI authoring — UC catalog is the vendor evaluation grid
- RUP-style use-case-driven projects in regulated or government contexts where iterations are scoped to UC sets
- Regulated industries where UCs anchor actor goal → step → commit → test → audit evidence
- Legacy migration (mainframe, Oracle Forms) where reverse-engineering screens into UCs is the safe path to a greenfield spec
- Outsourced delivery where step-level UC specs replace ambient context the offshore team lacks
- Stakeholder alignment workshops bridging executive outcomes and engineering features

## Skip If (ANY kills it)

- Lean/startup contexts — JTBD, Opportunity Solution Trees, or story mapping deliver faster discovery without SoW UC obligations
- Data/analytics platforms — DFDs and dimensional models better expose the meaningful structure
- Internal tools with a single actor and fewer than 10 transactions — a one-page acceptance-criteria sheet suffices
- ML/LLM surfaces with probabilistic responses — UC main flows assume deterministic system responses and mislead
- Event-sourced/reactive architectures — event storming better exposes the structure
- Teams already running smoothly on user stories + acceptance criteria — layering UCs duplicates work

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ba/business-analyst/`
