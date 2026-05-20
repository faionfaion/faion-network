---
slug: templates
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Eight copy-paste templates for Specification-Driven Development: constitution (tech stack and constraints), spec (requirements and user stories), design (architecture and decisions), test-plan (verification per acceptance criterion), implementation-plan (task breakdown and order), task (single executable unit), roadmap (feature timeline and metrics), and memory (patterns and lessons).
content_id: "180a580e913ae900"
tags: [sdd, templates, documentation, planning, task-management]
---
# SDD Document Templates

## Summary

**One-sentence:** Eight copy-paste templates for Specification-Driven Development: constitution (tech stack and constraints), spec (requirements and user stories), design (architecture and decisions), test-plan (verification per acceptance criterion), implementation-plan (task breakdown and order), task (single executable unit), roadmap (feature timeline and metrics), and memory (patterns and lessons).

**One-paragraph:** Eight copy-paste templates for Specification-Driven Development: constitution (tech stack and constraints), spec (requirements and user stories), design (architecture and decisions), test-plan (verification per acceptance criterion), implementation-plan (task breakdown and order), task (single executable unit), roadmap (feature timeline and metrics), and memory (patterns and lessons). All templates use YAML frontmatter for machine-readable metadata and support LLM-assisted workflows.

## Applies If (ALL must hold)

- Starting a new project: generate constitution and roadmap before any code.
- Adding a feature: scaffold spec, design, test-plan, implementation-plan in one agent pass.
- When a human provides a rough feature description and wants a fully structured SDD folder immediately.
- When bootstrapping a project that will be executed by faion-sdd-executor-agent.
- Onboarding a new team to Specification-Driven Development; templates teach the format by example.

## Skip If (ANY kills it)

- Single-file bug fixes or one-liner patches: no SDD overhead needed.
- Vibe-coding or rapid throwaway prototypes where specs will be discarded.
- When a feature already has complete SDD docs: check .aidocs/ first before re-generating.
- When constitution.md does not yet exist: create it first; templates depend on it for constraints.
- Projects where no one will read or maintain documentation: templates create false promise if abandoned.

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
