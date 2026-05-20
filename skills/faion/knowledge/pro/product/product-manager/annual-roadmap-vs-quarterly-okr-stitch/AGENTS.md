---
slug: annual-roadmap-vs-quarterly-okr-stitch
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "249f9cedbd952ef9"
summary: An explicit stitching methodology that decomposes annual product bets into quarterly OKR cascades so the year's bet and the quarter's KRs stay coupled across all four quarters.
tags: [product, roadmap, okr, planning, quarterly, pro]
---
# Annual Roadmap → Quarterly OKR Stitch

## Summary

**One-sentence:** An explicit stitching methodology that turns each annual product bet into a four-quarter OKR cascade with documented bet → objective → key-result lineage, preventing the common "Q3 OKRs don't reference the annual bet" drift.

**One-paragraph:** Annual product strategy and quarterly OKRs are usually planned in different rooms with different vocabularies; by Q3 the OKRs are about whatever crisis recurred, and the annual bet exists only in the strategy doc. This methodology defines the stitch: for each annual bet, the PM authors a `bet-to-okr-cascade.yaml` that lists 1-3 objectives spanning the year, 4 quarter-keyed KR sets that each carry the bet's identifier, and a per-quarter validation step that confirms the new quarter's OKRs still trace to the annual bet. Output: a per-quarter stitching review in the planning meeting where missing links are surfaced and either fixed or the bet is explicitly retired with rationale.

## Applies If (ALL must hold)

- Organisation does annual strategy AND quarterly OKR planning.
- A product manager owns the bet-to-OKR linkage at least at the team level.
- Annual bets are documented (strategy doc, board memo, roadmap file).
- Quarterly OKR review is a recurring meeting (not skipped).

## Skip If (ANY kills it)

- Organisation does only quarterly OKRs (no annual bets) — different methodology.
- Organisation does only annual planning (no quarterlies) — overhead exceeds the win.
- Annual bets are confidential / unwritten — stitch impossible without a written bet.
- Team is in mid-strategy shift (acquisition, pivot) — defer until shape settles.

## Prerequisites

- Annual bets enumerated in a roadmap doc or `annual-bets.yaml`.
- A quarterly OKR template (own / borrowed from `okr-fundamentals`).
- A quarterly planning meeting on the calendar.
- A small group (PM + lead + design or eng peer) that can co-author the cascade.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager/okr-fundamentals` (or equivalent) | OKR canonical shape; stitch sits on top. |
| `pro/product/product-manager/annual-product-strategy-refresh` | Annual bets emerge from this; stitch consumes them. |
| `pro/product/product-manager/quarter-planning-okr-cascade` | Quarterly planning ritual; stitch is a co-input. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bet has a bet_id, every KR has a bet_id reference, quarterly stitch review, explicit retire-vs-extend, KR count cap | ~1100 |
| `content/02-output-contract.xml` | essential | bet-to-okr-cascade schema, quarterly review log shape | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: orphan KRs, vanity KRs, bet-amnesia | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bet-decompose-to-objectives` | opus | Cross-input synthesis from the annual strategy doc |
| `quarter-kr-draft` | sonnet | Bounded judgement: which KRs advance the bet this quarter |
| `coupling-audit` | sonnet | Per-KR check: does the KR reference the bet_id with rationale |
| `retire-vs-extend-decision` | opus | Cross-quarter synthesis; high-stakes call |

## Templates

| File | Purpose |
|------|---------|
| `templates/bet-to-okr-cascade.yaml` | Per-bet annual cascade across 4 quarters |
| `templates/quarter-review.md` | Markdown template for the quarterly stitch review |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/coupling-audit.py` | Read OKR list; assert every KR has a bet_id and the bet exists | Pre-quarterly planning |
| `scripts/cascade-render.py` | Emit a one-page roadmap-to-OKR visualisation | Quarterly all-hands |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodologies: `okr-fundamentals`, `annual-product-strategy-refresh`, `quarter-planning-okr-cascade`
- external: [Measure What Matters (Doerr)](https://www.whatmatters.com/) · [Christina Wodtke "Radical Focus"](https://eleganthack.com/) · [Lenny Rachitsky on OKRs](https://www.lennysnewsletter.com/)
