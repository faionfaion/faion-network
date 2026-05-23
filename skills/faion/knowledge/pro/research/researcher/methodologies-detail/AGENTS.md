---
slug: methodologies-detail
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a deep-dive page per research methodology (when-to-use, core-rules, output-contract, anti-patterns, validators) for use inside the faion.net knowledge surface.
content_id: "6f1bea52a3a9cb39"
complexity: medium
produces: spec
est_tokens: 4400
tags: [docs, methodology, deep-dive, authoring]
---
# Methodologies Detail

## Summary

**One-sentence:** Produces a deep-dive page per research methodology (when-to-use, core-rules, output-contract, anti-patterns, validators) for use inside the faion.net knowledge surface.

**One-paragraph:** Authoring methodology: given a methodology slug, this produces the deep-dive surface (the full Markdown rendition of AGENTS.md + content/*.xml as it appears on faion.net Pro tier documentation). Enforces consistent section ordering, mandatory testable rules count, and valid+invalid example pairing. Used by the docs pipeline, not by runtime agents.

**Ефективно для:**

- Поява нової методології - треба написати deep-dive сторінку для docs.
- Аудит існуючої сторінки методології (відсутні sections, TBD, незакриті example pairs).
- Reformatting batch після зміни schema (наприклад, F-066 wave).
- Authoring playbook посилається на методологію - сторінка має існувати.
- Локалізація детальної сторінки на іншу мову.

## Applies If (ALL must hold)

- Authoring a new deep-dive page for a research methodology.
- Auditing an existing detail page for completeness (sections, TBDs, example pairs).
- Reformatting batch after a schema change (F-066 wave, etc.).
- Cross-referencing playbook content to a methodology; the page must exist before publish.
- Localising a detail page to a new language.

## Skip If (ANY kills it)

- Authoring the short summary card (use methodologies-index instead).
- Editing source content of the methodology (edit AGENTS.md + content/*.xml directly).
- Drafting a one-off blog post about the methodology (use marketing content, not docs).
- Internal-only methodology with no public surface.
- Pre-spec methodology that does not yet have stable rules.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source methodology AGENTS.md | markdown | knowledge/<tier>/<group>/<slug>/ |
| Source content/*.xml | XML | knowledge/<tier>/<group>/<slug>/content/ |
| Tier + group + slug | frontmatter | methodologies-index |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[methodologies-index]] | supplies the catalog row that this detail page hangs off |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `section-extract` | haiku | Mechanical XML -> Markdown section copy. |
| `rules-render` | sonnet | Render testable rules table with id + statement + rationale + source. |
| `audit-pass` | sonnet | Audit completeness (sections, TBD, example pair, validator presence). |

## Templates

| File | Purpose |
|------|---------|
| `templates/methodology-detail.md` | Deep-dive page template (sections in canonical order) |
| `templates/audit-checklist.md` | Audit checklist (12 binary checks) used by the audit pass |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodologies-detail.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[methodologies-index]]
- [[frameworks]]
- [[workflows]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
