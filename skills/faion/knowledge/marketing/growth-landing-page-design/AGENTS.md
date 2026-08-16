# AIDA-Structured Landing Page

## Summary

**One-sentence:** Produces a landing-page copy artefact (headline + AIDA flow + single CTA per section + social proof below CTA) gated by headline structure and one-CTA rule.

**One-paragraph:** Solo operators ship hero copy as clever phrases with multi-CTA sections and social proof above the fold; CVR sits at floor. This methodology pins AIDA-structured copy: [Outcome] + [Timeframe] + [Without Pain] headline, Attention / Interest / Desire / Action section order, exactly one CTA per section, social proof below the primary CTA, and a mobile-first 375px fold. Output: a landing-page copy artefact.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-landing-page-design» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Landing page exists or is being designed.
- Conversion goal is defined and tracked.
- Operator has authority over copy + design decisions.

## Skip If (ANY kills it)

- Page is for a free content piece with no conversion goal — AIDA overhead beats payoff.
- Regulated industry requiring clinical-claim review of every line.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing page wireframe | Figma / image | design |
| Conversion goal definition | tracked event | analytics |
| Customer outcome data for headline | doc | research / CS |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/marketing/conversion-optimizer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/growth-customer-testimonials` | Social proof source. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the landing-page-copy artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-landing-page-design.md.j2` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-landing-page-design.md` | Markdown skeleton: artefact body + per-section table. Generated from `templates/growth-landing-page-design.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/growth-landing-page-design.json` | landing-page-copy JSON skeleton validating against scripts/. |
| `templates/audit-checklist.md.j2` | Copy-auditable landing-page conversion checklist scored /60 (above-the-fold, copy, trust, technical). |
| `templates/audit-checklist.md` | Copy-auditable landing-page conversion checklist scored /60 (above-the-fold, copy, trust, technical). Generated from `templates/audit-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/saas-page-structure.md.j2` | Full SaaS landing-page section-by-section copy skeleton (nav through footer). |
| `templates/saas-page-structure.md` | Full SaaS landing-page section-by-section copy skeleton (nav through footer). Generated from `templates/saas-page-structure.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-landing-page-design.py` | Validate the landing-page-copy artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[growth-customer-testimonials]]
- [[messaging-house-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-landing-page-design.json`

```json
{
  "artefact_id": "growth-landing-page-design-<client>-<YYYY-MM-DD>",
  "owner": "<Full Name> <email>",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "inputs_used": [
    {
      "name": "<input name>",
      "source": "<path or URL>"
    }
  ],
  "findings": [
    {
      "id": "f1",
      "summary": "<finding summary>",
      "severity": "medium"
    }
  ],
  "decision": "<verdict; one sentence>",
  "rationale": "<rationale citing \u22651 input by name; \u226520 chars>"
}
```
