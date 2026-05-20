---
slug: internationalization
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for preparing software to support multiple languages and locales without code changes.
content_id: "66f987770d3b9b55"
tags: [i18n, localization, icu-messageformat, rtl, internationalization]
---
# Internationalization

## Summary

**One-sentence:** Methodology for preparing software to support multiple languages and locales without code changes.

**One-paragraph:** Methodology for preparing software to support multiple languages and locales without code changes. Covers string externalization via ICU MessageFormat, Babel (Python) and react-intl (TS), database-driven translations, locale-aware formatting (date/number/currency), RTL layout, and the translation management workflow. Core rule: one message = one complete sentence with ICU placeholders; never concatenate translated fragments.

## Applies If (ALL must hold)

- Product shipping into a second locale or with regulatory obligation (EU, Quebec Bill 96)
- Externalising hardcoded strings before translation work begins
- Adding RTL support (Arabic, Hebrew, Persian) — must be designed in, not retrofitted
- Standardising date/number/currency formatting across services
- Creating white-label products requiring locale switching
- Product is shipping into a second locale or already has user demand from non-English speakers
- Legal / contractual obligation (EU CRA, French Toubon law, Quebec Bill 96, accessibility regs)
- Standardising date/number/currency formatting across services (e.g., backend → email → mobile must agree)

## Skip If (ANY kills it)

- Single-locale internal tool with no expansion plan — extraction/build overhead not justified
- Marketing landing pages better handled by a translation CMS (Phrase, Lokalise, Crowdin)
- Domain-specific jargon that does not translate — keep English, localise only UI chrome
- Using Google Translate at runtime — fluency too low for product UI; only acceptable for user-generated content snippets

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

- parent skill: `solo/dev/software-developer/`
