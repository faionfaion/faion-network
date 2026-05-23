<!-- purpose: Minimum viable filled-in wiring report for one project. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Sentry Supabase Vercel Wiring — Report

## Project

minimum viable example

## Configs shipped

- sentry.client.config.ts
- sentry.server.config.ts
- sentry.edge.config.ts

## Vercel env vars

- SENTRY_AUTH_TOKEN
- SENTRY_ORG
- SENTRY_PROJECT

## Findings

- F1 — verified source-map upload — https://sentry.io/issues/123

## Recommendations

- R1 — schedule quarterly noise review — @owner

**Owner:** @ruslan (platform lead)  •  **Reviewed:** 2026-05-23
