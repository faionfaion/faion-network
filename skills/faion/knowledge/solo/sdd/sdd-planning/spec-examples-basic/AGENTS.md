---
slug: spec-examples-basic
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Ship a small catalogue of basic spec examples (CRUD feature, integration, internal tool, polish) covering the most common shapes a solo team writes.
content_id: "eddc3ed9640addd4"
complexity: light
produces: spec
est_tokens: 3500
tags: ["spec", "examples", "basic", "worked-examples", "starter"]
---
# Spec Examples Basic

## Summary

**One-sentence:** Ship a small catalogue of basic spec examples (CRUD feature, integration, internal tool, polish) covering the most common shapes a solo team writes.

**One-paragraph:** Solo teams hit a small number of common spec shapes repeatedly: CRUD feature, third-party integration, internal tool, polish/refactor. This methodology ships a tight catalogue of four worked basic examples covering each shape. Each example is fully filled in, archetype-tagged, and version-coupled with spec-structure. Authors pick by archetype, copy, and adapt; reviewers compare against the example for tone and depth.

**Ефективно для:**

- Solo founder writing their tenth spec; wants a closer-fit example than the generic one.
- Agent generating spec from discovery output; archetype anchors structure.
- Reviewer scanning multiple specs per week; consistent examples cut review time.
- Onboarding new solo collaborators to the spec convention.

## Applies If (ALL must hold)

- Spec-structure methodology is in use.
- The current spec fits one of the four basic archetypes.
- Author wants a closer match than the canonical ecommerce-cart example.
- Examples are version-coupled with spec-structure.

## Skip If (ANY kills it)

- Spec needs advanced patterns (NFR, glossary, versioning) — use spec-advanced-guidelines example.
- Author prefers blank-page authoring.
- Pre-discovery — feature scope unknown.
- Example versions stale — re-sync first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| spec-structure spec | markdown | spec-structure |
| Four worked basic examples | markdown | templates/ |
| Archetype selector | decision tree | This methodology |
| Discovery output | markdown | Discovery methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | Template these examples instantiate. |
| `solo/sdd/sdd-planning/spec-example-ecommerce-cart` | Canonical worked example, larger-scoped sibling. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-archetype` | haiku | Match feature to one of four archetypes. |
| `adapt-example` | sonnet | Substitute domain terms. |
| `compare-review` | sonnet | Reviewer compares draft against example. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-examples-basic.json` | JSON skeleton conforming to the output contract schema. |
| `templates/spec-examples-basic.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spec-examples-basic.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-structure]]
- [[spec-example-ecommerce-cart]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
