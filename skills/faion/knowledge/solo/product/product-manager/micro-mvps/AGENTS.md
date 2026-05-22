---
slug: micro-mvps
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Micro-MVPs are extremely small, high-signal experiments (hours to days) that validate one specific assumption before committing engineering time.
content_id: "fafd75a87ee3804d"
tags: [product-validation, experiments, assumption-testing, mvp, learning]
---
# Micro-MVPs

## Summary

**One-sentence:** Micro-MVPs are extremely small, high-signal experiments (hours to days) that validate one specific assumption before committing engineering time.

**One-paragraph:** Micro-MVPs are extremely small, high-signal experiments (hours to days) that validate one specific assumption before committing engineering time. The rule: pre-register the success criterion as a number before launching; if a "micro" MVP takes longer than one week to build, it is not micro.

## Applies If (ALL must hold)

- Validating one specific assumption (demand, willingness-to-pay, workflow fit) before committing engineering time
- Pre-PMF stage where every shipped feature is a learning bet, not a delivery
- Validating a new segment for an existing product (fake-door, smoke-test)
- Solo or 2-person team with limited capacity — micro-MVPs preserve runway
- Founder is "in love with a feature" — a micro-MVP is the cheapest way to disprove the hypothesis

## Skip If (ANY kills it)

- Post-PMF feature work for an established product where users expect polish — fake-door damages trust
- Compliance, security, or infrastructure work — there is no demand to validate
- Teams with no monitoring/instrumentation — you cannot learn from the experiment without measurement
- Brand-sensitive launches where being seen running an experiment is reputational risk
- B2B enterprise sales cycles where a "video demo" is table stakes, not a validation experiment

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

- parent skill: `solo/product/product-manager/`
