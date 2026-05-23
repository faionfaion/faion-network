---
slug: build-in-public-cadence
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a daily capture-hook-ship-log rhythm + weekly fan-out spec — X / IH / newsletter from a single source — so an indie hacker sustains build-in-public for >8 weeks.
content_id: "b9560394d28c281e"
complexity: light
produces: spec
est_tokens: 4200
tags: ["build-in-public", "cadence", "indie-hacker", "twitter-x", "weekly-fan-out"]
---
# Build In Public Cadence

## Summary

**One-sentence:** Generates a daily capture-hook-ship-log rhythm + weekly fan-out spec — X / IH / newsletter from a single source — so an indie hacker sustains build-in-public for >8 weeks.

**One-paragraph:** Generates a daily capture-hook-ship-log rhythm + weekly fan-out spec — X / IH / newsletter from a single source — so an indie hacker sustains build-in-public for >8 weeks.

**Ефективно для:**

- Solo founder posting build-in-public daily.
- Indie hacker who has previously burned out on irregular posting.
- Multi-surface fan-out from a single weekly capture.

## Applies If (ALL must hold)

- Founder builds in public on X, IH, LinkedIn, or a newsletter.
- Founder has a shipped product or active build to talk about (no vapor).
- Founder has ≤30 min/day for marketing on top of building.
- Founder has burned out on irregular posting at least once.

## Skip If (ANY kills it)

- Founder refuses to write — cadence will not fix that.
- B2B enterprise where social is not the channel.
- Founder has a dedicated content marketer — use weekly-growth-review-rhythm.
- Pre-product — use distribution-first-ideation first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Primary channel | string | X / IH / LinkedIn / newsletter |
| Daily capture | min | ≤30 min/day commitment |
| Single source doc | path | weekly capture document |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| build-in-public-content-engine | Provides the post formats this cadence consumes. |
| content-atomization-engine | Atomization rules for fan-out. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-daily-capture-hook-ship-log, r2-single-source-fan-out, r3-30-min-cap, r4-named-owner, r5-weekly-fan-out-fixed-day | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Build In Public Cadence artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: irregular-posting, multi-source-writing, burnout-no-cap | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-build-in-public-cadence` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-build-in-public-cadence` | sonnet | Bounded structural check against the output contract. |
| `review-build-in-public-cadence` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-in-public-cadence.json` | JSON skeleton matching the output contract. |
| `templates/build-in-public-cadence.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-build-in-public-cadence.py` | Validate Build In Public Cadence output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[build-in-public-content-engine]]
- [[content-atomization-engine]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
