---
slug: brainstorming-ideation
tier: solo
group: comms
domain: communicator
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Brainstorming-ideation covers using brainstorming techniques as a generative input for automated pipelines — where the output is a scored shortlist, not a facilitated group session.
content_id: "35555799f51e924d"
tags: [ideation, brainstorming, agentic-pipeline, diverge-converge, feature-generation]
---
# Brainstorming Ideation (Agentic Pipeline)

## Summary

**One-sentence:** Brainstorming-ideation covers using brainstorming techniques as a generative input for automated pipelines — where the output is a scored shortlist, not a facilitated group session.

**One-paragraph:** Brainstorming-ideation covers using brainstorming techniques as a generative input for automated pipelines — where the output is a scored shortlist, not a facilitated group session. The agent receives a problem statement, runs a structured generation pass (Classic, Reverse, or Brainwriting-simulated), deduplicates semantically, clusters by theme, and scores against an impact/effort rubric. For facilitated group sessions, see brainstorming-techniques which covers the human-facilitation angle.

## Applies If (ALL must hold)

- Product feature generation: given a persona + pain point, produce candidate features to evaluate against backlog
- Content ideation: bulk-generating article topics, campaign angles, or ad copy variants for human selection
- Risk surfacing: Reverse Brainstorming to enumerate failure modes before a launch or deployment
- Feeding a scored shortlist into a downstream pipeline (Linear backlog, Notion idea database)

## Skip If (ANY kills it)

- When human group dynamic is the point (team alignment, buy-in, psychological safety) — agentic bulk generation skips the relational work
- When the problem is too narrow for divergent thinking; use direct prompting or SCAMPER instead
- When ideas require domain-expert validation that an LLM cannot reliably provide (medical, legal, engineering safety)
- When you need the dot-voting or scoring to be done by the same agent that generated the ideas — circular bias invalidates the prioritization

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

- parent skill: `solo/comms/communicator/`
