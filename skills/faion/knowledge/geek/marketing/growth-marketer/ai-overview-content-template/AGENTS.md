---
slug: ai-overview-content-template
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Concrete section template — definition block, comparison table, numbered list with bolded keys, citation row — that retrofits posts for Google AI Overview, Perplexity, and ChatGPT-Search citation eligibility."
content_id: "f69e2b1acad29fbf"
complexity: medium
produces: spec
est_tokens: 2900
tags: [aio, ai-overviews, content-template, seo, marketing, geek]
---

# AI Overview Content Template

## Summary

**One-sentence:** Concrete section template — definition block, comparison table, numbered list with bolded keys, citation row — that retrofits posts for Google AI Overview, Perplexity, and ChatGPT-Search citation eligibility.

**One-paragraph:** `google-ai-overviews-optimization` covers strategy; this methodology ships the actual content sections. Four mandatory section types (definition block at top of page, comparison table, numbered list with bolded keys for step-by-step, citation row at section end), plus the cross-cutting TL;DR-with-answer-in-first-40-words pattern. Apply on every new piece + retrofit across the topic cluster. Output: a post that produces measurably higher AIO citation rate than essay-style posts in the same niche, tracked via the sibling monitoring methodology.

**Ефективно для:** content marketers retrofitting topic clusters for AI search; SEO managers preparing pillar pages; agencies pitching AIO services.

## Applies If (ALL must hold)

- Target query has measurable AIO presence (panel appears on Google SERP)
- Content is informational or commercial-informational (not pure transactional)
- A topic cluster strategy is in place — this template is one section type
- Writer/marketing team can revise published posts (no editorial freeze)

## Skip If (ANY kills it)

- Zero-click query where AIO eats all attention — deprioritise via ai-overview-risk-scoring
- Brand / persona content for non-AIO discovery (founder LinkedIn) — different format
- Niche has no AIO presence yet — defer retrofit
- Writer cannot include citations or comparison data (NDA) — different content type

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Priority query list with AIO citation status | YAML | ai-overview-monitoring tracker |
| Research notes with ≥3 named-entity citations per piece | Markdown | content ops |
| Topic cluster index (pillar + supporting) | YAML | content strategy |
| Snippet-readiness pre-check | Markdown rubric | ai-content-quality-review |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[google-ai-overviews-optimization]] | strategy-level methodology |
| [[ai-overview-monitoring]] | monitor for retrofit impact |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `definition-block-draft` | haiku | Mechanical format-fill from research notes |
| `comparison-table-extract` | sonnet | Bounded judgement: which dimensions to compare |
| `numbered-list-rewrite` | sonnet | Bounded prose → numbered steps |
| `citation-row-compose` | sonnet | Per-claim citation match |

## Templates

| File | Purpose |
|------|---------|
| `templates/section-schema.json` | JSON schema for retrofit-eligible sections |
| `templates/aio-snippets.md` | Real examples of each section type with attribution |
| `templates/retrofit-log.md` | Per-piece retrofit log: sections added, citation added, date |
| `templates/_smoke-test.md` | Minimum-viable filled section |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-overview-content-template.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[google-ai-overviews-optimization]]
- [[ai-overview-monitoring]]
- [[ai-overview-risk-scoring]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-overview-content-template applies: root question — "Does the target query show an AIO panel AND is the post in scope for revision?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-definition-block, r2-comparison-table, r3-numbered-list-format, r4-citation-row, r5-40-word-answer, r6-retrofit-log.
