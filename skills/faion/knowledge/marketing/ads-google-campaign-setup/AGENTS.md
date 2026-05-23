# Google Ads Campaign Setup

## Summary

**One-sentence:** Provisions a Google Search campaign via API with conversion-tracking-first, PAUSED status, ad groups by theme, RSAs, extensions, and pre-launch verification — never ENABLED without checklist pass.

**One-paragraph:** API-provisioned Google Search campaigns silently inherit risky defaults (Display + Search Partners enabled, broad keywords, single-headline ads). This methodology specs the safe order: conversion tracking first → campaign PAUSED → ad groups by theme → RSAs (Responsive Search Ads) with required 15 headlines + 4 descriptions → extensions → pre-launch checklist → ENABLED. Output: campaign config + ad-group structure + RSA spec + extension list + verification checklist.

**Ефективно для:**

- Agency що template-їть new client account з repeatable skeleton.
- Onboarding multi-tenant accounts: same campaign structure per client.
- Pre-launch QA: блокує ENABLED поки checklist не пройдено.
- Migration manual → Smart Bidding через fresh templated campaign.

## Applies If (ALL must hold)

- Templating new Google Ads accounts (agency or in-house).
- Onboarding multi-tenant clients with repeated campaign skeleton.
- Pre-launch QA where launch must be blocked until checklist passes.
- Migrating manual campaigns to Smart Bidding via templated rebuild.

## Skip If (ANY kills it)

- Single-keyword test campaign — full structure overhead exceeds value.
- Display / YouTube / Discovery campaign — different methodology.
- Conversion tracking unavailable — methodology cannot complete required first step.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-google-campaign-setup` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton with 5-line header |
| `templates/output.json` | JSON sidecar with __faion_header__ |
| `templates/_smoke-test.yaml` | Minimum viable filled config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-google-campaign-setup.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
