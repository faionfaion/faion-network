---
slug: search-everywhere-optimization
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a multi-platform search visibility plan artefact (SEO + AEO + GEO across Google + ChatGPT + Perplexity + YouTube + TikTok) gated by AI-extractable content structure."
content_id: "d2b9ff50f0a6597b"
complexity: deep
produces: spec
est_tokens: 4900
tags: ["seo", "aeo", "geo", "ai-search", "multi-platform", "solo"]
---
# Search Everywhere Optimization

## Summary

**One-sentence:** Produces a multi-platform search visibility plan artefact (SEO + AEO + GEO across Google + ChatGPT + Perplexity + YouTube + TikTok) gated by AI-extractable content structure.

**One-paragraph:** Solo operators optimise for Google only and miss the surface area now spread across ChatGPT / Perplexity / YouTube / TikTok. This methodology pins multi-platform visibility: ≥3 target platforms with rationale, AI-extractable content structure (headings + lists + Q&A + schema), named citation targets per platform, author E-E-A-T anchors (bio + credentials + last-updated), and a monthly citation-monitoring task. Output: a search-everywhere plan spec.

**Ефективно для:**

- готова основа для повторюваної задачі «search-everywhere-optimization» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Operator publishes content on a domain they control.
- Operator has author identity to attach to content.
- Monthly cycle available for citation monitoring.

## Skip If (ANY kills it)

- Operator refuses to add structured author bios.
- Content lives on a 3rd-party platform without schema control.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target query shortlist per platform | spreadsheet | research |
| Author bio + credentials | doc | operator |
| Site schema config | JSON-LD snippet | developer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/eeat-signal-pass-template` | Per-post EEAT pass methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the search-everywhere-plan artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/search-everywhere-optimization.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/search-everywhere-optimization.json` | search-everywhere-plan JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-search-everywhere-optimization.py` | Validate the search-everywhere-plan artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[eeat-signal-pass-template]]
- [[growth-youtube-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
