---
slug: supabase-mvp-stack
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Supabase-specific patterns: Auth + RLS + Storage + Realtime + Edge Functions wired as a coherent MVP stack.
content_id: "8be443df5004f21e"
tags: [supabase-mvp-stack, dev, solo]
---

# Supabase MVP Stack

## Summary

**One-sentence:** Supabase-specific patterns: Auth + RLS + Storage + Realtime + Edge Functions wired as a coherent MVP stack.

**One-paragraph:** Supabase is the modal database for indie SaaS MVPs in 2026. faion has no Supabase-specific methodology despite covering Postgres heavily. Output: stack layout + RLS policy template + auth flow + migration discipline.

## Applies If (ALL must hold)

- indie hacker building MVP
- needs auth + DB + storage in one stack
- team size 1-2

## Skip If (ANY kills it)

- team ≥5 with dedicated DB ops (different stack)
- regulated workload requiring HSM / on-prem (Supabase Pro+ may not be sufficient)
- high-throughput analytics workload (use dedicated DWH)

## Prerequisites

- Supabase project created
- schema sketch (≥3 tables)
- decision on auth providers (email, OAuth)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent skill — provides operating context for this methodology |
| `solo/dev/api-developer` | peer methodology — produces inputs or consumes outputs |
| `solo/dev/lean-stack-bootstrapper-blueprint` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/dev/software-developer/`
- peer methodology: `solo/dev/api-developer`
- peer methodology: `solo/dev/lean-stack-bootstrapper-blueprint`
- peer methodology: `free/dev/backend-developer`
- external: https://supabase.com/docs; https://supabase.com/docs/guides/auth/row-level-security
