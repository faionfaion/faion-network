---
slug: error-recovery
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Write error messages and recovery flows that name the problem in plain language, point at the offending input, and offer a concrete next action.
content_id: "207312f33d6aa6e7"
complexity: medium
produces: checklist
est_tokens: 3200
tags: ["heuristic", "error-messages", "microcopy", "recovery", "nielsen"]
---
# Help Users Recognise, Diagnose, Recover from Errors

## Summary

**One-sentence:** Write error messages and recovery flows that name the problem in plain language, point at the offending input, and offer a concrete next action.

**One-paragraph:** Write error messages and recovery flows that name the problem in plain language, point at the offending input, and offer a concrete next action.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Forms or workflows surface error states that block progress.
- Support tickets cite confusing error messages or dead-end states.
- Errors include codes, stack traces, or technical jargon shown to end users.
- Recovery requires user action and the path forward is not obvious.
- Design and engineering can collaborate on copy, layout, and instrumentation.

## Skip If (ANY kills it)

- System is back-office only and admins debug from logs.
- Errors are exclusively system-side and surfaced via on-call alerts.
- Microcopy is owned solely by legal and cannot be changed.
- Prototype too early — wait for real backend error catalogue.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Error catalogue | yaml | Backend team |
| Support-ticket sample with error keywords | csv | Support tool |
| Microcopy guidelines | markdown | Content team |
| Component inventory for inline errors | storybook | Design system |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/error-prevention` | Prevention reduces what recovery must handle. |
| `solo/ux/ux-ui-designer/user-control-freedom` | Undo plus recovery is the safety net pair. |

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
| `templates/error-recovery.json` | JSON skeleton conforming to the output contract schema. |
| `templates/error-recovery.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-recovery.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[error-prevention]]
- [[user-control-freedom]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
