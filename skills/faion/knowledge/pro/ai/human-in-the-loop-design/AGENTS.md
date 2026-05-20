---
slug: human-in-the-loop-design
tier: pro
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Where to insert review steps, how to design confidence-based escalation to humans, how to capture corrections back into the eval set.
content_id: "0e643af70b2300ce"
tags: [human-in-the-loop-design, ai, pro]
---

# Human-in-the-Loop Design

## Summary

**One-sentence:** Where to insert review steps, how to design confidence-based escalation to humans, how to capture corrections back into the eval set.

**One-paragraph:** Tangentially touched by confidence-thresholded-cascade but not as a product-design methodology. Output: HITL placement map + escalation policy + correction-loop wiring.

## Applies If (ALL must hold)

- AI workflow with stakes (legal, money, customer-facing copy, code)
- human reviewers available with bandwidth
- engineering capacity to add review checkpoints

## Skip If (ANY kills it)

- low-stakes high-volume tasks (categorization with high tolerance)
- human review impossible at scale (no team)
- fully autonomous research / agent loops outside production

## Prerequisites

- list of decision points in the workflow
- list of available human reviewers + bandwidth
- ability to add review queue + correction capture

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/confidence-thresholded-cascade` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/llm-judge-rubric-evidence-first` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `geek/ai/confidence-thresholded-cascade`
- peer methodology: `geek/ai/llm-judge-rubric-evidence-first`
- external: https://arxiv.org/abs/2204.02839 (Constitutional AI); https://www.anthropic.com/research/agentic-misalignment
