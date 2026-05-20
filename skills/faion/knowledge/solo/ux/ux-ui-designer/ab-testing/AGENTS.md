---
slug: ab-testing
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A/B testing is a controlled experiment that compares two versions of a UI element (control A vs.
content_id: "b7f4b22564934e1d"
tags: [ab-testing, experimentation, ux-testing, cro, statistics]
---
# A/B Testing

## Summary

**One-sentence:** A/B testing is a controlled experiment that compares two versions of a UI element (control A vs.

**One-paragraph:** A/B testing is a controlled experiment that compares two versions of a UI element (control A vs. variant B) on a live user population to determine which produces a better outcome on a defined metric. Design decisions based on opinions create unresolvable debates. A/B testing replaces opinion with behavioral evidence from real users at scale. The hypothesis, primary metric, and minimum sample size must be pre-registered before launch to prevent peeking and moving goalposts.

## Applies If (ALL must hold)

- A design change has a clear, measurable primary metric (conversion rate, click-through, completion).
- Traffic is sufficient for the required sample size (typically 1,000+ conversions/month).
- The change is isolated — one variable at a time to enable attribution.
- Iterative optimization of an existing flow, not early-stage discovery.

## Skip If (ANY kills it)

- Traffic under ~1,000 conversions/month — sample size makes results meaningless.
- Major redesigns with multiple simultaneous changes — too many confounds to attribute results.
- When you need to understand why users behave differently — use user interviews instead.
- Early-stage product where the primary metric itself is unclear.
- Regulatory or safety-critical features where split exposure carries risk.

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

- parent skill: `solo/ux/ux-ui-designer/`
