# Testimonial Harvest SOP

## Summary

**One-sentence:** Produces an end-of-engagement harvest artefact (written quote + Loom video + outcome metric) gated by the 3-question script and project-handover trigger.

**One-paragraph:** Solo operators ask for testimonials weeks after handover and get generic praise without metrics. This methodology pins an SOP: trigger at handover (final deliverable accepted), 3-question script (before-state / outcome / what-changed), both written quote AND Loom video captured, ≥1 outcome metric, and explicit publication consent with usage rights scope. Output: a harvest artefact per closed engagement.

**Ефективно для:**

- готова основа для повторюваної задачі «testimonial-harvest-sop» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Engagement has reached final-deliverable acceptance.
- Customer relationship is intact (no dispute / refund).
- Operator has Loom or equivalent recording capacity.

## Skip If (ANY kills it)

- Engagement ended in dispute or refund — no harvest.
- Customer is under NDA preventing any public quote.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Engagement-close trigger event | tracked event | ops |
| 3-question script template | doc | this methodology |
| Consent + usage-rights template | doc | legal / ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/conversion-optimizer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/growth-customer-testimonials` | Downstream placement methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the testimonial-harvest artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/testimonial-harvest-sop.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/testimonial-harvest-sop.json` | testimonial-harvest JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testimonial-harvest-sop.py` | Validate the testimonial-harvest artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-customer-testimonials]]
- [[solo-lead-qualification-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
