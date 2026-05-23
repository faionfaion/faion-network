---
slug: distribution-channel-research
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Bullseye-style channel evaluation: shortlist 3 of 19 channels, run small-budget tests (<=$500 each), score on CAC + reach + time-to-signal, lock the top 1-2 channels with stop-loss tripwires.
content_id: "7fd83cacf0ed982a"
complexity: medium
produces: report
est_tokens: 5200
tags: [distribution, channels, bullseye, growth, cac]
---
# Distribution Channel Research

## Summary

**One-sentence:** Bullseye-style channel evaluation: shortlist 3 of 19 channels, run small-budget tests (<=$500 each), score on CAC + reach + time-to-signal, lock the top 1-2 channels with stop-loss tripwires.

**One-paragraph:** Methodology to evaluate distribution channels (Traction's 19 + AI-era variants) without spreading budget thin. Shortlist 3 channels with the highest fit signal, run bounded small-budget tests (<=$500 each), score each on CAC + reach + time-to-signal + retention-of-channel-customers, and lock the top 1-2 with explicit stop-loss tripwires. Output: channel-report.md with the picked channels + tripwires + test results.

**Ефективно для:**

- Pre-launch або post-PMF: треба обрати 1-2 канали з 19 кандидатів без розпорошення бюджету.
- Бюджет на тестування <= $5k загалом; на канал <= $500.
- Сегмент ICP стабільний (не міняється кожного тижня).
- Маркетинговий найм або agency selection - треба обґрунтувати канал чисельно.
- Channel fatigue: один канал давав CAC, тепер CAC виріс 3x - треба перетестувати.

## Applies If (ALL must hold)

- Pre-launch or post-PMF: must select 1-2 channels from 19 candidates without budget spread.
- Test budget <= $5k total, <=$500 per channel.
- Stable ICP segment (does not change weekly).
- Marketing hire or agency selection requires a numeric channel justification.
- Channel fatigue: one channel that delivered CAC X now delivers 3x; retest needed.

## Skip If (ANY kills it)

- Pre-MVP with no product to attribute conversion to.
- Single channel mandated by the platform (e.g., Shopify App Store).
- Regulated industry where most channels are off-limits.
- Pure organic / word-of-mouth strategy that does not pay for acquisition.
- Investor-driven 'spend the round in 90 days' mandate - run a different playbook.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Persona doc | markdown | persona-building output |
| ARPU + payback target | CSV | business-model-research output |
| Test budget cap | decimal USD | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[persona-building]] | supplies the ICP that filters channel fit signals |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `channel-shortlist` | sonnet | Score 19 channels against persona + product shape. |
| `test-design` | sonnet | Design <=$500 test per channel with explicit stop-loss. |
| `results-score` | haiku | Mechanical CAC + reach + time-to-signal calculation. |
| `verdict` | sonnet | Pick top 1-2 with tripwires. |

## Templates

| File | Purpose |
|------|---------|
| `templates/channels.yaml` | Channel catalog with fit signals and tooling notes |
| `templates/channel-fit-scorer.py` | Score each channel on fit + cost + speed + measurability |
| `templates/channel-report.md` | Channel-evaluation report skeleton: shortlist + tests + tripwires |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-distribution-channel-research.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[business-model-research]]
- [[persona-building]]
- [[market-research-tam-sam-som]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
