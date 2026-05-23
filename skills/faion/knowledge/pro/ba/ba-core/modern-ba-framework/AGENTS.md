---
slug: modern-ba-framework
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a framework-selection decision (BABOK / Lean BA / Product-Ops BA / Hybrid) with explicit fit criteria for the engagement context.
content_id: "2c78881e45c7356c"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: [ba, framework, babok, lean, product-ops]
---
# Modern BA Framework

## Summary

**One-sentence:** Produces a framework-selection decision (BABOK / Lean BA / Product-Ops BA / Hybrid) with explicit fit criteria for the engagement context.

**One-paragraph:** Produces a framework-selection decision (BABOK / Lean BA / Product-Ops BA / Hybrid) with explicit fit criteria for the engagement context. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Новий engagement, де sponsor не диктує framework — потрібен документований вибір.
- Existing framework fails (overhead > value) — треба explicit re-selection.
- Hybrid context (BABOK для compliance + Lean BA для discovery) — треба decision-record.
- BA team з різним досвідом — потрібен стандарт, щоб не варіюватись між БА.

## Applies If (ALL must hold)

- BA engagement is new and framework choice is not yet made.
- Existing framework is failing — re-selection needed.
- Hybrid engagement where multiple frameworks compete (BABOK rigor + Lean speed).
- BA team needs a documented stance to defend against client pushback.

## Skip If (ANY kills it)

- Framework is already mandated by client policy.
- Engagement is too small (< 4 weeks) to justify framework selection ceremony.
- Practice has only one BA — there is no team variance to reconcile.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Engagement context (industry, regulation, team-size) | Markdown | PMO |
| Team experience matrix (BABOK CBAP, Lean, Product-Ops) | Markdown | BA team |
| Sponsor expectations (rigour vs. speed) | Email / interview | sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | framework choice constrains T1 approach |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-context` | haiku | Mechanical fit-scoring per framework axis (rigour, speed, regulation). |
| `pick-and-justify` | opus | Synthesise framework recommendation under conflicting signals. |

## Templates

| File | Purpose |
|------|---------|
| `templates/framework-decision-record.md` | ADR-style framework selection record. |
| `templates/ba-framework-select.sh` | Shell helper running the scoring matrix. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-modern-ba-framework.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[ba-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
