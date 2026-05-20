---
slug: sentry-supabase-vercel-wiring
tier: solo
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Integration-level wiring for Sentry on the default solo stack (Next.js on Vercel + Supabase): SDK setup, source-map upload, edge-runtime caveats, noise suppression."
content_id: "1f92f092832713b3"
tags: [sentry-supabase-vercel-wiring, infra, solo]
---
# Sentry Supabase Vercel Wiring

## Summary

**One-sentence:** Concrete integration recipe that wires Sentry into a Next.js-on-Vercel + Supabase solo stack with source-maps, edge-runtime support, and pre-tuned noise filters.

**One-paragraph:** Faion has pieces of this in isolation — Sentry as a tool, Supabase auth, Vercel deploy — but no methodology that integrates the actual default solo stack into a working observability pickup line. Solo builders hit edge-runtime errors, missing source maps, and PII leakage from auth-error payloads, and burn a weekend fixing the wiring after the first 500 lands. This methodology gives a single recipe: install order, environment-variable map, Vercel build hook for source-map upload, edge-runtime sampling caveats, Supabase RLS-error scrubbing, and pre-tuned `ignoreErrors` to mute Next.js dev noise. Output is a working `sentry.{client,server,edge}.config.ts` plus a `vercel.json` snippet.

## Applies If (ALL must hold)

- you ship a Next.js (App Router or Pages) app on Vercel
- you use Supabase for auth and/or database
- you want first-incident error visibility without enterprise observability
- tier == solo or higher

## Skip If (ANY kills it)

- you self-host Next.js outside Vercel (use the standard Sentry Next.js guide)
- you use a different error tracker (Highlight, Honeybadger, Bugsnag) — pattern differs
- you've already wired Sentry and the question is tuning, not bootstrap (see incident-response methodology)

## Prerequisites

- Sentry account + project DSN
- Supabase project (URL + anon key)
- Vercel project linked to a git repo
- Next.js 13+ (App Router supported)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/one-person-rollback-runbook` | downstream — once Sentry tells you about a regression |
| `solo/infra/supabase-rls-audit-checklist` | sibling — Supabase-side guardrails |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable wiring rules + 1 worked config example | ~950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate_sentry_configs` | haiku | template fill from project IDs |
| `scrub_supabase_errors` | sonnet | per-Supabase-error-class redaction logic |
| `tune_ignore_list` | sonnet | match Sentry events to noise patterns |

## Related

- parent skill: `solo/infra/`
- `solo/infra/one-person-rollback-runbook`
- `solo/infra/supabase-rls-audit-checklist`
- upstream playbook: `p1-solo-saas-builder/Solo prod incident response (no team safety net)`
