# Spec Structure

## Summary

**One-sentence:** Pin the canonical spec layout (problem, users, goals, non-goals, requirements, AC, open questions) so every spec fits one page and reviewers know exactly where to look.

**One-paragraph:** Specs that wander across layouts waste reviewer cycles. This methodology pins the seven-section canonical layout — problem, users, goals, non-goals, requirements, acceptance criteria, open questions — and caps the core at one page. Sections may be marked N/A with a one-line justification but never omitted. The structure is enforced by a validator so downstream agents (design.md drafter, impl-plan generator) can parse the spec without LLM intervention.

**Ефективно для:**

- Solo founder writing spec for engineering handoff; one-page cap forces clarity.
- Reviewer scanning multiple specs per week; predictable layout cuts scan time.
- Agent generating design.md from spec; predictable layout enables parsing.
- Onboarding new collaborators to the spec convention.

## Applies If (ALL must hold)

- Spec is part of the SDD flow.
- Reviewers need predictable layout to scan efficiently.
- Downstream agents will consume the spec.
- Spec lives in version control.

## Skip If (ANY kills it)

- Trivial 1-line config change — no spec needed.
- Spike or research task — different format applies.
- External vendor RFP — different format.
- Free-form discovery doc — pre-spec.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| templates/spec.md | markdown | This methodology |
| Discovery output | markdown | Discovery methodology |
| User persona doc | markdown | Persona doc |
| AC rubric | rubric | ac-quality-rubric |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-requirements` | Numbering format this layout hosts. |
| `solo/sdd/sdd-planning/spec-example-ecommerce-cart` | Canonical worked example. |

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
| `draft-spec` | sonnet | Section-by-section reasoning from discovery. |
| `lint-structure` | haiku | Section-presence check. |
| `review-spec` | opus | Cross-section coherence audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-structure.json` | JSON skeleton conforming to the output contract schema. |
| `templates/spec-structure.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spec-structure.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-requirements]]
- [[spec-example-ecommerce-cart]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
