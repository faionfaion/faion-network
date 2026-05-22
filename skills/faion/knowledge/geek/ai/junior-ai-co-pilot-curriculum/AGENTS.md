---
slug: junior-ai-co-pilot-curriculum
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Structured curriculum: when NOT to ask the agent, how to verify generated code, code-review prompts for self-review, pair-with-AI-then-pair-with-human cadence.
content_id: "f6808bd639bc27bc"
tags: [junior-ai-co-pilot-curriculum, ai, geek]
---

# Junior AI Co-Pilot Curriculum

## Summary

**One-sentence:** Structured curriculum: when NOT to ask the agent, how to verify generated code, code-review prompts for self-review, pair-with-AI-then-pair-with-human cadence.

**One-paragraph:** Stated pain: junior over-reliance on AI. No methodology exists for a structured curriculum that lets a junior use AI productively without atrophying. Output: 12-week curriculum + assessment rubric + manager check-ins.

## Applies If (ALL must hold)

- team with ≥1 junior engineer (≤2 years experience)
- AI coding tools in active use (Cursor, Copilot, Claude Code)
- manager bandwidth for weekly check-ins

## Skip If (ANY kills it)

- team policy bans AI assistants — curriculum irrelevant
- junior is in formal bootcamp / external program — defer
- team treats AI as black-box productivity tool with no junior-development concern

## Prerequisites

- junior dev with named manager + buddy
- weekly 1:1 time blocked
- access to AI tools the team uses

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/ai-usage-policy-team` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/ai-over-reliance-self-audit` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `geek/ai/ai-agents/`
- peer methodology: `geek/ai/ai-usage-policy-team`
- peer methodology: `solo/dev/ai-over-reliance-self-audit`
- peer methodology: `pro/dev/junior-dev-onboarding`
- external: https://stackoverflow.blog/2024/03/05/ai-coding-assistants-survey/; https://about.gitlab.com/handbook/engineering/ux/ai-assisted-coding/
