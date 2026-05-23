# Micro MVPs

## Summary

**One-sentence:** Produces a micro-MVP spec (single-hypothesis + ≤7-day build + manual back-end allowed + measurable signup-or-pay gate) so a one-week test ships instead of becoming a small MVP.

**Ефективно для:** Solopreneur PMs who write 'MVP' on a doc and 6 weeks later ship a small product instead of a one-week test.

**One-paragraph:** MVP scope-creep is the default failure mode of solo product work. This methodology pins micro-MVPs to a one-week build window, a single falsifiable hypothesis, an allowed manual back-end ('Wizard of Oz' patterns), and a measurable signup-or-pay gate that fires inside the test window. Output is consumed by next-bet decisions in the 30-day post-launch review.

## Applies If (ALL must hold)

- Operator has ≥1 falsifiable product hypothesis ready to test.
- Operator can dedicate ≤7 days of build effort.
- A measurable gate (signup, pay, click) is identifiable.
- Manual back-end / fake back-end is acceptable for the test window.

## Skip If (ANY kills it)

- Hypothesis isn't falsifiable — fix hypothesis first.
- Build effort > 7 days planned — that's not micro; use mvp-scoping methodology instead.
- No measurable gate — test cannot conclude.
- Solution requires automated back-end on day 1 (regulatory / safety) — manual is illegal.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| falsifiable hypothesis | string | founder |
| named gate event | string | founder |
| build budget (≤7 days) | days | operator |
| manual-back-end plan | string | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/mvp-scoping` | Sibling — full MVP method when micro doesn't apply. |
| `solo/product/mvp-instrumentation-checklist` | Downstream — gate event must be instrumented. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `scope_micro_mvp` | haiku | Bounded spec-fill from prereqs. |
| `validate_one_week_window` | sonnet | Bounded judgement: is the build ≤7 days? |
| `gate_review_synthesis` | opus | Post-window synthesis: did the gate fire? |

## Templates

| File | Purpose |
|---|---|
| `templates/micro-mvps.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/micro-mvps.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-micro-mvps.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[mvp-scoping]] — related methodology.
- [[mvp-instrumentation-checklist]] — related methodology.
- [[30-day-post-launch-review-template]] — related methodology.
- [[kill-criteria-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
