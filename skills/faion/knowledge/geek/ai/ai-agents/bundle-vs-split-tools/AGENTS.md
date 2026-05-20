---
slug: bundle-vs-split-tools
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When tool count exceeds about 25, model tool-selection accuracy collapses and tokens spent on tool definitions dominate.
content_id: "d5a9bc774894d04b"
tags: [tool-use, bundling, tool-routing, agent-design, function-calling]
---
# Bundle vs Split Tools

## Summary

**One-sentence:** When tool count exceeds about 25, model tool-selection accuracy collapses and tokens spent on tool definitions dominate.

**One-paragraph:** When tool count exceeds about 25, model tool-selection accuracy collapses and tokens spent on tool definitions dominate. Bundle related atomic tools into a single composite tool with a mode arg ONLY when modes share most of their argument shape AND the model has training-data prior for that bundle pattern. Default is split — many small named tools. Bundle only to escape the >25 limit; never as a first design choice.

## Applies If (ALL must hold)

- Tool count exceeds 25 and you can group related ops cleanly.
- The same prompt audience uses all modes (e.g., "file ops" → list, read, write, delete).
- Training data has strong priors for the bundle (e.g., REST verbs, file ops, git commands).
- Tools share most of their args (e.g., they all take `path`).
- Reducing tool-def tokens is critical (e.g., streaming-based systems where prompt size affects latency).

## Skip If (ANY kills it)

- Tool count < 25 — default to split; each tool's description is a tight prompt for one job.
- Tools have meaningfully different purposes — keep them split for clarity.
- Tools serve completely different audiences (e.g., git vs npm vs docker) — model gets confused; better as separate tools.
- Modes have totally different args — shared args is part of the bundle premise.
- Mode arg would require the model to guess user intent — the mode should map to user-explicit intent.

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

- parent skill: `geek/ai/ai-agents/`
