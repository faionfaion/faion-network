---
slug: requirements-traceability
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Requirements traceability links every artifact (business requirement, stakeholder requirement, solution requirement, design, code, test) to its origin and its downstream dependents, enabling forward coverage analysis (need → test) and backward justification (test → need).
content_id: "5c8b6df0fd700d15"
tags: [traceability, requirements, rtm, coverage, impact-analysis]
---
# Requirements Traceability Matrix (RTM) Generation and Maintenance

## Summary

**One-sentence:** Requirements traceability links every artifact (business requirement, stakeholder requirement, solution requirement, design, code, test) to its origin and its downstream dependents, enabling forward coverage analysis (need → test) and backward justification (test → need).

**One-paragraph:** Requirements traceability links every artifact (business requirement, stakeholder requirement, solution requirement, design, code, test) to its origin and its downstream dependents, enabling forward coverage analysis (need → test) and backward justification (test → need). The RTM is a generated artifact, not a hand-edited file: typed links in source artifact frontmatter (`traces: [BR-05, SR-12]`) feed a generator script that builds the matrix and computes coverage metrics. Agents propose links, detect orphans, and walk the graph for impact analysis — they never write the matrix directly.

## Applies If (ALL must hold)

- Regulated builds (ISO 13485, IEC 62304, ISO 26262, DO-178C, SOX) where auditors demand a complete chain
- Multi-team programs where a single change request hits four or more artifact types
- Pairing with requirements-lifecycle and requirements-validation to close the Specify → Verify loop with coverage numbers
- Migrations where every legacy capability must be provably preserved or explicitly retired
- Vendor/outsourced delivery where the RTM is the contractual acceptance deliverable

## Skip If (ANY kills it)

- Pre-PMF/discovery work — opportunity-solution-trees and lightweight user stories suffice; an RTM ossifies premature decisions
- Solo developer or 2-person team — git log --grep plus issue links already provide enough trace
- Pure infrastructure/SRE work where requirements are SLOs, not features
- When the team will not enforce maintenance discipline — an outdated RTM gives false assurance to auditors

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
