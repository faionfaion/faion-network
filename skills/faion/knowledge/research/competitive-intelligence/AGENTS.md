# Competitive Intelligence

## Summary

**One-sentence:** Continuous CI pipeline that splits mechanical collection (Haiku) from strategic synthesis (Opus); produces dated weekly digests, monthly threat assessments, and battlecards with a hard 14-day TTL.

**One-paragraph:** Point-in-time competitor snapshots go stale within weeks. This methodology builds a continuous CI pipeline where six subagents split mechanical collection (Haiku) from strategic synthesis (Opus), publish weekly digests, monthly threat assessments, and battlecards with a hard 14-day TTL. Every claim must cite a fetched URL, every URL passes a fact-checker HEAD request before distribution.

**Ефективно для:**

- Live B2B/SaaS ринок, де конкуренти шиплять щотижня та змінюють pricing.
- Sales team потребує свіжих battlecards (deal cycle > 30 днів робить stale-дані видимими).
- Roadmap-рішення заблоковані на feature parity або диференціації.
- Funding / M&A / executive-hire сигнали мають з'являтись у вікні 24h.
- Вже маєте 3+ названих direct competitors з стабільними URL для моніторингу.

## Applies If (ALL must hold)

- Live B2B/SaaS market where competitors ship weekly and pricing changes often.
- Sales team needs current battlecards; deal cycle > 30 days exposes stale data fast.
- Product roadmap decisions are blocked on feature parity or differentiation gaps.
- Funding, M&A, or executive-hire signals must surface within 24 hours.
- You already have 3+ named direct competitors with stable URLs to track.

## Skip If (ANY kills it)

- Pre-PMF or category-creation phase — competitors are not the bottleneck.
- Fewer than 5 known competitors — a manual quarterly snapshot beats infrastructure overhead.
- Highly regulated or closed markets (defense, sealed bids) where public signals are noise.
- Personal projects with no GTM motion — output has no consumer.
- When the team will not act on alerts — CI without an action loop is theater.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Watchlist | YAML (competitor, URLs, signal types) | GTM team + sales |
| Positioning doc | markdown | marketing |
| Win/loss interview notes | markdown / transcripts | sales ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[competitor-analysis]] | supplies the seed competitor list and positioning baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 7-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ci-collector` | haiku | Mechanical polling of YAML watchlist. |
| `ci-classifier` | haiku | Tag events by signal type; near-deterministic. |
| `ci-synthesizer` | sonnet | Weekly digest writing with cited sources. |
| `ci-threat-analyst` | opus | Strategic threat scoring + scenario planning. |
| `ci-battlecard-writer` | sonnet | Per-competitor battlecard regeneration. |
| `ci-fact-checker` | sonnet | Adversarial pass: every claim cites a HEAD-validated URL. |

## Templates

| File | Purpose |
|------|---------|
| `templates/watchlist.yaml` | Input config: competitor + URLs + signal types |
| `templates/ci-collector.py` | Minimal collector: fetches watchlist URLs and emits NDJSON delta events |
| `templates/battlecard.md` | Per-competitor battlecard skeleton with 14-day TTL stamp |
| `templates/weekly-digest.md` | Weekly digest skeleton with event-id provenance |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-competitive-intelligence.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[competitor-analysis]]
- [[trend-analysis]]
- [[continuous-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
