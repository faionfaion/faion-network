---
slug: engineering-ladder-and-growth-plan
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Generates L1-L5 engineering ladder definitions with example artifacts plus a per-engineer growth-plan + promo-packet — pins career steps so juniors stay."
content_id: "11587182dc5d8681"
complexity: medium
produces: spec
est_tokens: 3600
tags: [pm, career-ladder, growth-plan, promo-packet, engineering-management]
---
# Engineering Ladder And Growth Plan

## Summary

**One-sentence:** Generates L1-L5 engineering ladder definitions with example artifacts plus a per-engineer growth-plan + promo-packet — pins career steps so juniors stay.

**One-paragraph:** Generates L1-L5 engineering ladder definitions with example artifacts plus a per-engineer growth-plan + promo-packet — pins career steps so juniors stay. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** EM-у/тех-ліду — щоб синьйор / джуніор бачив наступний крок, а не звільнявся.

## Applies If (ALL must hold)

- Engineering org has ≥5 engineers across ≥2 levels.
- At least one engineer has flagged 'unclear growth path' in the last review.
- A named owner (EM or VPE) is accountable for refreshing the ladder annually.
- Promo decisions currently happen — even if informally.

## Skip If (ANY kills it)

- Team < 5 engineers — ladder overhead exceeds value; use direct mentoring.
- No named owner — anonymous ladders rot in 6 months.
- Org already adopted a public ladder (Patrick Kua, Rent the Runway) — fork it, do not re-author.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current engineer roster + levels | CSV/HR export | HRIS |
| Prior promo decisions | doc/notes | promo committee history |
| Reference ladders | links | Patrick Kua / Square / Rent-the-Runway public ladders |
| Named owner sign-off | email | EM or VPE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager/1on1-template-managers` | 1:1 cadence the growth plan attaches to. |
| `geek/pm/project-manager/cross-role-handoff-protocol` | Handoff stages the artefacts in the ladder reference. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-ladder-levels` | haiku | L1-L5 skeleton fill from reference ladders. |
| `calibrate-against-references` | sonnet | Per-level judgement: does Square L3 map to our L3? |
| `growth-plan-synthesis` | opus | Per-engineer synthesis — needs cross-context reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Canonical ladder skeleton with L1-L5 placeholders, growth-plan section, promo-packet block. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-engineering-ladder-and-growth-plan.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[1on1-template-managers]]
- [[cross-role-handoff-protocol]]
- [[delivery-maturity-rubric]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether the full ladder is authored (≥5 engineers + named owner + growth complaints), blocked (no owner), or skipped (small team). Run before any reference-ladder reading begins.
