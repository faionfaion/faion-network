---
slug: go-layout-agentic-workflow
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Drive Go service scaffolding as a four-stage pipeline: layout agent generates the skeleton, code-gen agent emits handler/service/repository/model per resource, wiring agent assembles main.
content_id: "fd9d99cb4a356468"
tags: [go, agentic-workflow, scaffolding, llm-prompts]
---
# Go Standard Layout — Agentic Workflow and Prompts

## Summary

**One-sentence:** Drive Go service scaffolding as a four-stage pipeline: layout agent generates the skeleton, code-gen agent emits handler/service/repository/model per resource, wiring agent assembles main.

**One-paragraph:** Drive Go service scaffolding as a four-stage pipeline: layout agent generates the skeleton, code-gen agent emits handler/service/repository/model per resource, wiring agent assembles main.go, review agent runs the import-rule checklist. Pair with persistent stack decisions in .aidocs/ to stop agents re-deciding per PR.

## Applies If (ALL must hold)

- Scaffolding a new Go service with multiple resources (3 or more domain entities) using an AI agent.
- Multi-agent sessions where different agents handle layout, code-gen, wiring, and review independently.
- Teams that want a repeatable, auditable agentic workflow instead of a free-form "write me a Go service" prompt.
- Onboarding agents to an existing Go codebase that already follows the standard layout.

## Skip If (ANY kills it)

- Simple one-endpoint or one-binary scripts — a four-stage pipeline is overkill; use a single prompt.
- Agents working on a codebase that does not follow the standard layout — apply only the review-agent stage.

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

- parent skill: `pro/dev/backend-systems/`
