---
slug: tech-debt-budget-for-solos
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Tech-debt budget for solos: 20%-of-cycle cap, named ledger with impact + interest, ship-vs-pay decision per item, monthly review, owner sign-off.
content_id: "d59cdbc293de01dc"
complexity: medium
produces: spec
est_tokens: 5000
tags: [tech-debt, solo, budget, ledger, refactor]
---
# Tech-Debt Budget for Solos

## Summary

**One-sentence:** Tech-debt budget for solos: 20%-of-cycle cap, named ledger with impact + interest, ship-vs-pay decision per item, monthly review, owner sign-off.

**One-paragraph:** Enterprise tech-debt frameworks demand committees the solo cannot afford. This methodology produces a 1-page debt ledger sized for a solopreneur: each item carries an impact estimate, an interest rate (how fast it gets worse), a ship-vs-pay decision for the current cycle, and a 20%-of-cycle cap to keep velocity unblocked. The artefact updates monthly and the owner signs the cap review. Replaces 'I will clean this up later' with a budget the future-self has to respect.

**Ефективно для:**

- Solo dev перевантажений refactor-bullshit-task - впровадити cap і ledger.
- Post-incident коли debt вистрілив - закласти interest rate і pay-now decision.
- Перехід з 'clean up later' на 'budgeted next cycle' - формалізувати ledger.
- Кожен sprint починається з debt-discussion - cap-by-policy вирішує суперечку.
- Stakeholders не бачать debt - signed ledger робить його видимим.

## Applies If (ALL must hold)

- Solo developer or 2-3 person team owning the codebase end-to-end.
- Team ships in iterations (sprints, releases, or milestones).
- Codebase has known debt items (code-comments, deferred refactors, known bugs).
- Owner can decide cycle allocation without external approval.

## Skip If (ANY kills it)

- Enterprise team with a dedicated tech-debt committee - use that framework.
- Pre-MVP discovery phase - debt is throwaway; ledger overhead not justified.
- Strict regulatory ship gate with no slack to allocate - debt is paid through compliance.
- Team has no debt today (greenfield + green CI for 30 days) - delay until first debt.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Debt inventory | list of items with impact + interest | engineering |
| Cycle length | sprint / release / month duration | team |
| Owner accountability | named person who signs the ledger | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[xp-extreme-programming]] | trunk-based + refactor discipline this budget formalises. |
| [[solo-self-code-review-protocol]] | review discipline that feeds debt detection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: 20%-cycle cap, named-ledger, impact + interest, ship-vs-pay, monthly review, skip-gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: inventory, score, decide, allocate, sign | ~800 |
| `content/05-examples.xml` | essential | Worked example: a 2-week cycle with 4 debt items + 20% cap | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals to a rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-items` | sonnet | Impact + interest scoring requires per-item judgement. |
| `draft-ledger` | haiku | Mechanical table fill from scored items. |
| `cycle-allocate` | sonnet | Cap discipline vs scope pressure. |
| `owner-sign` | opus | Stakes high; cap misallocation blocks roadmap. |

## Templates

| File | Purpose |
|------|---------|
| `templates/debt-ledger.md` | Markdown skeleton for the debt ledger (items + scores + decisions). |
| `templates/scoring-rubric.md` | Rubric for impact + interest scores (1-5 scale, anchored examples). |
| `templates/_smoke-test.json` | Filled-in minimum viable debt ledger for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-budget-for-solos.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[xp-extreme-programming]]
- [[solo-self-code-review-protocol]]
- [[spec-driven-debugging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree checks preconditions, then ledger presence, then scoring discipline, then 20%-cap, then sign-off. Every leaf maps to a rule id from `content/01-core-rules.xml`, with skip-this-methodology as the default for pre-MVP / enterprise contexts.
