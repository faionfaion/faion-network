# MVP Scoping

## Summary

**One-sentence:** Scope an MVP that tests one riskiest assumption with ≤2 weeks build, ≥10 segment users, and explicit kill / success thresholds — defends scope against feature creep.

**One-paragraph:** Scopes an MVP from the bottom up: name riskiest assumption → minimum journey that tests it → cut everything else. Defends scope against creep with an explicit Now/Not-Now policy. Ship date is a function of scope, not a wish.

**Ефективно для:**

- Solo founder whose MVPs keep landing as full products — needs a scoping discipline that holds scope under stakeholder pressure.

## Applies If (ALL must hold)

- Riskiest assumption is named.
- ≥10 segment users reachable.
- ≤2 weeks build capacity available.

## Skip If (ANY kills it)

- Compliance / contractual scope blocks bottom-up cuts.
- Risk requires multi-week build (use Micro-MVP series instead).
- Pre-discovery — no riskiest assumption yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Riskiest assumption | string | Discovery |
| Reachable segment | csv | CRM |
| Build capacity estimate | estimate | Plan |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/minimum-product-frameworks` | Frame selection routing to MVP. |
| `solo/product/product-planning/micro-mvp-cut-rubric` | Sub-tool for scope-cutting. |

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
| `draft-mvp-scoping` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-mvp-scoping` | haiku | Schema check + threshold checks; deterministic. |
| `review-mvp-scoping` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mvp-scoping.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/mvp-scoping.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/mvp-scoping.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/mvp-quick-check.md.j2` | 5-question MVP sanity check with a capacity check. |
| `templates/mvp-quick-check.md` | 5-question MVP sanity check with a capacity check. Generated from `templates/mvp-quick-check.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/mvp-scope-doc.md.j2` | Full MVP scope document. |
| `templates/mvp-scope-doc.md` | Full MVP scope document. Generated from `templates/mvp-scope-doc.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[minimum-product-frameworks]]
- [[micro-mvp-cut-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
