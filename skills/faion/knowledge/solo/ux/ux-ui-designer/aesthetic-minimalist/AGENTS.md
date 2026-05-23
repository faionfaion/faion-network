---
slug: aesthetic-minimalist
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Apply Nielsen Heuristic #8 — strip irrelevant information using content prioritisation, progressive disclosure, hierarchy, and whitespace so important elements stand out.
content_id: "9b2a743aaacaba26"
complexity: medium
produces: checklist
est_tokens: 3400
tags: ["heuristic", "minimalism", "visual-hierarchy", "ux-design", "nielsen"]
---
# Aesthetic and Minimalist Design

## Summary

**One-sentence:** Apply Nielsen Heuristic #8 — strip irrelevant information using content prioritisation, progressive disclosure, hierarchy, and whitespace so important elements stand out.

**One-paragraph:** Apply Nielsen Heuristic #8 — strip irrelevant information using content prioritisation, progressive disclosure, hierarchy, and whitespace so important elements stand out.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Existing UI shows visual clutter, low contrast hierarchy, or feature creep.
- Adding a new feature risks overloading an already dense page.
- Content audit identified remove / hide / keep candidates needing a rubric.
- Mobile breakpoint forces a simplification pass to fit thumb-reach zone.
- Dashboard or data-heavy screen overwhelms first-time users.

## Skip If (ANY kills it)

- Data-dense tools (analytics, IDE) where density is the value proposition.
- First-pass feature discovery — minimalism assumes features already exist.
- Research has not yet flagged which features are rarely used.
- Marketing or branding surface where richness drives emotion, not utility.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current UI inventory | figma / screenshots | Design system |
| Feature usage analytics | csv | Product analytics |
| Heuristic-evaluation report | markdown | heuristic-evaluation methodology |
| Content audit | markdown | content-audit methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/heuristic-evaluation` | Heuristic-8 violations seed the cleanup backlog. |
| `solo/ux/ux-ui-designer/content-audit` | Content audit decides what is rarely needed. |

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
| `templates/aesthetic-minimalist.json` | JSON skeleton conforming to the output contract schema. |
| `templates/aesthetic-minimalist.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aesthetic-minimalist.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[heuristic-evaluation]]
- [[content-audit]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
