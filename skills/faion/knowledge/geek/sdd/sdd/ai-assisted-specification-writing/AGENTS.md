---
slug: ai-assisted-specification-writing
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Collaborative human-AI specification creation using LLMs to draft, refine, and validate requirements.
content_id: "8daa6240b93f156a"
tags: [specification, sdd, requirements, ai-assisted, human-in-loop]
---
# AI-Assisted Specification Writing

## Summary

**One-sentence:** Collaborative human-AI specification creation using LLMs to draft, refine, and validate requirements.

**One-paragraph:** Collaborative human-AI specification creation using LLMs to draft, refine, and validate requirements. The workflow: human provides intent, AI structures questions and drafts FR list with edge cases and Given-When-Then acceptance criteria, human reviews and approves, then implementation begins. Human approval gates are mandatory at every stage.

## Applies If (ALL must hold)

- Starting a new feature, service, or system where requirements are known informally but not structured
- Producing spec.md and design.md documents in the SDD lifecycle before implementation begins
- When a human has described intent but edge cases, dependencies, and acceptance criteria are not yet explicit
- Reviewing an existing specification for completeness, internal conflicts, and missing acceptance criteria
- Converting informal requirements (meeting notes, chat logs, PRDs) into structured SDD-format specifications

## Skip If (ANY kills it)

- When domain knowledge is highly specialized (medical, legal, financial regulatory) and the agent lacks sufficient context — garbage-in-garbage-out on domain-specific requirements
- When specifications are already complete and formally approved — agent review adds no value and risks introducing changes to finalized docs
- For pure infrastructure or configuration tasks where the spec is trivially derived from the implementation
- When no human reviewer is available — AI-generated specs must always have a human approval gate before implementation begins

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

- parent skill: `geek/sdd/sdd/`
