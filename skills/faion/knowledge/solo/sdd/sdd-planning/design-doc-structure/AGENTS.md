---
slug: design-doc-structure
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pin the canonical design-doc layout (context, design, alternatives considered, risks, rollout) so every team member produces a doc reviewers can scan in one pass.
content_id: "78076e216ebb4b87"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["design-doc", "structure", "layout", "template", "sdd"]
---
# Design Doc Structure

## Summary

**One-sentence:** Pin the canonical design-doc layout (context, design, alternatives considered, risks, rollout) so every team member produces a doc reviewers can scan in one pass.

**One-paragraph:** A team-wide design-doc structure prevents the 'every doc looks different' problem that wastes reviewer cycles. The five-section canonical layout — context, proposed design, alternatives, risks, rollout — covers 90% of cases; advanced patterns layer on top via design-doc-advanced-patterns. The structure is enforced at the template level: writers cannot remove sections, only mark them N/A with a one-line justification.

**Ефективно для:**

- Team adopting design docs for the first time; needs a shared layout to stop bikeshedding.
- Solo founder writing a doc that future agents must consume; structure must be machine-parseable.
- Reviewer scanning multiple docs per week; predictable layout cuts review time in half.
- Migration to specification-driven development — design doc slots in between spec.md and impl-plan.md.

## Applies If (ALL must hold)

- Team or solo founder writes design docs as part of SDD flow.
- Reviewers need a predictable layout to scan efficiently.
- Spec.md and impl-plan.md already exist; design doc fits between them.
- Doc will be stored in repo (not wiki) for agent file-system access.

## Skip If (ANY kills it)

- Trivial change with no architectural surface — no design doc needed.
- Pure exploration where the doc would invent a design that does not exist yet.
- External vendor RFP — different layout required.
- Doc lives in a non-version-controlled tool (Confluence) — methodology assumes filesystem access.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| spec.md | markdown | Spec methodology output |
| Relevant ADRs | markdown | ADR methodology output |
| templates/design-doc.md | markdown | This methodology |
| Reviewer list | list | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | Spec.md upstream of the design doc. |
| `solo/sdd/sdd-planning/architecture-decision-records` | ADRs referenced as AD-X citations in the design. |

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
| `draft-design-doc` | sonnet | Section-by-section reasoning from spec + ADRs. |
| `check-structure` | haiku | Deterministic section-presence lint. |
| `review-design` | opus | Cross-document synthesis — design + ADRs + impl-plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-doc-structure.json` | JSON skeleton conforming to the output contract schema. |
| `templates/design-doc-structure.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-doc-structure.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-structure]]
- [[design-doc-writing-process]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
