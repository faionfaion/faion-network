---
slug: adr-reversibility-tagging
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "937b67e192c6bf76"
summary: Tags every ADR with one-way-door vs. two-way-door reversibility so review depth and approval gates match the cost of being wrong.
tags: [adr, reversibility, one-way-door, decision-making, architecture, bezos]
---
# ADR Reversibility Tagging

## Summary

**One-sentence:** Tags every ADR with one-way-door vs. two-way-door reversibility so review depth and approval gates match the cost of being wrong.

**One-paragraph:** Existing ADR methodology covers structure (context / decision / consequences) but not the dimension Bezos called the most important in decision-making: is this reversible? Mechanism: every ADR carries a `reversibility` frontmatter field with one of four values — `two_way_door` (cheap to undo, &lt; 1 day rollback), `partial_two_way` (medium, &lt; 1 week with refactor), `one_way_door_costly` (multi-week rollback, contractual / data-migration), `one_way_door_irrevocable` (cannot be undone — vendor lock, public commitment, deleted data). Reversibility drives approval depth: two-way-door = solo decision, one-way-door = founder/architect sign-off + a "what would make us reverse this" pre-mortem. Primary output: a `reversibility:` field on every ADR + review-gate routing.

## Applies If (ALL must hold)

- you use ADRs (MADR, Nygard, or similar lightweight format)
- multiple people contribute architecture decisions, OR you author ≥ 5 ADRs per quarter
- decisions vary in cost-of-reversal (some easy, some hard) — relevant to most teams
- you have a code review process where ADRs can carry tags

## Skip If (ANY kills it)

- no ADRs in use yet — start with `architecture-decision-records` first
- single-developer pet project with no audit trail need — overkill
- regulatory environment requires all decisions to go through full board review — tagging adds no signal
- ADRs are pure documentation (not decision-gates) — tag has nowhere to plug in

## Prerequisites (must be true before starting)

- ADR format with frontmatter or a metadata table at the top
- agreed mapping from reversibility tier to approval requirement (solo / lead / founder)
- a definition of "rollback cost" for your context (hours of work + dollars + customer impact)
- example ADRs at each tier for calibration

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Provides the base ADR format this tag extends |
| `pro/dev/software-architect/adr-staleness-audit` | Counterpart: staleness audit uses reversibility to prioritize re-review |
| `geek/sdlc-ai/kb-adr-decay-detector-agent` | Decay detector weights one-way-door violations higher |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 4-tier taxonomy, reversibility-drives-approval, pre-mortem on one-way, evidence required, default-to-two-way on missing tag | ~900 |
| `content/02-output-contract.xml` | essential | ADR frontmatter schema, review-gate routing schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes (over-tagging as one-way, under-tagging vendor lock-in, missing pre-mortem, gate bypass, reversibility staleness) | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tag_reversibility_per_adr` | sonnet | Bounded classification, 4-way enum |
| `pre_mortem_synthesis` | sonnet | Generate "what would cause us to reverse" list |
| `cross_adr_reversibility_audit` | opus | Spot patterns (10 vendor-lock decisions tagged two-way) |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-with-reversibility.md` | ADR template with reversibility frontmatter populated |
| `templates/reversibility-decision-tree.md` | Flowchart: how to pick the tier |
| `templates/pre-mortem.md` | Pre-mortem template for one-way decisions |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/tag-reversibility-batch.py` | Suggest reversibility tier for ADRs missing the field | Backfill / monthly |
| `scripts/validate-reversibility-frontmatter.py` | Lint: every ADR has reversibility field with valid value | CI pre-merge |

## Related

- parent skill: `solo/dev/software-architect/`
- peer methodologies: `architecture-decision-records`, `adr-staleness-audit`, `decision-tree-architecture-style`
- external: [Bezos 1997 Shareholder Letter - Type 1 vs Type 2 decisions](https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm) · [Michael Nygard - ADR](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · [MADR](https://adr.github.io/madr/)
