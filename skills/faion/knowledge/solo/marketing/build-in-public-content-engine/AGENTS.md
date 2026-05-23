---
slug: build-in-public-content-engine
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a 6-week build-in-public engine spec — weekly inputs, 5 post formats, hook patterns, repurposing chain, metric loop — so a solo founder hits compound subscriber growth in <4h/week.
content_id: "5f8692d802ed4b0b"
complexity: medium
produces: spec
est_tokens: 5000
tags: ["build-in-public", "indie-hacker", "content-engine", "twitter-x", "audience-growth"]
---
# Build-in-Public Content Engine

## Summary

**One-sentence:** Generates a 6-week build-in-public engine spec — weekly inputs, 5 post formats, hook patterns, repurposing chain, metric loop — so a solo founder hits compound subscriber growth in <4h/week.

**One-paragraph:** Generates a 6-week build-in-public engine spec — weekly inputs, 5 post formats, hook patterns, repurposing chain, metric loop — so a solo founder hits compound subscriber growth in <4h/week.

**Ефективно для:**

- Solo founder shipping weekly who 'dislikes marketing'.
- Indie hacker building audience from zero on X / LinkedIn.
- Newsletter operator repurposing build work into the list.

## Applies If (ALL must hold)

- Founder is actively building a product (shipping or close to shipping weekly).
- Founder is willing to share work publicly (numbers, mistakes, screenshots).
- A primary channel is selected (default: X) and an account exists with a basic bio.
- Founder can commit at least 3 short posts + 1 longer post per week.

## Skip If (ANY kills it)

- Product is in stealth or under enterprise NDA — no public sharing possible.
- Founder has zero tolerance for public commentary — engine fails on internal resistance.
- Target ICP is not on social media — switch to outbound + community methodology.
- Founder has <1 hour/week available — engine requires minimum 3-4 hrs/week.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Weekly product-work log | md | commits + decisions + screenshots |
| Primary social account | url | X / LinkedIn handle |
| Email-capture page | url | Substack / ConvertKit / static |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| build-in-public-cadence | Daily-weekly rhythm this engine plugs into. |
| content-atomization-engine | Atomization rules for X → LinkedIn → blog → newsletter. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-weekly-input-ritual, r2-five-format-menu, r3-hook-discipline, r4-repurposing-chain, r5-metric-loop | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Build-in-Public Content Engine artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: vanity-only-metrics, generic-llm-posts, format-sprawl | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-build-in-public-content-engine` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-build-in-public-content-engine` | sonnet | Bounded structural check against the output contract. |
| `review-build-in-public-content-engine` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-in-public-content-engine.json` | JSON skeleton matching the output contract. |
| `templates/build-in-public-content-engine.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-build-in-public-content-engine.py` | Validate Build-in-Public Content Engine output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[build-in-public-cadence]]
- [[content-atomization-engine]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
