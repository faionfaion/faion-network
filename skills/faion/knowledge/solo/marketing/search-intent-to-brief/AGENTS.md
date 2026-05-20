---
slug: search-intent-to-brief
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Convert a target query into a structured content brief — intent class, must-cover entities, JTBD framing, SERP-feature inventory — before any drafting starts."
content_id: "43986eee5b2dc80c"
tags: [search-intent-to-brief, marketing, solo]
---
# Search Intent to Brief

## Summary

**One-sentence:** A structured handoff between keyword research and content drafting that produces a brief tagged with intent class, must-cover entities, JTBD frame, and SERP-feature inventory.

**One-paragraph:** Faion has `growth-seo-fundamentals` and `topical-authority` but no methodology for the highest-leverage handoff: turning a target query into a brief an AI or human can draft against. Without an explicit intent tag, drafts drift toward generic prose and miss SERP-feature opportunities (featured snippets, PAA, video carousels, etc.). This methodology fixes that with a 5-rule production pipeline: classify intent (I/C/T/N), enumerate must-cover entities from top-10 SERP, frame the JTBD ("when I have query X, I want to Y, so I can Z"), inventory current SERP features, and write the brief as a contract draft authors cannot ignore.

## Applies If (ALL must hold)

- you have a single target query (head term or long-tail) ready for content
- you can access live SERP for that query (manual or API)
- output will be handed to a drafter (human or AI) — not used internally
- tier == solo or higher

## Skip If (ANY kills it)

- query is below 10 monthly searches AND not a topical-authority hub piece
- intent is purely transactional and the page is already a product page (no editorial brief needed)
- you are writing for an internal audience with no organic-search goal

## Prerequisites

- target query string
- top-10 SERP snapshot (URL, title, snippet, page type)
- access to the topical cluster map this brief slots into

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/seo-manager` | parent — provides cluster-level context |
| `solo/marketing/on-page-seo-checklist-2026` | downstream consumer of the brief |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + 1 worked example brief | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_intent` | haiku | 4-class classification from query + SERP titles |
| `extract_entities` | sonnet | NER over top-10 snippets, dedupe, rank |
| `frame_jtbd` | sonnet | one-shot prompt with bounded inputs |

## Related

- parent skill: `solo/marketing/`
- `solo/marketing/seo-manager`
- upstream playbook: `role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence`
