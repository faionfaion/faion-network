---
slug: mistake-memory
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Mistake Memory is the SDD practice of documenting failures in `.
content_id: "e05f7288f7f29d6e"
tags: [learning, mistakes, quality-gates, prevention, memory]
---
# Mistake Memory

## Summary

**One-sentence:** Mistake Memory is the SDD practice of documenting failures in `.

**One-paragraph:** Mistake Memory is the SDD practice of documenting failures in `.aidocs/memory/mistakes.md` immediately after they occur and injecting relevant warnings into agent context before similar tasks. Each entry requires: severity, what happened, root cause (Five Whys chain, min 3 levels), and one concrete prevention step. Generic preventions ("be more careful") are not acceptable.

## Applies If (ALL must hold)

- Before starting any task: load `.aidocs/memory/mistakes.md` and filter entries matching the task's domain keywords
- After a task fails (CI failure, production bug, review rejection): append a new MIS-NNN entry within 24 hours
- When the same failure pattern occurs a second time: escalate to an automated prevention rule in CI
- When onboarding a new agent: include mistakes.md in the project context handoff

## Skip If (ANY kills it)

- For tracking product bugs in a bug tracker — mistakes.md captures LLM/agent execution patterns, not feature defects
- When the project has fewer than 3 completed tasks — corpus too thin for useful patterns
- As a replacement for post-mortems on infrastructure incidents (mistakes.md is development-workflow scoped)

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
