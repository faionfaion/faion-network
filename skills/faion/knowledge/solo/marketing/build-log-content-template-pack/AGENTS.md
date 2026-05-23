---
slug: build-log-content-template-pack
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a full template pack — weekly build log, monthly MRR report, milestone, pivot, sunset — across X / IH / newsletter / blog so build-in-public posts ship from a single source.
content_id: "6808a0415373fcef"
complexity: light
produces: spec
est_tokens: 4200
tags: ["build-log", "template-pack", "indie-hacker", "marketing", "fan-out"]
---
# Build Log Content Template Pack

## Summary

**One-sentence:** Generates a full template pack — weekly build log, monthly MRR report, milestone, pivot, sunset — across X / IH / newsletter / blog so build-in-public posts ship from a single source.

**One-paragraph:** Generates a full template pack — weekly build log, monthly MRR report, milestone, pivot, sunset — across X / IH / newsletter / blog so build-in-public posts ship from a single source.

**Ефективно для:**

- Indie hacker repeating the same 5 post types weekly/monthly.
- Multi-channel fan-out where each channel needs format adaptation.
- Pre-launch consolidation of post templates before the engine starts.

## Applies If (ALL must hold)

- Founder publishes ≥1 build log / MRR report / milestone per month.
- Channels include ≥2 of: X, IH, newsletter, blog.
- Templates will be reused for ≥6 months.
- Brand voice is documented (or will be before first publish).

## Skip If (ANY kills it)

- One-off announcement — overhead exceeds value.
- Founder writes everything fresh each time — preference, not gap.
- Pre-product with no shipping — no build log to template.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Channel inventory | list | X / IH / newsletter / blog handles |
| Brand voice doc | path | brand-voice-consistency-system output |
| Sample posts | list | ≥5 prior posts per format |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| build-in-public-content-engine | Provides the engine these templates plug into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-five-canonical-templates, r2-per-channel-adaptation, r3-fill-slots-not-rewrite, r4-named-owner, r5-version-bumped-on-change | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Build Log Content Template Pack artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: freeform-rewrite, channel-monoculture, untracked-edits | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-build-log-content-template-pack` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-build-log-content-template-pack` | sonnet | Bounded structural check against the output contract. |
| `review-build-log-content-template-pack` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-log-content-template-pack.json` | JSON skeleton matching the output contract. |
| `templates/build-log-content-template-pack.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-build-log-content-template-pack.py` | Validate Build Log Content Template Pack output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[build-in-public-content-engine]]
- [[brand-voice-consistency-system]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
