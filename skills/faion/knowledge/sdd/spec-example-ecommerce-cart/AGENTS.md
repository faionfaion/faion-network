# Spec Example: Ecommerce Cart

## Summary

**One-sentence:** Provide a fully worked one-pager spec for an ecommerce shopping cart feature so writers see a realistic instantiation of the spec-structure template.

**One-paragraph:** An ecommerce cart is the canonical worked spec example: well-bounded scope, clear users, explicit non-goals (no discount engine, no multi-currency), testable AC, and three open questions. This methodology ships the example as a copy-and-adapt starting point; the front-matter records the archetype so reviewers can calibrate. The example is updated whenever spec-structure changes so it never drifts from the template.

**Ефективно для:**

- Engineer writing their first spec on a small team; needs a worked example to gauge scope.
- Reviewer comparing a draft spec against a known-good baseline.
- Agent generating spec from discovery output; example anchors structure.
- Onboarding new team members to spec conventions.

## Applies If (ALL must hold)

- Spec-structure methodology is the canonical layout.
- The current feature resembles an ecommerce-cart-shaped scope (single-team, well-bounded, testable AC).
- Author wants to copy + adapt rather than build from scratch.
- Example version matches the spec-structure version.

## Skip If (ANY kills it)

- Feature is multi-team or regulated — use spec-advanced-guidelines example instead.
- Author prefers blank-page authoring.
- Pre-discovery — feature scope not yet defined.
- Example version is stale — re-sync first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| spec-structure spec | markdown | spec-structure |
| templates/cart-spec.md | markdown | This methodology |
| Discovery output | markdown | Discovery methodology |
| User persona | markdown | Persona doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | Template the example instantiates. |
| `solo/sdd/sdd-planning/spec-examples-basic` | Sibling examples covering basic shapes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `adapt-example` | sonnet | Substitute domain-specific terms. |
| `lint-adapted-spec` | haiku | Format check against spec-structure. |
| `review` | sonnet | Reviewer compares against example. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-example-ecommerce-cart.json` | JSON skeleton conforming to the output contract schema. |
| `templates/spec-example-ecommerce-cart.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spec-example-ecommerce-cart.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-structure]]
- [[spec-examples-basic]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
