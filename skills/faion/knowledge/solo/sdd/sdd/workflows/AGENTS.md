---
slug: workflows
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: SDD workflows guide the progression from idea to deployed code through structured phases.
content_id: "5855a9b1517a6537"
tags: [sdd, workflows, phases, llm, agents]
---
# SDD Workflows

## Summary

**One-sentence:** SDD workflows guide the progression from idea to deployed code through structured phases.

**One-paragraph:** SDD workflows guide the progression from idea to deployed code through structured phases. Each workflow includes decision points, state transitions, quality gates, and LLM prompts covering spec, design, implementation, and review phases.

## Applies If (ALL must hold)

- Starting a new multi-day feature that needs structured progression from idea to deployed code.
- An agent needs to orchestrate multiple sub-agents across spec → design → implementation → review phases.
- The codebase already has `.aidocs/` structure and the team follows SDD lifecycle.
- Resuming mid-session work: agent reads `session.md` to restore state and continue from last checkpoint.
- Producing auditable artifacts: regulated domains, client deliverables, or systems requiring traceability.

## Skip If (ANY kills it)

- Task estimated at under 2 hours — direct implementation is faster than full SDD overhead.
- Pure bug fix with a known root cause — fix + test is sufficient without spec and design phases.
- Exploratory spike or prototype — throwaway code does not benefit from full SDD overhead.
- Configuration-only change — editing a config file needs no spec or design phase.

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
