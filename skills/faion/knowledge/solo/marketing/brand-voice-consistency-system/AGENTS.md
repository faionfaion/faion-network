---
slug: brand-voice-consistency-system
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a brand voice doc + per-channel checklist + voice-check rubric — voice attributes, do/don't pairs, drift audit — gated by a named voice owner.
content_id: "0d065caa1c16842f"
complexity: medium
produces: spec
est_tokens: 4600
tags: ["brand-voice", "marketing", "content", "consistency", "ai-content"]
---
# Brand Voice Consistency System

## Summary

**One-sentence:** Generates a brand voice doc + per-channel checklist + voice-check rubric — voice attributes, do/don't pairs, drift audit — gated by a named voice owner.

**One-paragraph:** AI generation collapses brand voice across 10 channels. This methodology pins a one-page voice doc (5 attributes, 10 do/don't pairs, audience tone vector), a per-channel adaptation table (Twitter / LinkedIn / blog / email / docs), and a drift audit rubric. Output: a VoiceDoc + ChannelChecklist + DriftAudit triple.

**Ефективно для:**

- Solo founder running role-growth-marketing/Ship one piece into 10 channels with AI atomization.
- Multi-author content where voice drifted unnoticed.
- Pre-launch brand consolidation across web + email + social.
- Drift audit after a quarter of AI-heavy output.

## Applies If (ALL must hold)

- Operator publishes across ≥3 channels regularly.
- AI tools generate ≥30% of the prose.
- Brand voice matters (not internal docs).
- No documented voice doc OR existing doc > 6 months old.

## Skip If (ANY kills it)

- Single-channel operator with no AI assistance.
- Internal-only documentation with no audience.
- Brand-agency-managed voice already in place.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Sample prose from last 90 days | ≥20 posts | operator archive |
| Audience description | ≤300 words | ICP doc |
| Competitor voice references | ≥3 examples | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| ai-slop-detector-checklist | Voice scoring uses the slop rubric voice dimension. |
| audience-to-customer-funnel | Channel adaptation depends on stage in funnel. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-five-attributes-named, r2-do-dont-pairs, r3-per-channel-adaptation, r4-named-owner, r5-quarterly-drift-audit | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Brand Voice Consistency System artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: voice-by-vibes, ai-default-flattens, no-channel-adaptation, drift-unnoticed | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-voice-doc` | opus | High-stakes synthesis — sets a year of content tone. |
| `draft-channel-checklist` | sonnet | Per-channel adaptation rules. |
| `drift-audit` | sonnet | Diff recent prose against voice doc. |

## Templates

| File | Purpose |
|------|---------|
| `templates/brand-voice-consistency-system.json` | VoiceDoc + ChannelChecklist JSON skeleton. |
| `templates/brand-voice-consistency-system.md` | One-page voice doc + adaptation table. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-brand-voice-consistency-system.py` | Validate VoiceDoc JSON against the schema. | On creation + quarterly review. |

## Related

- [[ai-slop-detector-checklist]]
- [[audience-to-customer-funnel]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
