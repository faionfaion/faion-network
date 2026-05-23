# Lookalike and Retargeting Audience Design

## Summary

**One-sentence:** Designs seed-audience policy, exclusion logic, lookalike degree, overlap audit, and frequency caps for post-iOS17 paid ads — the audience moat replacing creative-only optimization.

**One-paragraph:** Post-2024 cookie deprecation and iOS17 mail-privacy collapse, paid-ads audience design is the durable moat. This methodology covers seed-audience selection (purchase events / high-LTV cohorts / engaged-90-day), exclusion stacks (existing customers / opt-outs / low-fit segments), lookalike degree per platform (Meta 1-3% / Google similar-audiences / LinkedIn matched-audiences), monthly audience-overlap audit, and frequency-cap discipline (>=8 impressions/week is wasteful). Output: audience design spec covering all five layers.

**Ефективно для:**

- Marketing owner з >=$1k/mo Meta + Google spend, який втратив creative moat post-iOS17.
- Перебудова стратегії: 'creative-led → audience-led' з seed + exclusion + lookalike layers.
- Audit-only режим: знайти overlap між кампаніями, який убиває ROAS.
- Pre-launch audience spec для нового продукту з існуючою CRM-базою.

## Applies If (ALL must hold)

- Active paid-ads spend >= $1k/month across Meta or Google.
- First-party data available (CRM, purchases, events, email engagement).
- Marketing owner has platform-level access (Meta Business Manager, Google Ads).
- Operator can run monthly overlap audit (Meta Audience Insights or BigQuery).

## Skip If (ANY kills it)

- Spend < $500/month — broad targeting outperforms layered audiences below this threshold.
- No first-party data — no seed = no lookalike; collect events first.
- Single-platform spend with < 3 campaigns — overhead exceeds value.

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
| `content/03-failure-modes.xml` | essential | >=4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-lookalike-and-retargeting-audience-design` | opus | Synthesis under output contract; final write-up. |
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
| `scripts/validate-lookalike-and-retargeting-audience-design.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
