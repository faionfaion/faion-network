---
slug: vision-accessibility
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: VLMs generate WCAG-compliant alt text and extended scene descriptions for images at scale.
content_id: "a14803a24c27ae9d"
tags: [vision, accessibility, alt-text, wcag, vlm]
---
# Vision Accessibility: Alt Text and Scene Description

## Summary

**One-sentence:** VLMs generate WCAG-compliant alt text and extended scene descriptions for images at scale.

**One-paragraph:** VLMs generate WCAG-compliant alt text and extended scene descriptions for images at scale. The alt text must be concise (≤125 characters, no "image of" prefix), context-aware, and verbatim for embedded text. Extended descriptions cover spatial relationships, colors, mood, and key data points for charts. Keep alt-text generation in a separate subagent from data extraction to keep prompts focused.

## Applies If (ALL must hold)

- Accessibility tooling: auto-generating alt text and image descriptions at scale for CMS or e-commerce platforms.
- Publishing pipelines where images arrive without alt text and must be WCAG-compliant before publication.
- Retroactively making large image libraries accessible without manual review of every image.
- Screen reader support for dynamically generated charts, graphs, and data visualisations.

## Skip If (ANY kills it)

- Decorative images (spacers, backgrounds, borders) — set alt="" explicitly; do not generate descriptions that add noise for screen readers.
- Images requiring medical/legal accuracy in descriptions — VLM descriptions may hallucinate or mischaracterise details; human review required.
- Real-time descriptions during live video — VLM API latency (500 ms–2 s) makes synchronous video description impractical.

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

- parent skill: `geek/ai/ml-engineer/`
