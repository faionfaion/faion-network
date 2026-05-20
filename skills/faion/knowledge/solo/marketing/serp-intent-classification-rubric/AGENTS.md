---
slug: serp-intent-classification-rubric
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Rubric that forces explicit intent classification (I/C/T/N + sub-types) for every target query before drafting, with falsifiable SERP-anchored evidence."
content_id: "b36285379b80eca8"
tags: [serp-intent-classification-rubric, marketing, solo]
---
# SERP Intent Classification Rubric

## Summary

**One-sentence:** A rubric that tags every target query with one primary intent and (optional) one secondary intent, anchored to falsifiable SERP evidence.

**One-paragraph:** AI-generated drafts miss intent because the human author never made it explicit. This rubric forces the tagger to (a) pick exactly one primary intent from a closed set, (b) cite which SERP signals justify it (page types in top-10, SERP features present, "related searches" framing), (c) flag intent-mixed queries that should be split, (d) reject ambiguous queries that need user-research first. Output is a one-line intent label that downstream methodologies (`search-intent-to-brief`, `on-page-seo-checklist-2026`) consume. Without this rubric, AI drafting on solo workflows produces format-mismatched content that ranks but doesn't convert.

## Applies If (ALL must hold)

- you have a target query (head or long-tail)
- you can pull a live top-10 SERP for the query
- you intend to draft content against the query
- tier == solo or higher

## Skip If (ANY kills it)

- the query is purely navigational for a known brand and you ARE that brand
- the query has < 10 monthly searches AND no cluster value (deprioritize entirely)
- the brand explicitly does not target organic search for this term

## Prerequisites

- the target query string
- a live top-10 SERP snapshot (manual screenshot or API)
- access to GSC "related searches" or keyword tool's question expansion (optional but recommended)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/search-intent-to-brief` | downstream — consumes the intent label |
| `solo/marketing/on-page-seo-checklist-2026` | downstream — format choices follow from intent |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable classification rules + intent sub-type taxonomy + 1 worked classification | ~950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_serp_signals` | haiku | structured pull from top-10 |
| `apply_rubric` | sonnet | classification with cited evidence |
| `flag_intent_mix_or_ambiguity` | sonnet | meta-judgement |

## Related

- parent skill: `solo/marketing/`
- `solo/marketing/search-intent-to-brief`
- `solo/marketing/seo-manager`
- upstream playbook: `role-growth-marketing/Keyword research session for a new topic (deep, 2-3 hrs)`
