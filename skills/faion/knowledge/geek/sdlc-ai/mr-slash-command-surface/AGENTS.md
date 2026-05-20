---
slug: mr-slash-command-surface
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Expose review-bot capabilities as PR-comment slash commands so humans steer the bot in-band rather than through a separate dashboard.
content_id: "995fe325a7282940"
tags: [pr-review, slash-commands, qodo-merge, coderabbit, review-bot]
---
# Slash-Command Surface for PR Review Bots

## Summary

**One-sentence:** Expose review-bot capabilities as PR-comment slash commands so humans steer the bot in-band rather than through a separate dashboard.

**One-paragraph:** Expose review-bot capabilities as PR-comment slash commands so humans steer the bot in-band rather than through a separate dashboard. Qodo Merge / PR-Agent set the standard: `/describe` regenerates title and walkthrough, `/review` posts inline issues, `/improve` posts code-suggestion patches you can apply with one click, `/ask "why does this regex differ?"` queries the diff. Auto-trigger `/describe` plus `/review` on PR open and re-push; leave `/improve` opt-in (it's the noisy one). CodeRabbit (`@coderabbitai resolve|review`) and Sourcery follow the same surface.

## Applies If (ALL must hold)

- Multi-author repos where humans want a "second pair of eyes" before requesting human review.
- High-PR-volume repos (>20/day) where humans drown in description-writing.
- Repos already using a slash-command-capable bot (Qodo Merge, CodeRabbit, Sourcery).
- Open-source repos where contributors lack institutional context to describe risk in PR bodies.

## Skip If (ANY kills it)

- Tiny PRs (<20 LOC) — `/review` adds more noise than it removes.
- Repos with strict "no third-party app on source" policy without a self-hosted PR-Agent install.
- Single-author repos where the author already writes the description — auto-describe overwrites it.
- Compliance setups where bot comments must be pre-approved before posting.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
