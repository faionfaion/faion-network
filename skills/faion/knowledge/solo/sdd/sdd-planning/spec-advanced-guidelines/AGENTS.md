---
slug: spec-advanced-guidelines
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Apply advanced spec patterns (NFR table, AC rubric, glossary, versioning, source-of-truth pointer) on top of the standard spec when the feature is multi-team, regulated, or long-lived.
content_id: "8d723aec0e9943e8"
complexity: deep
produces: spec
est_tokens: 4200
tags: ["spec", "advanced", "nfr", "ac-rubric", "glossary", "versioning"]
---
# Spec Advanced Guidelines

## Summary

**One-sentence:** Apply advanced spec patterns (NFR table, AC rubric, glossary, versioning, source-of-truth pointer) on top of the standard spec when the feature is multi-team, regulated, or long-lived.

**One-paragraph:** Standard one-pager specs work for solo + small-team features. Advanced patterns kick in when specs must survive multi-team review, regulation, or longevity beyond 12 months. This methodology layers five optional blocks — NFR table, AC quality rubric, glossary, versioning record, source-of-truth pointer — onto spec-structure, with explicit triggers for when each block is mandatory.

**Ефективно для:**

- Specs for regulated features (PII, payments, health) needing NFR + glossary.
- Long-lived specs (>12 months) where versioning record matters.
- Multi-team specs where AC quality rubric reduces back-and-forth.
- Source-of-truth specs that other systems reference by ID.

## Applies If (ALL must hold)

- Base spec (spec-structure) already exists in draft.
- Feature is multi-team, regulated, or long-lived.
- Reviewers need rubric + NFRs to align expectations.
- Spec is expected to remain a source of truth >12 months.

## Skip If (ANY kills it)

- Single-team solo-week feature — base spec is enough.
- Spike or short-lived experiment — overhead exceeds benefit.
- Pre-discovery — assumptions still being tested.
- Internal tool with no regulatory or long-life concern.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Base spec draft | markdown | spec-structure |
| NFR catalogue | rubric | Internal |
| AC quality rubric | rubric | ac-quality-rubric |
| Glossary template | markdown | Internal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | Base layout this methodology extends. |
| `solo/sdd/sdd-planning/spec-requirements` | Requirement formats this methodology refines. |

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
| `nfr-block` | sonnet | Per-NFR judgement against catalogue. |
| `ac-rubric-pass` | sonnet | Apply AC rubric to every criterion. |
| `glossary` | haiku | Term-by-term definition lookup. |
| `audit-versioning` | opus | Multi-revision synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-advanced-guidelines.json` | JSON skeleton conforming to the output contract schema. |
| `templates/spec-advanced-guidelines.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spec-advanced-guidelines.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-structure]]
- [[spec-requirements]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
