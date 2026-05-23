# User Control and Freedom

## Summary

**One-sentence:** Audit and design undo, cancel, redo, exit, and recovery mechanisms so users can escape unwanted states without confirmation fatigue or data loss.

**One-paragraph:** Audit and design undo, cancel, redo, exit, and recovery mechanisms so users can escape unwanted states without confirmation fatigue or data loss.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Workflow allows users to start an irreversible action without a clear escape route.
- Support tickets cite 'how do I undo / cancel / get back' for normal flows.
- Critical actions (delete, send, pay) need consistent recovery affordances.
- Design system lacks documented patterns for undo, confirm, and exit.
- Engineering can implement reversible operations or trash semantics.

## Skip If (ANY kills it)

- Truly irreversible domain (e.g., signed legal commits) — focus on confirm patterns instead.
- Single-action utility with no destructive operations.
- Compliance forbids undo (e.g., regulated submissions).
- Real-time collaborative editor where undo semantics need a CRDT design instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inventory of destructive actions | markdown | Design audit |
| Support-ticket sample on 'undo' keyword | csv | Support tool |
| Design-system pattern catalogue | url | Storybook |
| Engineering feasibility note | markdown | Tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/error-prevention` | Prevention rules set what should never need undo. |
| `solo/ux/ux-ui-designer/error-recovery` | Recovery patterns close the loop after the error. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + run/skip rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-artefact` | sonnet | Section-by-section judgement against the rubric. |
| `lint-and-validate` | haiku | Deterministic schema validation + forbidden-pattern check. |
| `final-review` | opus | Cross-section coherence and stakeholder readiness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-control-freedom.json` | JSON skeleton conforming to the output contract schema. |
| `templates/user-control-freedom.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-control-freedom.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[error-prevention]]
- [[error-recovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
