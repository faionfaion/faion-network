---
slug: ops-customer-success-basics
tier: pro
group: marketing
domain: gtm-strategist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A proactive framework for ensuring customers achieve their goals with your product before they churn.
content_id: "8337f3c3ab716dc4"
tags: [customer-success, retention, churn, expansion, health-scoring]
---
# Customer Success Basics for Solopreneurs

## Summary

**One-sentence:** A proactive framework for ensuring customers achieve their goals with your product before they churn.

**One-paragraph:** A proactive framework for ensuring customers achieve their goals with your product before they churn. Five stages: Define (one north-star success metric per product), Measure (per-account health score from usage + sentiment + billing), Engage (event-triggered lifecycle touchpoints, not calendar dates), Enable (knowledge base + self-serve resources built before lifecycle emails), Expand (upgrade signals → expansion prompts). Core rule: trigger touchpoints on behavior events, cap automated re-engagements at one per week per account, and never let an agent issue refunds, downgrades, or credits autonomously.

## Applies If (ALL must hold)

- Defining success metrics for the first time on a SaaS, course, membership, or service product
- Building lifecycle email sequences (Day 1/3/7/14/30) with product-event triggers
- Computing customer health scores and routing at-risk accounts
- Designing self-serve enablement: knowledge base, onboarding guides, video library
- Building expansion playbooks: detect upgrade signals, trigger relevant offers

## Skip If (ANY kills it)

- Reactive support tickets — use ops-customer-support
- Detailed health-score modeling and CS KPIs — use ops-customer-success-metrics
- Churn-prevention forensics on already-churning customers — different, deeper diagnostic
- Enterprise named-account QBRs — framework covers structure; agents should not drive strategic conversations
- Pre-sales / SDR motion — use gtm-strategy or growth-cold-outreach

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

- parent skill: `pro/marketing/gtm-strategist/`
