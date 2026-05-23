---
slug: content-atomization-engine
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an atomization spec — extract → transform per channel → quality check → distribute — so one canonical asset ships into 10 channels without voice collapse.
content_id: "18d8ebb5044f1652"
complexity: medium
produces: spec
est_tokens: 4600
tags: ["atomization", "content", "fan-out", "indie-hacker", "marketing"]
---
# Content Atomization Engine

## Summary

**One-sentence:** Generates an atomization spec — extract → transform per channel → quality check → distribute — so one canonical asset ships into 10 channels without voice collapse.

**One-paragraph:** Generates an atomization spec — extract → transform per channel → quality check → distribute — so one canonical asset ships into 10 channels without voice collapse.

**Ефективно для:**

- Solo founder turning a long-form post / podcast / talk into 10 channel-native units.
- Build-in-public engine fan-out from a weekly source.
- Pre-launch atomization of a flagship piece across the funnel.

## Applies If (ALL must hold)

- Canonical asset exists (long-form post / podcast / talk / build log).
- Channels include ≥3 of: X, LinkedIn, IH, newsletter, blog, YouTube.
- Brand voice is documented.
- Quality check pass exists before distribution.

## Skip If (ANY kills it)

- Single-channel publishing — atomization is wasted overhead.
- Asset is one-off announcement — overhead exceeds value.
- No brand voice — atomization amplifies undefined tone.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Canonical asset | path | long-form source |
| Channel inventory | list | active channels + audience |
| Brand voice doc | path | brand-voice-consistency-system output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| brand-voice-consistency-system | Voice doc gates every atomized piece. |
| ai-content-quality-review | Quality rubric before distribution. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-single-canonical-source, r2-per-channel-transformation, r3-quality-gate-before-distribution, r4-named-owner, r5-distribution-log | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Content Atomization Engine artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: verbatim-repost, multi-source-leak, quality-bypass | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-content-atomization-engine` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-content-atomization-engine` | sonnet | Bounded structural check against the output contract. |
| `review-content-atomization-engine` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-atomization-engine.json` | JSON skeleton matching the output contract. |
| `templates/content-atomization-engine.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-content-atomization-engine.py` | Validate Content Atomization Engine output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[brand-voice-consistency-system]]
- [[ai-content-quality-review]]
- [[build-in-public-content-engine]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
