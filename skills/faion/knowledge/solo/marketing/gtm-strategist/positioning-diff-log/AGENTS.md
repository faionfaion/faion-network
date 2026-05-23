---
slug: positioning-diff-log
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an ADR-style positioning diff log entry: trigger, old wording, new wording, expected effect, 30/90-day check metrics — every change to the positioning statement gets captured so iterations stop disappearing into git.
content_id: "631823a7c80706dc"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["positioning", "adr", "log", "decisions", "marketing", "solo"]
---
# Positioning Diff Log

## Summary

**One-sentence:** Generates an ADR-style positioning diff log entry: trigger, old wording, new wording, expected effect, 30/90-day check metrics — every change to the positioning statement gets captured so iterations stop disappearing into git.

**One-paragraph:** Positioning Diff Log produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder iterating on positioning who needs an ADR-style log capturing every wording change with trigger, expected effect, and 30/90-day check metric — before positioning evolves without rationale.

## Applies If (ALL must hold)

- There IS a current positioning statement (even draft)
- Founder iterates positioning ≥1x per quarter
- Has access to a metric surface (signups, demos, replies) to measure effect

## Skip If (ANY kills it)

- No positioning statement exists yet — write one before logging diffs
- Brand-only positioning with no measurable metric — different governance
- Static brand 5+ years stable — over-engineered for no change

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current positioning statement | doc | marketing brief / landing page |
| Metric surface (analytics + ESP + CRM) | stack | ops dashboard |
| Trigger event for the change (sales call, churn, repositioning campaign) | doc | founder log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `freelancer-positioning-content-calendar` | Calendar pillars depend on positioning. |
| `objection-bank` | Top objections often trigger positioning diffs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-one-entry-per-change, r2-trigger-named, r3-old-and-new-wording-verbatim, r4-expected-effect-falsifiable, r5-30-90-day-check, r6-named-owner | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-positioning-diff-log` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-positioning-diff-log` | haiku | Schema check + threshold checks; deterministic. |
| `review-positioning-diff-log` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/positioning-diff-log.json` | JSON skeleton conforming to the output contract schema. |
| `templates/positioning-diff-log.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-positioning-diff-log.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[freelancer-positioning-content-calendar]]
- [[objection-bank]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
