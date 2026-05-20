---
slug: icp-message-mining-from-ai-conversations
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Mining support chats, sales transcripts, and AI-agent conversation logs for jobs-to-be-done phrases, objections, and success language — VOC for the 2026 stack.
content_id: "8f9a379155d24ab7"
tags: [icp-message-mining-from-ai-conversations, marketing, pro]
---

# ICP Message Mining from AI Conversations

## Summary

**One-sentence:** Mining support chats, sales transcripts, and AI-agent conversation logs for jobs-to-be-done phrases, objections, and success language — VOC for the 2026 stack.

**One-paragraph:** In 2026 the highest-quality voice-of-customer is in support chats, sales transcripts, AI-agent conversation logs. No methodology covers mining these for messaging extraction. Output: mining pipeline + extraction taxonomy + messaging deliverable.

## Applies If (ALL must hold)

- ≥100 transcripts/month across support + sales + AI-agent conversations
- marketing owner with authority to update copy
- consent / privacy basis for analyzing customer conversations

## Skip If (ANY kills it)

- B2B with <50 transcripts/quarter — sample too small
- no consent basis for analyzing conversations — must establish first
- conversations heavily redacted/PII-stripped to uselessness

## Prerequisites

- transcript store + access pattern
- extraction taxonomy: JTBD phrases, objections, success language
- consent + privacy basis confirmed

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/growth-marketer` | peer methodology — produces inputs or consumes outputs |
| `pro/research/researcher` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `pro/marketing/growth-marketer`
- peer methodology: `pro/research/researcher`
- peer methodology: `solo/research/user-interviews`
- external: https://www.amplitude.com/blog/voice-of-customer; https://intercom.com/blog/voice-of-customer-research/
