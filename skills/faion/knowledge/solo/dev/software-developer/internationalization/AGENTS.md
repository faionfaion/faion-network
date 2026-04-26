# Internationalization

## Summary

Methodology for preparing software to support multiple languages and locales without code
changes. Covers string externalization via ICU MessageFormat, Babel (Python) and react-intl
(TS), database-driven translations, locale-aware formatting (date/number/currency), RTL layout,
and the translation management workflow. Core rule: one message = one complete sentence with
ICU placeholders; never concatenate translated fragments.

## Why

String concatenation breaks grammar in most locales; naive `if n == 1` plural logic fails for
Slavic, Arabic, and Welsh; hardcoded `MM/DD/YYYY` and `$` symbols are wrong outside the US.
ICU MessageFormat, Babel, and the `Intl.*` APIs handle these edge cases correctly. Retrofitting
i18n after launch costs 5-10x more than building it in.

## When To Use

- Product shipping into a second locale or with regulatory obligation (EU, Quebec Bill 96)
- Externalising hardcoded strings before translation work begins
- Adding RTL support (Arabic, Hebrew, Persian) — must be designed in, not retrofitted
- Standardising date/number/currency formatting across services
- Creating white-label products requiring locale switching

## When NOT To Use

- Single-locale internal tool with no expansion plan — extraction/build overhead not justified
- Marketing landing pages better handled by a translation CMS (Phrase, Lokalise, Crowdin)
- Domain-specific jargon that does not translate — keep English, localise only UI chrome
- "We'll use Google Translate at runtime" — fluency too low for product UI

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-principles.xml` | ICU MessageFormat rules, key naming, plurals, never-concat rule |
| `content/02-python-i18n.xml` | Babel setup, gettext, FastAPI locale middleware, DB translations |
| `content/03-frontend-i18n.xml` | react-intl, FormattedMessage, RTL with CSS logical properties |

## Templates

| File | Purpose |
|------|---------|
| `templates/babel-cfg.ini` | Babel extraction config for Python + Jinja2 |
| `templates/pseudo-loc.py` | Pseudo-localisation generator to surface truncation in CI |
