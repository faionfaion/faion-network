# Audience to Paid Conversion Loop

## Summary

**One-sentence:** Generates an iterating audience→paid loop spec — cohort definition, conversion event, attribution window, A/B variant, learn-step — gated by frozen window per test.

**One-paragraph:** Solo founders move newsletter signups into paid by 'testing things' without freezing attribution windows. This methodology pins a 6-step loop: define cohort → declare conversion event → freeze attribution window → ship one variant → wait the full window → record + decide. Output: a LoopRunArtefact per cycle with cohort_size, conversion_rate, window_days, variant, decision (keep / drop / iterate).

**Ефективно для:**

- Solo founder with audience that doesn't pay yet.
- Newsletter → paid conversion experiments that need rigour.
- A/B testing where retroactive window-shopping has skewed past results.
- Multi-cohort analysis (early subs vs late subs) at small N.

## Applies If (ALL must hold)

- Audience exists (≥200 subscribers OR ≥1000 monthly visitors).
- There's a defined paid conversion event (trial start, purchase, upgrade).
- Operator can run ≥1 variant change per loop cycle.
- Attribution can be tracked end-to-end (analytics + payment).

## Skip If (ANY kills it)

- Pre-audience: no subscribers / traffic to test on.
- Audience too small for any signal (<50 subs).
- Enterprise sales cycle measured in months — different methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cohort definition | SQL query / segment filter | analytics |
| Conversion event spec | tracked event name + value | payment + analytics |
| Variant set | control + 1 treatment | operator hypothesis |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| audience-to-customer-funnel | Cohort + conversion event align with funnel stage definitions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-frozen-attribution-window, r2-one-variant-per-loop, r3-cohort-size-min, r4-named-owner, r5-decision-after-full-window | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Audience to Paid Conversion Loop artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: window-shopping, multi-variant-noise, tiny-cohort-conclusion, decision-before-window | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-loop-spec` | sonnet | Per-cycle definition with stakes. |
| `analyse-loop-result` | sonnet | Variant comparison at small N. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audience-to-paid-conversion-loop.json` | LoopRunArtefact JSON skeleton. |
| `templates/audience-to-paid-conversion-loop.md` | Loop log + decision rationale. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audience-to-paid-conversion-loop.py` | Validate LoopRunArtefact JSON against the schema. | End of each loop cycle. |

## Related

- [[audience-to-customer-funnel]]
- [[brand-voice-consistency-system]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
