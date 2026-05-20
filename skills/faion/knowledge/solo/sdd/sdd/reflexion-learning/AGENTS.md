---
slug: reflexion-learning
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reflexion (NeurIPS 2023) is a verbal reinforcement learning paradigm where LLM agents improve through accumulated episodic memory rather than weight updates.
content_id: "1fdb37776dcbcf80"
tags: [reflexion, reinforcement-learning, memory-architecture, sdd, pdca]
---
# Reflexion Learning

## Summary

**One-sentence:** Reflexion (NeurIPS 2023) is a verbal reinforcement learning paradigm where LLM agents improve through accumulated episodic memory rather than weight updates.

**One-paragraph:** Reflexion (NeurIPS 2023) is a verbal reinforcement learning paradigm where LLM agents improve through accumulated episodic memory rather than weight updates. Applied to SDD, it maps to the PDCA cycle: Plan (load patterns.md + mistakes.md), Do (execute with context), Check (evaluate against AC, generate verbal reflection), Act (write new PAT-NNN or MIS-NNN entries). External feedback signals — tests, linter, type checker — are mandatory; self-evaluation alone has a 64.5% blind-spot rate.

## Applies If (ALL must hold)

- Any multi-task SDD workflow where agent quality must improve across tasks within a project
- When an agent has failed the same task type more than once
- Setting up a new project's `.aidocs/memory/` structure — Reflexion defines the memory architecture
- Unattended overnight agent batches where no human is available to correct mid-task failures

## Skip If (ANY kills it)

- Single-shot one-off tasks with no follow-up — no memory to accumulate
- Tasks where external ground truth is unavailable (no tests, no linter, no type checker) — self-evaluation degrades quality
- Projects under 1 week old with fewer than 10 completed tasks — corpus too thin
- When PDCA overhead exceeds the value of the learning loop (very small tasks under ~5k tokens)

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
