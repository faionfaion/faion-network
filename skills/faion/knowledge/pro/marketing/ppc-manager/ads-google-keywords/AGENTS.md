---
slug: ads-google-keywords
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Designs keyword strategy by intent (informational / commercial / transactional), match-type stacks (exact + phrase + negatives), ad-group structure, and STR mining cadence.
content_id: "9c535496b66fc07f"
complexity: medium
produces: spec
est_tokens: 5300
tags: ["marketing", "google-ads", "keywords", "search", "intent", "ppc", "pro"]
---
# Google Ads Keyword Strategy

## Summary

**One-sentence:** Designs keyword strategy by intent (informational / commercial / transactional), match-type stacks (exact + phrase + negatives), ad-group structure, and STR mining cadence.

**One-paragraph:** Broad-match-only keyword strategies waste 30-60% of spend on irrelevant clicks; over-narrow exact-only strategies miss long-tail opportunities. This methodology specifies intent-first keyword research, match-type stacking (exact + phrase + tight negatives), ad-group structure (one intent per group, <=20 keywords/group), and weekly Search Terms Report (STR) mining to extract new negatives + theme expansions. Output: keyword strategy spec + match-type assignments + negative-list seed.

**Ефективно для:**

- PPC manager що builds new search campaign і вибирає match-type stack.
- Cleanup існуючого account з >100 keywords per group і broad-match leak.
- Weekly STR mining cadence для extract negatives + new theme expansions.
- Migration broad-only → phrase + exact + tight negatives.

## Applies If (ALL must hold)

- New search campaign requiring keyword research + ad-group structure.
- Existing campaign with >=100 keywords per group needing reorganization.
- Migration from broad-only to phrase + exact + negatives.
- Weekly STR mining cadence to extract negatives + themes.

## Skip If (ANY kills it)

- Brand-only campaign (just brand exact) — overhead exceeds value.
- Performance Max account — keywords managed differently (themes + audience signals).
- Spend < $500/mo — broad-match auto-bidding may outperform structured strategy.

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
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-google-keywords` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md` | Minimum viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-google-keywords.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
