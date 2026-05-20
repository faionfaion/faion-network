---
slug: modern-ba-framework
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A meta-framework for applying the six BABOK Knowledge Areas to modern delivery contexts: agile, AI/ML, cloud-native, platform engineering, and process-mining.
content_id: "2eca489bf32c2da9"
tags: [babok, ba-framework, meta-framework, agile, perspective-routing]
---
# Modern BA Framework: BABOK for Agile, AI/ML, Cloud, and Platform Delivery

## Summary

**One-sentence:** A meta-framework for applying the six BABOK Knowledge Areas to modern delivery contexts: agile, AI/ML, cloud-native, platform engineering, and process-mining.

**One-paragraph:** A meta-framework for applying the six BABOK Knowledge Areas to modern delivery contexts: agile, AI/ML, cloud-native, platform engineering, and process-mining. The deliverable for an agent is not "do BA" but a routing decision — a ba-approach.json that picks methodologies per KA, declares delivery perspective (Agile/BI/IT/BizArch/BPM/Data-Product/AI-Product), maps per-task model tiers, and requires human PO sign-off before execution. The framework also maps team competencies against ECBA/CCBA/CBAP/AAC/CBDA/CPOA and SFIA v9.

## Applies If (ALL must hold)

- Onboarding a new BA or PO: agent reads project context and emits a tailored BA approach that selects methodologies per KA and perspective.
- Migration audits: shifting from waterfall BABOK artifacts to agile/lean BA equivalents.
- Certification-aligned skill assessment: scoring a team against BABOK certifications and SFIA v9.
- Multi-perspective discovery: work spanning Agile + BI + Business Architecture simultaneously.
- Model selection routing: assigning haiku/sonnet/opus per task type (format → haiku, AC → sonnet, gap analysis → opus).
- Trigger phrases from the user: "design a BA approach", "how should we run BA on this", "modernize our BA process", "set up BA for an AI project", "competency gap analysis".

## Skip If (ANY kills it)

- A specific BA task is already scoped — load the concrete sibling methodology directly (acceptance-criteria, elicitation-techniques, business-process-analysis).
- Pure non-BA work (code refactor, infra hardening) — the framework manufactures BA scaffolding nobody asked for.
- Solo founders with no enterprise team — the routing value collapses to a single perspective.
- Greenfield product discovery before stakeholders or a problem statement exist — use continuous-discovery first.

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
