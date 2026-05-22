---
slug: agent-context-engineering-corpus-standard
tier: pro
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Defines the canonical 2026 vocabulary, file shape, and citation rules for any agent-context-engineering artefact so faion becomes the standard reference.
content_id: "c49abc2fe6bccbfe"
tags: [agent-context-engineering-corpus-standard, ai, pro]
---

# Agent Context-Engineering Corpus Standard

## Summary

**One-sentence:** Defines the canonical 2026 vocabulary, file shape, and citation rules for any agent-context-engineering artefact so faion becomes the standard reference.

**One-paragraph:** P7 pain: 'no shared context-engineering corpus'. faion already has fragments (progressive-disclosure-skills, prompt-cache-prefix-order, compaction-preserve-refs, filesystem-as-working-memory, subagent-as-context-firewall, auto-evict-tool-results, inverted-header-content-first). Missing: a corpus standard. Output: glossary + artefact template + citation requirement.

## Applies If (ALL must hold)

- author writing a new context-engineering methodology or pattern
- audience is LLM-agent developers (P7) and AI engineers
- artefact will be cited from other faion methodologies

## Skip If (ANY kills it)

- writing non-context aspects (eval, RAG, tool use specifically)
- informal post/blog — corpus standard is for canonical entries only

## Prerequisites

- read existing faion fragments before authoring
- draft slug + abstract
- evidence: ≥2 production references OR ≥1 published primary source

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `progressive-disclosure-skills` | peer methodology — produces inputs or consumes outputs |
| `prompt-cache-prefix-order` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer methodology: `progressive-disclosure-skills`
- peer methodology: `prompt-cache-prefix-order`
- peer methodology: `compaction-preserve-refs`
- external: https://www.anthropic.com/research/building-effective-agents (Anthropic, Building Effective Agents)
