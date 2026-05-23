# Sentry Supabase Vercel Wiring

## Summary

**One-sentence:** Concrete integration recipe wiring Sentry into a Next.js-on-Vercel + Supabase solo stack: source-map upload via bundler plugin, edge-runtime sampling cap, Supabase auth-payload scrubbing, RLS error classification.

**One-paragraph:** Solo builders hit edge-runtime errors, missing source maps, and PII leakage from auth-error payloads, and burn a weekend fixing the wiring after the first 500 lands. This methodology gives a single recipe: install order, env-var map, Vercel build hook for source-map upload, edge-runtime sampling caveats, Supabase RLS-error scrubbing, and pre-tuned `ignoreErrors` to mute Next.js dev noise. Output is a working `sentry.{client,server,edge}.config.ts` plus a `vercel.json` snippet.

## Applies If (ALL must hold)

- App is Next.js (App Router or Pages) deployed on Vercel.
- Auth or database goes through Supabase.
- Operator wants first-incident error visibility without enterprise observability.

## Skip If (ANY kills it)

- Self-host Next.js outside Vercel — use the standard Sentry Next.js guide.
- Different error tracker (Highlight, Honeybadger, Bugsnag) — pattern differs.
- Sentry already wired; question is tuning, not bootstrap — use the tuning runbook.

**Ефективно для:**

- Indie SaaS на Next.js + Supabase + Vercel — найшвидший шлях до робочого Sentry.
- Соло-розробники що вперше натрапили на 500 в prod без stack trace.
- Команди де middleware-auth ловить edge-runtime errors поза client/server конфігом.
- Стартапи з GDPR / privacy-compliance — потрібен scrubbing JWT з error payloads.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Sentry account + project DSN | DSN URL | sentry.io |
| Supabase project URL + anon key | URL + key | Supabase dashboard |
| Vercel project linked to a git repo | Vercel project ID | Vercel dashboard |
| Next.js 13+ codebase | App Router or Pages | operator repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/one-person-rollback-runbook` | Downstream — Sentry alert triggers rollback runbook. |
| `solo/infra/supabase-rls-audit-checklist` | Sibling — Supabase-side guardrails. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable wiring rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: missing edge config, no source maps, JWT leak, edge oversampling | 900 |
| `content/04-procedure.xml` | essential | Wiring procedure from npm install to first verified event | 900 |
| `content/05-examples.xml` | essential | Worked example: full sentry.*.config.ts triplet + vercel.json env | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-sentry-configs` | haiku | Template fill from project IDs. |
| `scrub-supabase-errors` | sonnet | Per-Supabase-error-class redaction logic. |
| `tune-ignore-list` | sonnet | Match Sentry events to noise patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown report listing wired configs + env-var checklist. |
| `templates/_smoke-test.md` | Minimum viable filled-in wiring report for one project. |
| `templates/sentry.server.config.ts` | Server-runtime Sentry config with scrubbing + ignore list. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sentry-supabase-vercel-wiring.py` | Validate wiring artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | After wiring; in CI on any sentry.*.config.ts change. |

## Related

- [[one-person-rollback-runbook]]
- [[supabase-rls-audit-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
