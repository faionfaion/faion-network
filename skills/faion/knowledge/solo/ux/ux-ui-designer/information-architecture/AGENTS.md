---
slug: information-architecture
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Translate IA framework decisions into a sitemap, taxonomy, and navigation spec that the design team can build against without re-deriving the structure.
content_id: "10facf6f10a90242"
complexity: deep
produces: spec
est_tokens: 4200
tags: ["information-architecture", "sitemap", "navigation-spec", "design-system", "ux-design"]
---
# Information Architecture (Designer Surface)

## Summary

**One-sentence:** Translate IA framework decisions into a sitemap, taxonomy, and navigation spec that the design team can build against without re-deriving the structure.

**One-paragraph:** Translate IA framework decisions into a sitemap, taxonomy, and navigation spec that the design team can build against without re-deriving the structure.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Designers need to start screen design but the IA decisions are unwritten.
- Sitemap and taxonomy need to be visible in the design tool, not only docs.
- Cross-team handover requires a single navigation spec.
- Component library can be wired against the spec (nav, breadcrumb, footer).
- Designers will own ongoing IA hygiene as new pages are added.

## Skip If (ANY kills it)

- No agreed IA framework yet — run ia-framework first.
- Single landing page with no hierarchy.
- Engineering team will derive IA from CMS schema independently.
- Reorganisation halted until further user research.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved IA framework | markdown | ia-framework methodology |
| Content inventory | csv | Content audit |
| Component library | storybook | Design system |
| Brand and labelling rules | markdown | Design system |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/ia-framework` | Framework decisions drive the designer-facing spec. |
| `solo/ux/ux-researcher/ia-templates` | Templates seed sitemap, taxonomy, and nav spec. |

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
| `templates/information-architecture.json` | JSON skeleton conforming to the output contract schema. |
| `templates/information-architecture.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-information-architecture.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[ia-framework]]
- [[ia-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
