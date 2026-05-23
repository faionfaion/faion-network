# Niche Positioning for Solo Dev

## Summary

**One-sentence:** Picks a (vertical x stack x outcome) positioning lane for a solo dev so marketing copy, lead magnets, and pricing collapse to one sharp story.

**One-paragraph:** Solo devs lose 6-18 months trying to market 'full-stack web development' before realizing generic positioning attracts low-fit leads. This methodology forces a three-axis decision: vertical (which industry), stack (which tools), outcome (which result the buyer cares about). Output: positioning decision record with named lane, headline copy, three test prospects, and exit criteria (when to repivot).

**Ефективно для:**

- Solo dev або 1-2 person consultancy шукає sharper market fit.
- Перехід з 'full-stack dev' на 'Stripe integration для Shopify Plus stores'.
- Збір data з останніх 10 проектів для пошуку (vertical x stack x outcome) паттерну.
- 6-month positioning trial з clear exit criteria.

## Applies If (ALL must hold)

- Solo dev or 1-2 person consultancy seeking sharper market fit.
- >= 3 months of prior project history to mine for vertical / stack / outcome patterns.
- Operator willing to say 'no' to non-fit projects for 6 months.
- Buyer ICP can be named at company-size + role + decision-trigger level.

## Skip If (ANY kills it)

- Operator < 3 months in business — too early; mine more data first.
- Operator already has named lane and 80%+ projects fit — skip to next iteration.
- Operator unwilling to refuse non-fit work — positioning will fail under economic pressure.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-niche-positioning-for-solo-dev` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Markdown decision record skeleton |
| `templates/_smoke-test.md` | Minimum viable filled decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-niche-positioning-for-solo-dev.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
