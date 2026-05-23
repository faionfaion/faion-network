---
slug: wireframing
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Builds the lowest-fidelity-that-still-answers-the-question wireframe in 30-60 minutes: information hierarchy, layout grid, primary actions, and content slots — explicitly stripped of visual polish to keep stakeholder feedback on structure not aesthetics.
content_id: "149f32cedf514639"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["wireframing", "low-fidelity", "structure", "layout", "ux"]
---
# Wireframing

## Summary

**One-sentence:** Builds the lowest-fidelity-that-still-answers-the-question wireframe in 30-60 minutes: information hierarchy, layout grid, primary actions, and content slots — explicitly stripped of visual polish to keep stakeholder feedback on structure not aesthetics.

**One-paragraph:** Wireframes fail when designers polish them before alignment is reached. This methodology pins a four-section format (information hierarchy, layout grid, primary actions, content slots) and a deliberate low-fidelity treatment (grayscale, system font, no imagery). The 30-60 minute time-box prevents premature polish; wireframes graduate to medium-fidelity only after the structure is signed off.

**Ефективно для:**

- Solo designer needing to align on structure before investing visual time.
- Founder + remote stakeholder where Figma high-fidelity sends wrong signal.
- AI agent generating wireframe variants where polish would mislead reviewers.
- Pre-mortem on a screen where the team is debating layout vs aesthetics.

## Applies If (ALL must hold)

- A new screen or flow needs structural alignment before visual design.
- Stakeholders are available for a 30-min wireframe review.
- 30-60 minute time-box can be respected.
- Wireframe will graduate to higher-fidelity AFTER structure sign-off.

## Skip If (ANY kills it)

- Structure is already signed off — go to medium-fidelity directly.
- Single-component micro-change with no structural impact.
- High-stakes investor demo where wireframes send wrong signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Screen or flow brief | doc | PM / designer |
| Layout grid spec | tokens or grid system | Design system |
| Content inventory | list | Content design / PM |
| Time-box (30-60 min) | integer | Designer calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/design-tokens-fundamentals` | Grid + spacing tokens used as guides. |
| `solo/ux/stakeholder-walkthrough-script` | Structured walkthrough for sign-off. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-wireframe` | sonnet | Per-screen judgement on hierarchy + action placement. |
| `validate-fidelity-discipline` | haiku | Deterministic check on grayscale + no-imagery rule. |
| `multi-screen-flow-audit` | opus | Cross-screen synthesis for a flow. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wireframing.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/wireframing.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wireframing.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-tokens-fundamentals]]
- [[stakeholder-walkthrough-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
