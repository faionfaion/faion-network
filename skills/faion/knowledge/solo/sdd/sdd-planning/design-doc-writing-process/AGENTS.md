---
slug: design-doc-writing-process
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Run the design-doc writing flow as a four-pass process (skeleton, draft, review, sign-off) with explicit gates so the doc never lands half-written.
content_id: "1ea7ea2d51df604c"
complexity: medium
produces: report
est_tokens: 4200
tags: ["design-doc", "process", "workflow", "review", "async"]
---
# Design Doc Writing Process

## Summary

**One-sentence:** Run the design-doc writing flow as a four-pass process (skeleton, draft, review, sign-off) with explicit gates so the doc never lands half-written.

**One-paragraph:** Design docs rot when they are treated as one-shot writeups. This methodology defines a four-pass flow: pass 1 lays down the skeleton with sections + headings, pass 2 fills sections from spec.md and ADRs, pass 3 collects reviewer feedback in-line, pass 4 resolves comments and ships. Each pass has an explicit gate (skeleton review, draft review, comment resolution, sign-off) so partial drafts cannot slip into the codebase as if they were complete.

**Ефективно для:**

- Solo founder writing the first design doc on a new feature; needs a workflow to avoid blank-page paralysis.
- Team adopting async design-doc reviews; needs explicit gates so reviewers know when to engage.
- Agent that drafts the skeleton; human fills the body; another agent runs lint.
- Migration to SDD where design docs go from optional to mandatory.

## Applies If (ALL must hold)

- Design-doc-structure methodology is in use as the canonical layout.
- At least one reviewer is available for async review.
- Spec.md and relevant ADRs exist before draft starts.
- Doc lives in version control; reviewers can comment via PR.

## Skip If (ANY kills it)

- Trivial change with no design surface — no doc, no process.
- Synchronous-only team where reviewers prefer live whiteboarding.
- Pre-discovery — design problem not yet defined.
- External vendor RFP — different process required.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| templates/design-doc.md | markdown | design-doc-structure |
| spec.md | markdown | Spec methodology |
| Relevant ADRs | markdown | ADR methodology |
| Reviewer list + SLA | team doc | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/design-doc-structure` | Layout the process fills. |
| `solo/sdd/sdd-planning/spec-structure` | Spec.md upstream of the design doc. |

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
| `pass1-skeleton` | haiku | Mechanical header insertion. |
| `pass2-draft` | sonnet | Section-by-section content from inputs. |
| `pass3-review` | opus | Reviewer-side synthesis across the full doc. |
| `pass4-resolve` | sonnet | Comment resolution + final lint. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-doc-writing-process.json` | JSON skeleton conforming to the output contract schema. |
| `templates/design-doc-writing-process.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-doc-writing-process.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-doc-structure]]
- [[design-doc-examples]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
