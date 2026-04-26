# Internationalization (i18n)

## Summary

Internationalization prepares software to support multiple locales without code changes: externalize all user-facing strings to ICU MessageFormat keys, route dates/numbers/currency through `Intl` (JS) or Babel (Python), use logical CSS properties for RTL safety, and validate on every PR that EN keys exist in every shipped locale with matching ICU placeholders.

## Why

Hardcoded strings, manual date formatting, and physical CSS (`margin-left`) silently break when adding a second locale. ICU MessageFormat handles plurals, gender, and select clauses that gettext-style `_n()` cannot express cleanly. Catching key drift in CI (diff of key paths) costs one bash script; fixing production translation gaps costs days.

## When To Use

- Externalizing hardcoded strings in a single-locale codebase (Python/FastAPI, Django, React/Next, Vue).
- Adding a second locale — especially RTL — requiring layout audit for physical CSS properties.
- Generating ICU plural/select rules for Slavic, Arabic, or Welsh locales (multi-category plural rules).
- Bootstrapping `pybabel`, `i18next`, `react-intl`, or `next-intl` configuration end-to-end.
- Syncing with a TMS (Lokalise, Crowdin, Phrase, Tolgee) via CLI.

## When NOT To Use

- Single-locale-forever apps (internal admin tools, regulated single-market products) — i18n overhead is not justified.
- Localization quality — agents extract and wire keys; native translators decide tone and dialect.
- Legal/medical/financial copy in regulated markets — requires certified translators.
- RTL bidirectional rendering bugs in third-party libraries — flag them but fixing requires Unicode BIDI expertise.

## Content

| File | What's inside |
|------|---------------|
| `content/01-string-externalization.xml` | Key naming conventions (dotted), ICU MessageFormat plurals/select, Python Babel setup, FastAPI locale middleware. |
| `content/02-formatting-rtl.xml` | Locale-aware date/number/currency formatting, logical CSS properties, RTL detection in React. |
| `content/03-workflow.xml` | Extract → TMS push → translate → pull → build validation cycle; CI key-drift check script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/check-i18n.sh` | CI script that diffs EN key paths against every shipped locale and fails on drift. |
| `templates/extract-push.sh` | i18next-parser extract + Lokalise push/pull cycle for TS/React projects. |
