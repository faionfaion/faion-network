---
slug: agent-builder-community-rituals
tier: geek
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Codifies the weekly/biweekly/monthly rituals (office hours, eval-sharing, prompt-swap) that turn isolated LLM-agent developers into a learning community.
content_id: "5f8d0d67ea5426e0"
tags: [agent-builder-community-rituals, product, geek]
---

# Agent-Builder Community Rituals

## Summary

**One-sentence:** Codifies the weekly/biweekly/monthly rituals (office hours, eval-sharing, prompt-swap) that turn isolated LLM-agent developers into a learning community.

**One-paragraph:** LLM agent developers (P7) cite 'no shared corpus / community of fellow agent builders' as a top pain. Mechanism: a calendar of named rituals each with cadence, format, exit-criteria; an artefact per ritual; a small public log so newcomers can observe. Output: ritual calendar + three artefact templates + 90-day retention metric.

## Applies If (ALL must hold)

- ≥5 builders willing to commit 2-4h/month
- shared infra (Discord/Slack + doc store + calendar)
- ≥1 organizer with authority to enforce cadence

## Skip If (ANY kills it)

- <5 builders — group too small; do 1:1 mentorship
- no shared infra and no budget for it — rituals collapse
- purely social meetup with no artefact intent — use meetup playbook

## Prerequisites

- list of founding members with calendars synced
- Discord/Slack + docs root (Notion/Outline/GitHub)
- explicit code of conduct

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent skill — provides operating context for this methodology |
| `geek/ai/llm-evaluation` | peer methodology — produces inputs or consumes outputs |
| `geek/sdlc-ai/team-async-rituals` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodology: `geek/ai/llm-evaluation`
- peer methodology: `geek/sdlc-ai/team-async-rituals`
- external: https://github.com/anthropics/anthropic-cookbook (community cookbook pattern)
