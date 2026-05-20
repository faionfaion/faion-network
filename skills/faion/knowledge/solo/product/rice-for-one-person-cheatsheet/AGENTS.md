---
slug: rice-for-one-person-cheatsheet
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "3c12d266af805e7f"
summary: "RICE adjusted for the solo SaaS builder: Reach baselined to a small absolute user count, Effort in dev-days not dev-weeks, Confidence forced to three discrete levels, and a WIP-1 framing that forces a single bet per Sunday roadmap ritual instead of a ranked stack of parallel work."
tags: [product, solo, p1-solo-saas, rice, prioritization, wip-1, sunday-roadmap]
---
# RICE for One-Person Cheatsheet

## Summary

Classic RICE assumes a team-sized Reach baseline (10k+ monthly active users), an Effort estimate in dev-weeks across multiple people, and a 4-level Confidence vibe scale that produces noise when one operator does all four roles. The solo SaaS builder needs the discipline of RICE but with the math reweighted: Reach in absolute small-number user counts (because 80 active users is a real signal at solo scale), Effort in dev-days for one person (because dev-weeks blurs the solo bottleneck), Confidence collapsed to three discrete levels so the operator stops self-grading "70%", and a WIP-1 framing in the Sunday roadmap ritual — top of the ranked list is the only bet of the week. The cheatsheet picks one thing, not a stack.

## Applies If

- The operator is a solo or two-person SaaS builder running a Sunday roadmap or weekly shaping ritual.
- A backlog exists with at least 5 candidate items competing for the same operator's hours.
- Active-user count, paying-customer count, or another concrete usage metric is measurable.
- The operator has authority to commit to a single weekly bet and to defer the rest.

## Skip If

- The team has &gt; 3 people who can work in parallel — use the standard RICE then; WIP-1 framing wastes parallelism.
- No usage metric is yet available (pre-MVP) — Reach has no data, score by ICE or anti-roadmap instead.
- The bet is regulator-imposed or contractual (must ship anyway) — prioritisation is moot.

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Five testable rules adjusting Reach, Impact, Confidence, Effort for the solo case, plus the WIP-1 weekly bet rule |

## Related

- parent skill: `solo/product/`
- triggering activity: `Sunday roadmap & week-shaping ritual`
- neighbouring: `solo/product/anti-roadmap-template`, `solo/product/rice-for-design`, `solo/product/kano-prioritization`
