---
slug: trade-off-quality-attributes
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Quality attributes often conflict: improving one typically degrades another.
content_id: "89a0d4e28402a57d"
tags: [quality-attributes, iso-25010, cap-theorem, architecture-styles, trade-off]
---
# Quality Attribute Trade-offs in Architecture

## Summary

**One-sentence:** Quality attributes often conflict: improving one typically degrades another.

**One-paragraph:** Quality attributes often conflict: improving one typically degrades another. This methodology covers the ISO 25010 model, common attribute conflict pairs, architecture style trade-offs (monolith vs microservices), CAP theorem data trade-offs, and communication pattern trade-offs as the factual basis for any trade-off decision. Includes a strict trigger list, a step-by-step how-to, a copy-paste ADR template, lift-and-paste prompts and a verify checklist.

## Applies If (ALL must hold)

- Building quality attribute scenarios for ATAM or filling a decision matrix — to identify which pairs are in tension.
- Evaluating architecture style options (monolith, modular monolith, microservices, serverless, event-driven).
- Selecting a data storage strategy where consistency must be weighed against availability or partition tolerance.
- Designing service-to-service communication (sync REST/gRPC vs async queues vs event-driven brokers).
- Writing the "Consequences" section of an ADR — to enumerate explicit gain/loss pairs.
- Reviewing a proposed change whose description contains any of: "scale", "low latency", "always available", "encrypt", "decouple", "extract service", "introduce queue", "switch DB", "rewrite", "cold start".

## Skip If (ANY kills it)

- As a substitute for context-specific analysis — these tables are starting points, not verdicts. Your system's actual trade-offs may differ.
- When a single quality attribute clearly dominates all others for your use case — simplify instead of balancing a full ISO 25010 analysis.
- For pure code-style or formatting decisions with no runtime quality impact.

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

- parent skill: `solo/dev/software-architect/`
