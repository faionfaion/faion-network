---
slug: key-trends-summary
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Orientation reference covering six major shifts relevant to SDD practitioners: SDD becoming the dominant paradigm for AI-assisted development (intent → spec → plan → execute → review); docs-as-code and LLM-optimized documentation; ADRs as standard practice at AWS, Google Cloud, and Microsoft Azure; LLM-first workflows (context packing, spec-first, agentic MCP); platform engineering growth (45% → 80% of large orgs by 2026); OpenTelemetry as the #2 CNCF project for observability.
content_id: "957157a8f69bccfc"
tags: [sdd, trends, architecture, platform-engineering, observability]
---
# Key Trends Summary 2025-2026

## Summary

**One-sentence:** Orientation reference covering six major shifts relevant to SDD practitioners: SDD becoming the dominant paradigm for AI-assisted development (intent → spec → plan → execute → review); docs-as-code and LLM-optimized documentation; ADRs as standard practice at AWS, Google Cloud, and Microsoft Azure; LLM-first workflows (context packing, spec-first, agentic MCP); platform engineering growth (45% → 80% of large orgs by 2026); OpenTelemetry as the #2 CNCF project for observability.

**One-paragraph:** Orientation reference covering six major shifts relevant to SDD practitioners: SDD becoming the dominant paradigm for AI-assisted development (intent → spec → plan → execute → review); docs-as-code and LLM-optimized documentation; ADRs as standard practice at AWS, Google Cloud, and Microsoft Azure; LLM-first workflows (context packing, spec-first, agentic MCP); platform engineering growth (45% → 80% of large orgs by 2026); OpenTelemetry as the #2 CNCF project for observability. Load at the start of architectural planning sessions, not per-task.

## Applies If (ALL must hold)

- At the start of an architectural planning session, before drafting constitution.md, roadmap.md, or any new spec.md
- When a human asks what tools to use for SDD/documentation in 2025-2026 (Kiro, Tessl, Spec Kit, MCP, Backstage, Port, Cortex)
- As context before quarterly roadmap or constitution-revision sessions
- When evaluating whether to adopt a new tool category (developer portal, observability stack, LLM workflow)
- When an ADR cites a market-share or adoption claim — load this doc to verify the claim has a recorded source date

## Skip If (ANY kills it)

- As a replacement for methodology-specific docs — use dedicated methodology folders for actionable guidance
- For time-sensitive tool decisions — this is a snapshot; verify market share data currency before committing
- For domains not covered here (the doc covers SDD, ADRs, living docs, platform engineering, observability)
- When the agent already has current context from a more specific source loaded this session
- Per-task — loading on every TASK_ execution wastes tokens; load once per session and rely on planning-time context

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

- parent skill: `solo/sdd/sdd/`
