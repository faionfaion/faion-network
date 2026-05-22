---
slug: core-vui-design-principles
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three foundational principles for voice user interfaces — simplicity (short, single-idea responses), natural conversation (follow-up awareness, human turn-taking), and context awareness (remembering prior turns, adapting to preferences) — that apply to all voice runtimes from Alexa Skills to LLM-powered Realtime API agents.
content_id: "f4ee38008ea70c40"
tags: [voice-ui, vui, principles, conversational-design, latency]
---
# Core VUI Design Principles

## Summary

**One-sentence:** Three foundational principles for voice user interfaces — simplicity (short, single-idea responses), natural conversation (follow-up awareness, human turn-taking), and context awareness (remembering prior turns, adapting to preferences) — that apply to all voice runtimes from Alexa Skills to LLM-powered Realtime API agents.

**One-paragraph:** Three foundational principles for voice user interfaces — simplicity (short, single-idea responses), natural conversation (follow-up awareness, human turn-taking), and context awareness (remembering prior turns, adapting to preferences) — that apply to all voice runtimes from Alexa Skills to LLM-powered Realtime API agents.

## Applies If (ALL must hold)

- Designing a new voice agent or LLM-powered voice interface (Alexa, Google Action, OpenAI Realtime).
- Auditing transcripts of an existing voice product for verbosity or missing context handling.
- Writing the system prompt and dialog policy for a Realtime API or Vapi voice agent.
- Defining acceptance criteria for voice flows in a spec or design doc.

## Skip If (ANY kills it)

- Visual UI or chat — these principles produce over-terse copy when applied to text interfaces.
- IVR with regulatory scripts (banking disclosures, healthcare consent) — mandatory verbosity overrides.
- Rapid voice prototype before basic ASR is confirmed working — premature optimization.

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

- parent skill: `pro/ux/ux-ui-designer/`
