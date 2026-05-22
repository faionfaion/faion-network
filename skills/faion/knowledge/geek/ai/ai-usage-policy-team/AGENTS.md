---
slug: ai-usage-policy-team
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: 1-page team-facing policy: what data engineers can paste into Claude/Cursor/Copilot, what cannot, and how to handle the gray zone.
content_id: "0c943f084e31d36b"
tags: [ai-usage-policy-team, ai, geek]
---

# Team AI Usage Policy

## Summary

**One-sentence:** 1-page team-facing policy: what data engineers can paste into Claude/Cursor/Copilot, what cannot, and how to handle the gray zone.

**One-paragraph:** Every product team needs this; 99% don't have it. faion has ai-governance-compliance at ML-engineer level — wrong audience. Mechanism: 1-page policy with three lists (always-OK, never-OK, ask-first) + incident-response. Output: versioned policy artefact with named owner + quarterly review.

## Applies If (ALL must hold)

- team size 3-50 with shared codebase
- devs use any AI tool (Cursor, Copilot, Claude.ai, ChatGPT, agentic CLIs)
- company handles customer data, source code, sales/legal docs, or PII

## Skip If (ANY kills it)

- solo dev with no customer data — use ai-over-reliance-self-audit
- company already has detailed AUP + DLP enforcement — augment, don't duplicate
- team in pre-commercial R&D with no production data

## Prerequisites

- list of AI tools in use (vendor + retention policy)
- list of data classifications (public/internal/confidential/regulated)
- named policy owner (CTO / Head of Eng / Security lead)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/ai-governance-compliance` | peer methodology — produces inputs or consumes outputs |
| `pro/sec/data-classification` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `geek/ai/ai-governance-compliance`
- peer methodology: `pro/sec/data-classification`
- external: https://www.nist.gov/itl/ai-risk-management-framework (NIST AI RMF); https://www.iso.org/standard/81230.html (ISO/IEC 42001)
