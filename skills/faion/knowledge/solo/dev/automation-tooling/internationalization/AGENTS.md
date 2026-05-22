---
slug: internationalization
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Extract user-facing strings to ICU MessageFormat keys, format dates/numbers/currency through locale-aware APIs (Intl/Babel), use logical CSS properties for RTL support, and validate key drift in CI.
content_id: "66f987770d3b9b55"
tags: [i18n, localization, rtl, icu-messageformat, multi-locale]
---
# Internationalization (i18n)

## Summary

**One-sentence:** Extract user-facing strings to ICU MessageFormat keys, format dates/numbers/currency through locale-aware APIs (Intl/Babel), use logical CSS properties for RTL support, and validate key drift in CI.

**One-paragraph:** Extract user-facing strings to ICU MessageFormat keys, format dates/numbers/currency through locale-aware APIs (Intl/Babel), use logical CSS properties for RTL support, and validate key drift in CI. Sync with a Translation Management System (TMS) like Lokalise or Crowdin for team translation workflows.

## Applies If (ALL must hold)

- Externalizing hardcoded strings in an existing single-locale codebase (Python/FastAPI, Django, React/Next, Vue, mobile).
- Adding a second/third locale (especially RTL) and needing to scan layouts for physical CSS properties, fixed widths, hardcoded date/number formats.
- Generating ICU MessageFormat plural/select rules for a target locale (Slavic/Arabic plurals are agent-trap territory).
- Extracting messages, syncing with a TMS (Lokalise/Crowdin/Phrase/Tolgee), and merging back into the repo.
- Bootstrapping pybabel, i18next, react-intl, or next-intl configuration end-to-end.

## Skip If (ANY kills it)

- True one-locale-forever apps (internal admin tools, regulated single-market products) — the i18n tax outweighs the value.
- For copywriting/localization quality. Agents extract and wire keys; native human translators decide tone, register, dialect.
- For legal/medical/financial copy in regulated markets — those need certified translators, not LLM output.
- For RTL bidirectional text rendering bugs in libraries — agents can flag them but fixing requires Unicode BIDI expertise.
- When the project uses a proprietary framework with no public message-extraction tooling.

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

- parent skill: `solo/dev/automation-tooling/`
