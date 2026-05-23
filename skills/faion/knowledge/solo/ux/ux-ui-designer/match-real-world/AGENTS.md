---
slug: match-real-world
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Audit UI copy and icons against users' mental model (Nielsen Heuristic #2) and produce a substitutions report — jargon and system-centric strings replaced with the user's vocabulary, consistently across the product.
content_id: "f297804d45736088"
complexity: medium
produces: report
est_tokens: 3700
tags: [heuristics, ux-copy, language, mental-models, localization]
---
# Match Between System and Real World

## Summary

**One-sentence:** Audit UI copy and icons against users' mental model (Nielsen Heuristic #2) and produce a substitutions report — jargon and system-centric strings replaced with the user's vocabulary, consistently across the product.

**One-paragraph:** Use words, icons, and organisational patterns that match users' mental models — not internal system or developer terminology. Inputs: UI string corpus (from i18n files / code grep) + user-vocabulary corpus (support tickets, interview transcripts, search logs). Output: a Language Audit report — each finding tagged (jargon | inconsistency | locale-blind | over-simplified-domain-term | icon-only) with a suggested rewrite grounded in user vocabulary citations.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Auditing UI copy for jargon, abbreviations, or technical terms before a release.
- A user-vocabulary corpus (support tickets, interviews, or search logs) is reachable.
- The product surface (web, app, email) has stable string identifiers reachable for citation.

## Skip If (ANY kills it)

- No user-vocabulary corpus exists — substitution would be team guesswork.
- The product is for domain experts whose precise vocabulary must be preserved (rewriting "invoice" → "bill" in accounting).
- Pre-release marketing copy where brand voice overrides heuristic compliance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| UI string corpus with identifiers | i18n JSON / CSV | engineering |
| User-vocabulary corpus | tickets export / transcripts / search-log CSV | support / research |
| Locale list + format rules | doc | i18n owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/user-interviews` | Source of user vocabulary citations. |
| `solo/ux/ux-ui-designer/usability-testing` | Validates that substitutions actually improve comprehension. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the language-audit report + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: extract → categorise → cite → substitute → consistency-pass | ~600 |
| `content/05-examples.xml` | medium | Worked rewrite example (SMTP → email; record created → booking confirmed) | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-strings` | haiku | Mechanical pull of UI strings from code / i18n. |
| `match-vocabulary` | sonnet | Map UI string to evidence in user corpus. |
| `consistency-pass` | sonnet | Diff terms across pages/emails for inconsistency. |

## Templates

| File | Purpose |
|------|---------|
| `templates/language-audit.md` | Language audit report skeleton. |
| `templates/extract-strings.py` | Stub to extract UI strings from a code tree. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-match-real-world.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[user-interviews]]
- [[usability-testing]]
- [[recognition-over-recall]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, user-vocabulary reachable, domain-expert override) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
