---
slug: interview-note-synthesis-ai
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Clustering insights across 20+ interviews, distinguishing signal from anecdote, producing opportunity-tree-feeding outputs — the synthesis step PMs stop short of.
content_id: "a4542b6013ff630e"
tags: [interview-note-synthesis-ai, research, geek]
---

# Interview Note Synthesis (AI-Assisted)

## Summary

**One-sentence:** Clustering insights across 20+ interviews, distinguishing signal from anecdote, producing opportunity-tree-feeding outputs — the synthesis step PMs stop short of.

**One-paragraph:** Researcher skill has ai-interview-analysis at geek tier but nothing covers synthesis specifically: clustering insights across 20+ interviews, signal vs anecdote, OST-feeding outputs. Most PMs stop at transcripts. Output: synthesis artefact + cluster map + OST candidates.

## Applies If (ALL must hold)

- ≥20 interview transcripts ready for synthesis
- researcher OR PM with AI tool access (Claude/GPT-4)
- downstream consumer is an OST or roadmap

## Skip If (ANY kills it)

- <10 interviews — sample too small for clustering
- interviews on sensitive topics with no AI consent
- team has no roadmap consumer — synthesis without target is theatre

## Prerequisites

- transcripts in machine-readable format
- extraction taxonomy (JTBD, pain, success quote)
- AI tool with sufficient context window OR chunking strategy

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent skill — provides operating context for this methodology |
| `pro/research/researcher` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/ai-interview-analysis` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/research/researcher/`
- peer methodology: `pro/research/researcher`
- peer methodology: `geek/ai/ai-interview-analysis`
- peer methodology: `pro/product/discovery-cadence-design`
- external: https://www.producttalk.org/2021/08/continuous-discovery-habits/; https://www.dovetail.com/blog/qualitative-research-synthesis
