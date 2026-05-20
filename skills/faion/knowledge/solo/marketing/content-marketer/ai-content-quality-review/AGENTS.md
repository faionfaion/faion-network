---
slug: ai-content-quality-review
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "232e403c9165b5a6"
summary: A discrete rubric that catches shallow AI-drafted content (entity-thin, citation-free, no original POV, generic intro padding, hallucinated stats) before publish.
tags: [content-quality, ai-content, e-e-a-t, solo, marketing]
---
# AI Content Quality Review

## Summary

**One-sentence:** A discrete, checklist-driven review pass that catches the five dominant failure modes of AI-drafted long-form content (entity-thin, citation-free, no original POV, generic intro padding, hallucinated stats) before publication.

**One-paragraph:** Solopreneurs and growth marketers ship AI-drafted content daily, but the dominant LLM output pattern is "plausible-but-doesn't-rank": generic intro padding, no named entities, no citations, no original viewpoint, and statistics that look authoritative but cannot be traced. This methodology operationalizes a 7-section review pass — entity density, citation depth, original-POV check, intro tax, stat verification, ICP fit, and snippet-readiness — that the founder or a sonnet-class subagent runs on every AI draft before it leaves staging. Output: a rubric-scored draft with red-flag lines highlighted and a hard publish/revise/scrap decision. This is the single highest-leverage content review in 2026 because Google's AI Overviews, Perplexity, and ChatGPT-Search all penalize the exact failure modes the rubric catches.

## Applies If (ALL must hold)

- The content was substantially AI-generated (any draft &gt;= 30% LLM tokens).
- The content is destined for indexable channels (blog, Substack, LinkedIn article, knowledge base).
- The piece is &gt;= 600 words (shorter pieces use a stripped-down 3-point check instead).
- A primary ICP and target keyword (or job-to-be-done query) are declared before review.

## Skip If (ANY kills it)

- Content is a transactional micro-copy (CTA, button text, error message) — overhead exceeds the win.
- The piece is a verbatim founder transcript with light AI cleanup — pass through the transcript review instead.
- Internal-only knowledge base entry never indexed publicly — only the stat-verification check applies.
- Content has already been reviewed by a domain expert with sign-off note — single review is enough.

## Prerequisites

- Draft is in a final-form Markdown file (not a fragment in a chat thread).
- ICP and target query / keyword declared in the draft's frontmatter or in a paired brief.
- A research notes file with named-entity candidates, citation URLs, and at least one original observation from the founder.
- A "do not publish without image" flag check (sibling rule from `feedback_no_publish_without_image`).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/growth-content-marketing` | Background on content marketing fundamentals; this rubric is a downstream gate. |
| `solo/marketing/seo-manager/seo-essentials` | Snippet-readiness check uses the same SERP heuristics. |
| `geek/marketing/seo-manager/google-ai-overviews-optimization` | AIO citation patterns inform the citation-depth rule. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: entity density floor, citation depth floor, original-POV requirement, intro tax cap, stat verification | ~1100 |
| `content/02-output-contract.xml` | essential | Rubric-score schema, red-flag annotation format, publish/revise/scrap decision rule | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes specific to LLM-drafted content with detectors and repairs | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `entity-density-scan` | haiku | Tokenizer + named-entity recognition; mechanical |
| `citation-extract-and-verify` | sonnet | Bounded URL fetch + claim-match; per-citation judgment |
| `original-pov-detection` | sonnet | Pattern-match against draft history + research notes; bounded |
| `rubric-aggregate-and-decide` | opus | Cross-section synthesis; needs whole-draft view to weigh tradeoffs |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | JSON schema for the 7-section rubric score |
| `templates/red-flag-annotations.md` | Inline annotation syntax: `[[entity-thin]]`, `[[stat-unverified]]`, etc. |
| `templates/review-prompt.txt` | Sonnet-class review prompt template parameterized by ICP + keyword |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/entity-density.py` | Compute named-entity / 100-word floor; flag entity-thin paragraphs | First pass on any draft |
| `scripts/citation-verifier.py` | Fetch every URL in citations; check claim-match via sonnet | After entity pass |
| `scripts/rubric-aggregate.py` | Combine per-section scores; emit publish / revise / scrap | Final pass |

## Related

- parent skill: `solo/marketing/content-marketer/`
- peer methodologies: `growth-content-marketing`, `growth-copywriting-fundamentals`
- external: [Google E-E-A-T Quality Rater Guidelines](https://services.google.com/fh/files/misc/hsw-sqrg.pdf) · [Originality.ai content audit](https://originality.ai/) · [Sparktoro AI content study 2025](https://sparktoro.com/)
