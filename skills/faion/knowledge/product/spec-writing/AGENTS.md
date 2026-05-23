# Spec Writing

## Summary

**One-sentence:** Write a one-pager spec containing problem / users / goals / non-goals / requirements / acceptance criteria / open questions, ready for an engineer to start without follow-up calls.

**One-paragraph:** A spec must answer 'what are we building and why' in one screen. The 7-section template forces decisions on goals vs non-goals and acceptance criteria upfront so engineering can scope confidently. Open questions are surfaced rather than hidden so the spec can be reviewed and signed.

**Ефективно для:**

- Solo PM/founder writing for a 1-2 engineer team; needs a spec that survives async review and ends with engineering able to start without scheduling a kickoff.

## Applies If (ALL must hold)

- Feature scope >2 dev-days and engineering needs context.
- Acceptance criteria need to be agreed before implementation.
- Spec will be reviewed by ≥1 reviewer other than the author.

## Skip If (ANY kills it)

- Bug fix or trivial change where the ticket title is sufficient.
- Spike or research task where the output is the learning, not the artefact.
- Pre-discovery — assumptions are still being tested.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem brief | markdown | Discovery output / PM doc |
| Target user persona | markdown | Research / CRM |
| Acceptance criteria rubric | rubric | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager/product-discovery` | Discovery output feeds the problem + users sections. |
| `solo/product/product-planning/ac-quality-rubric` | Quality bar for acceptance criteria within the spec. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-spec-writing` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-spec-writing` | haiku | Schema check + threshold checks; deterministic. |
| `review-spec-writing` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-writing.json` | JSON skeleton conforming to the output contract schema. |
| `templates/spec-writing.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spec-writing.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[product-discovery]]
- [[ac-quality-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
