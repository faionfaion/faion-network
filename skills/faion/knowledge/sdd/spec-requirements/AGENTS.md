# Spec Requirements

## Summary

**One-sentence:** Write functional and non-functional requirements in a numbered, testable form (FR-NNN, NFR-NNN) so engineering can map each to a test and reviewers can audit coverage.

**One-paragraph:** Requirements without numbering and testability rot fast: 'the system should be fast' cannot be regression-checked. This methodology pins the format — FR-NNN for functional, NFR-NNN for non-functional — each with one-sentence statement, verification method, and priority (must/should/could). Numbers are stable across revisions so downstream docs can reference FR-7 forever. The spec validator enforces non-empty verification method and forbids vague language.

**Ефективно для:**

- Solo founder writing spec for a feature that will live >6 months; FR-NNN gives stable anchors for tests.
- Reviewer auditing requirement coverage against test plan.
- Agent generating impl-plan from spec; numbered FRs map cleanly to TASKs.
- Migration projects where old + new behaviour must be cleanly enumerated.

## Applies If (ALL must hold)

- Spec is part of the SDD flow (spec.md → design.md → impl-plan.md).
- Requirements must be machine-traceable to tests and tasks.
- Feature surface is large enough to need numbering (>3 requirements).
- Reviewers need a coverage matrix.

## Skip If (ANY kills it)

- Spec for a 1-line config change.
- Spike or research task where output is learning.
- Pre-discovery — requirements still being elicited.
- Single-test-case feature where numbering is overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| spec-structure layout | markdown | spec-structure |
| Discovery output | markdown | Discovery methodology |
| NFR catalogue | rubric | Internal |
| Priority rubric | rubric | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | Envelope this methodology fills. |
| `solo/sdd/sdd-planning/spec-advanced-guidelines` | Advanced patterns layered on top. |

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
| `draft-fr-nfr` | sonnet | Per-requirement judgement against catalogue. |
| `lint-requirements` | haiku | Format + vague-language check. |
| `audit-coverage` | opus | Multi-document synthesis (spec ↔ tests ↔ tasks). |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-requirements.json` | JSON skeleton conforming to the output contract schema. |
| `templates/spec-requirements.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spec-requirements.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-structure]]
- [[spec-advanced-guidelines]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
