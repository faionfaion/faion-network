---
slug: writing-specifications
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: A 9-phase process producing spec.md with SMART functional requirements, personas, user stories, Given-When-Then acceptance criteria, and explicit scope boundaries before any design or code is written.
content_id: "4a0eca19120a99d7"
complexity: deep
produces: spec
est_tokens: 4500
tags: [specification, requirements, sdd, smart-criteria, user-stories]
---
# Writing Specifications

## Summary

**One-sentence:** A 9-phase process producing spec.md with SMART functional requirements, personas, user stories, Given-When-Then acceptance criteria, and explicit scope boundaries before any design or code is written.

**One-paragraph:** A 9-phase process producing spec.md with SMART functional requirements, personas, user stories, Given-When-Then acceptance criteria, and explicit scope boundaries before any design or code is written. The methodology pins the artefact: stable IDs (FR-X, US-X, AC-X), traceability between layers, a versioned header, and an out-of-scope list that prevents later scope creep.

**Ефективно для:**

- Solo founders codifying feature intent before they start coding.
- Teams who keep diverging on WHAT a feature is supposed to do.
- Spec-driven workflows where downstream design and tasks must trace back to a single artefact.
- Audit / hand-off surface: every requirement has an ID, an AC, and a known status.

## Applies If (ALL must hold)

- Feature is new and requirements have not been written down anywhere.
- Existing feature needs scope expansion and the current spec is absent or too vague to drive design.
- Stakeholder and developer have different mental models of what the feature does.
- Requirements exist informally (Slack messages, verbal agreements) and need to be formalized.

## Skip If (ANY kills it)

- Bug report with a clear reproduction path — write a task directly, not a spec.
- Infrastructure change with no user-visible behavior — record it in constitution.md instead.
- Feature already has an approved spec — open and amend it rather than rewriting from scratch.
- Experiment/spike whose output will determine whether to proceed at all.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| constitution.md | markdown | Repo root |
| done/ feature specs | markdown | SDD archive |
| Problem statement | text | Stakeholder interview |
| Persona list (≥2) | markdown | Research notes |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/sdd-workflow-overview` | Names the phase order and gating between spec/design/impl-plan. |
| `solo/sdd/sdd/yaml-frontmatter` | Defines the metadata schema embedded at the top of spec.md. |

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
