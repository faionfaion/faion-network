# Customer Testimonials and Social Proof

## Summary

**One-sentence:** Produces a testimonial bank artefact mapping each named-customer quote to placement, proof-tier, and refresh date — gated by attribution completeness.

**One-paragraph:** Solo marketers paste generic testimonials at the page bottom and never refresh them; conversion impact is near-zero. This methodology pins a testimonial bank: every quote anchored to a named customer with role + company + photo, mapped to a buying stage (awareness / consideration / decision / purchase), refreshed annually, with at least one testimonial within visual proximity of every CTA. Output: a versioned testimonial-bank spec consumable by landing-page templates.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-customer-testimonials» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Landing-page CVR below benchmark OR social proof is absent / generic.
- ≥3 paying customers exist with ≥1 measurable win each.
- Operator has authority to publish customer quotes (or a consent process).

## Skip If (ANY kills it)

- No paying customers yet — fabricated testimonials are worse than none.
- Regulated industry requiring legal review of every customer quote.
- B2B enterprise with multi-month approval chains — use logo wall instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Customer list with win events | CSV / spreadsheet | CRM or customer-success log |
| Consent template for quote publication | doc | legal / ops |
| Landing-page wireframe with CTA positions | image / Figma | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/conversion-optimizer/testimonial-harvest-sop` | Upstream harvest procedure feeding raw quotes. |
| `solo/marketing/content-marketer/` | Parent role / operating context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the testimonial-bank artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/growth-customer-testimonials.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-customer-testimonials.json` | testimonial-bank JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-customer-testimonials.py` | Validate the testimonial-bank artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[testimonial-harvest-sop]]
- [[growth-landing-page-design]]
- [[eeat-signal-pass-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
