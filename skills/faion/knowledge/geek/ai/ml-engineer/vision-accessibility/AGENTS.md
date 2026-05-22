---
slug: vision-accessibility
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates WCAG-compliant alt text (≤125 chars, no 'image of' prefix, embedded text verbatim) and extended scene descriptions from images using VLMs.
content_id: "ded816f1b4beb2fe"
complexity: medium
produces: spec
est_tokens: 3600
tags: [vision, accessibility, alt-text, wcag, vlm]
---
# Vision Accessibility — Alt Text & Scene Description

## Summary

**One-sentence:** Generates WCAG-compliant alt text (≤125 chars, no 'image of' prefix, embedded text verbatim) and extended scene descriptions from images using VLMs.

**One-paragraph:** WCAG 2.1 requires alt text for every non-decorative image. Manual authoring does not scale past a few hundred images. This methodology runs an alt-text subagent with page context (heading, slug), strict ≤125-char output, no 'image of' prefix, and verbatim embedded-text capture. Charts get an additional pass that includes the key insight (trend, comparison, extreme) — not just the chart type.

**Ефективно для:**

- CMS / e-commerce bulk back-fill: 10k+ images need alt text in a sprint.
- Publishing pipelines: new images arrive without alt and must be WCAG-compliant before publish.
- Chart-heavy dashboards: alt text must convey the insight, not the chart type.
- Regulated accessibility audits: defensible per-image alt + extended description records.

## Applies If (ALL must hold)

- Generating alt text at scale (≥100 images) for a CMS, marketplace, or knowledge base.
- WCAG 2.1 AA compliance is a deliverable.
- Page context (heading, slug, surrounding text) is available to pass to the VLM.

## Skip If (ANY kills it)

- Image is decorative (spacer, border): set alt="" instead of generating noise.
- Image requires medical / legal accuracy in description (hallucination risk too high).
- Real-time live-video description (VLM latency 500ms-2s makes sync video impractical).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Image file | jpg/png/webp | CDN or origin storage |
| Page context | string | Surrounding heading + section purpose + URL slug |
| Decorative flag | bool | Authoring system or CMS rule |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `alt_text_gen` | sonnet | Vision model call; needs context fusion. |
| `decorative_classify` | haiku | Binary; rule-based on dimensions + alpha. |
| `chart_insight` | sonnet | Must summarise the data, not the visual. |

## Templates

| File | Purpose |
|------|---------|
| `templates/alt-text-prompt.txt` | VLM prompt template for alt text generation |
| `templates/chart-insight-prompt.txt` | VLM prompt template for chart key-insight extraction |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-accessibility.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[vision-provider-selection]]
- [[vision-agentic-pipeline]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is the image decorative (per CMS flag or dimensions+alpha rule)? Branches route to a rule id from `content/01-core-rules.xml` (decorative-empty, chart-insight, embedded-text-verbatim, ...) so every leaf is traceable to a testable statement.
