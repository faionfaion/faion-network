# Product Discovery

## Summary

**One-sentence:** Run a discovery cycle that maps assumptions across four risk types (Value/Usability/Feasibility/Business-Viability), designs cheap falsifiable experiments with explicit kill thresholds, and emits a go/pivot/kill spec.

**One-paragraph:** Classifies every assumption into one of four risk types, sorts by severity, and runs 1-2 cheap experiments per cycle against the highest-severity assumption first. Every experiment carries a hypothesis, success threshold, and kill threshold so the cycle ends with an unambiguous proceed/pivot/kill decision rather than 'more data'.

**Ефективно для:**

- Solo founder or PM staring at a backlog of unvalidated ideas — needs a 1-4 week cycle that ends with kill/continue/double-down based on evidence, not opinion.

## Applies If (ALL must hold)

- Before committing engineering capacity to a new feature, product, or market segment.
- Stakeholder request lacks evidence and needs a structured assumption test.
- Analytics flags drop-off or churn and root cause is unknown before solutioning.
- Entering an unfamiliar domain where all four risk types are open.

## Skip If (ANY kills it)

- Pure execution work where all four risks are already addressed by existing evidence.
- Time-bounded compliance or contractual deliverables — discovery cannot move the deadline.
- Trivial features (<2 days) where running an experiment costs more than building.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Idea or feature brief | markdown | PM doc / backlog ticket |
| Customer access list | csv | CRM / community |
| Risk severity rubric | table | team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/continuous-discovery` | Cadence layer that feeds raw signals into discovery cycles. |
| `solo/product/product-manager/spec-writing` | Downstream artefact when discovery emits a proceed decision. |

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
| `draft-product-discovery` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-product-discovery` | haiku | Schema check + threshold checks; deterministic. |
| `review-product-discovery` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/product-discovery.json` | JSON skeleton conforming to the output contract schema. |
| `templates/product-discovery.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-discovery.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[continuous-discovery]]
- [[spec-writing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
