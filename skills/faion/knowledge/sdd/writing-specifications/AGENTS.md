# Writing Specifications (SDD core)

## Summary

**One-sentence:** Author spec.md as the canonical WHAT/WHY artefact for an SDD feature — SMART functional requirements, Given-When-Then acceptance criteria, explicit scope boundaries, and a versioned header — written for LLM agent consumption.

**One-paragraph:** Author spec.md as the canonical WHAT/WHY artefact for an SDD feature — SMART functional requirements, Given-When-Then acceptance criteria, explicit scope boundaries, and a versioned header — written for LLM agent consumption. The methodology pins the artefact: stable FR-X / NFR-X / AC-X / US-X identifiers, an explicit out-of-scope list, and a one-paragraph problem statement that downstream design and impl-plan must honour verbatim.

**Ефективно для:**

- SDD pipelines feeding spec to design + impl-plan + pool executors.
- Solo founders writing spec for an LLM agent to design and implement.
- Reviewers checking that what was promised matches what is built.
- Audit surface: every FR has an id, an AC, and a status.

## Applies If (ALL must hold)

- A new SDD feature is being started.
- Spec.md does not yet exist or is too vague to drive design.
- Downstream agents (design, impl-plan) will consume the spec verbatim.

## Skip If (ANY kills it)

- Bug fix with clear repro — write a task, not a spec.
- Infra change with no user-visible surface.
- Feature already has an approved spec.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| constitution.md | markdown | Repo root |
| Problem statement | text | Stakeholder |
| Persona list (≥2) | markdown | Research notes |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/sdd-workflow-overview` | Defines where spec sits in the SDD lifecycle. |

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
| `draft-writing-specifications` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-writing-specifications` | haiku | Schema check + threshold checks; deterministic. |
| `review-writing-specifications` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/writing-specifications.json` | JSON skeleton conforming to the output contract schema. |
| `templates/writing-specifications.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-writing-specifications.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[sdd-workflow-overview]]
- [[writing-design-documents]]
- [[writing-implementation-plans]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
