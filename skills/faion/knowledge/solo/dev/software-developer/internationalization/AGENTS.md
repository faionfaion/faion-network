---
slug: internationalization
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Prepare software for multiple languages and locales via ICU MessageFormat, externalised strings, locale-aware formatting, and RTL-ready CSS.
content_id: "096cf21fda14af00"
complexity: medium
produces: code
est_tokens: 4000
tags: [i18n, localization, icu-messageformat, rtl, internationalization]
---
# Internationalization

## Summary

**One-sentence:** Prepare software for multiple languages and locales via ICU MessageFormat, externalised strings, locale-aware formatting, and RTL-ready CSS.

**One-paragraph:** Externalise every user-facing string into locale catalogues (PO/JSON/XLIFF), use ICU MessageFormat for plurals and gender, format numbers / dates / currencies via Intl (browser) or CLDR (server), keep CSS logical (start/end vs left/right) for RTL, and run pseudo-localization in CI to catch hardcoded strings and overflow. Translators receive context comments and a translation memory; release pipeline includes a no-missing-keys check.

**Ефективно для:**

- Products targeting >=2 locales or multi-region rollout.
- Replacing ad-hoc string interpolation with ICU MessageFormat.
- Adding RTL support (Arabic, Hebrew) to existing LTR product.
- Establishing a translation handoff workflow.

## Applies If (ALL must hold)

- Product UI surfaces user-facing text (not backend-only).
- At least 2 locales planned or supported.
- Engineering owns the i18n pipeline (extraction, catalogues, build integration).
- Translators or translation vendors are in the workflow.

## Skip If (ANY kills it)

- Single-locale product with no internationalisation plans (premature).
- All text is dynamic user-generated content — i18n applies to UI chrome only here.
- Embedded firmware where locale catalogues exceed budget.
- Project delegates i18n to a SaaS (Crowdin/Lokalise) and accepts their model end-to-end.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Locale list + fallback rules | table | product |
| i18n library chosen (FormatJS, i18next, gettext, Polyglot) | config | platform |
| Translation pipeline (PO files vs SaaS) decided | ADR | tech-lead |
| Pseudo-localization tooling for CI | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[frontend-design]] | Design tokens + components support locale switching. |
| [[logging-patterns]] | Logs note locale + missing-key events. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (no hardcoded strings, ICU MessageFormat for plurals, Intl for numbers/dates, logical CSS for RTL, pseudo-loc in CI) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for i18n module spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: catalogue init → externalise strings → ICU patterns → RTL audit → pseudo-loc CI | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `string_externalisation` | sonnet | Mechanical: replace string literals with t() calls + keys. |
| `icu_message_authoring` | sonnet | Convert hand-built plural strings to ICU. |
| `rtl_audit` | sonnet | Walk CSS; replace physical (left/right) with logical (start/end). |
| `pseudo_loc_pipeline` | sonnet | CI step: render pages with pseudo-loc; assert no truncation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/babel-cfg.ini` | Babel/extraction config for gettext-style flows |
| `templates/pseudo-loc.py` | Pseudo-localization transformer for catalogue values |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-internationalization.py` | Validate i18n module spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[frontend-design]]
- [[logging-patterns]]
- [[accessibility]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps locale count, UI surface, and pipeline ownership to a rule from `01-core-rules.xml`, telling the agent whether to run the full i18n setup or skip when premature. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
