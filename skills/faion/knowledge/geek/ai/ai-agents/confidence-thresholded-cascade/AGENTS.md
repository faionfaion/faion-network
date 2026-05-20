---
slug: confidence-thresholded-cascade
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Send the request to a cheap model first.
content_id: "241bdb99ece23d76"
tags: [cost-optimization, multi-model, routing, confidence-calibration, frugal-gpt]
---
# Confidence-Thresholded Cascade

## Summary

**One-sentence:** Send the request to a cheap model first.

**One-paragraph:** Send the request to a cheap model first. The cheap model returns an answer AND a confidence score. If confidence is above threshold, accept it. Otherwise, escalate to the expensive model. This is FrugalGPT's core insight — most tasks are easy, and a cheap model can self-detect when it's out of its depth.

## Applies If (ALL must hold)

- High-volume traffic where cost dominates (chatbots, classifiers, batch processing)
- Mixed task difficulty (some easy, some hard) — cascade adapts
- Latency-tolerant production paths (cascade adds one round-trip)
- Tasks where confidence is calibrate-able (classification, factual extraction)

## Skip If (ANY kills it)

- Mission-critical decisions where ANY error has high cost (skip cascade; go straight to strong model)
- Tasks where "confidence" is hard to elicit (creative writing, planning)
- Cold-start: cheap model doesn't know its limits yet — needs eval data first
- Latency-critical interactive flows where the second hop blows the budget

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

- parent skill: `geek/ai/ai-agents/`
