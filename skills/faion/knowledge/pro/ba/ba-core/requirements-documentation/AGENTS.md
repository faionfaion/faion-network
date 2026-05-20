---
slug: requirements-documentation
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Produce sign-off-ready requirements sets (BRD + URS + SRS/FRD) aligned to a single locked standard (IEEE 830-1998 or ISO/IEC/IEEE 29148:2018).
content_id: "0b8ba53b7d51c38b"
tags: [requirements, documentation, brd, srs, ears]
---
# Requirements Documentation

## Summary

**One-sentence:** Produce sign-off-ready requirements sets (BRD + URS + SRS/FRD) aligned to a single locked standard (IEEE 830-1998 or ISO/IEC/IEEE 29148:2018).

**One-paragraph:** Produce sign-off-ready requirements sets (BRD + URS + SRS/FRD) aligned to a single locked standard (IEEE 830-1998 or ISO/IEC/IEEE 29148:2018). Write functional requirements in EARS patterns (Ubiquitous, Event-driven, State-driven, Optional, Unwanted-behaviour, Complex). Validate structure via a YAML conformance schema before any document is rendered to PDF. Source is Markdown with frontmatter; the PDF is a generated artifact via pandoc.

## Applies If (ALL must hold)

- Producing a classical, sign-off-ready requirements set for regulated work (IEC 62304, ISO 26262, DO-178C, BCBS 239, SOC2 audits)
- A vendor or client contract names a specific standard (IEEE 830, ISO 29148, IREB CPRE) and the deliverable list is fixed
- Hand-off across organizations where the document is the contract artifact
- Re-baselining: a previously approved pack must be re-issued at v2.0 with a redline, changelog, and fresh sign-off
- Auditors will physically read a PDF expecting: cover page, version table, approval block, glossary, traceability matrix, requirement IDs

## Skip If (ANY kills it)

- Solo or agile project where spec.md + acceptance tests already cover the audit surface
- Team has no document custodian — without a named owner the formal apparatus rots within two sprints
- Discovery work where requirements are still volatile — formal docs imply a baseline; baselining in flux is theatre
- Internal tooling for one team — lightweight user stories are sufficient
- The reviewer pool will not actually sign — unsigned formal docs are worse than informal ones

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

- parent skill: `pro/ba/ba-core/`
