# Product Development Trends 2026

## Summary

**One-sentence:** Snapshot specialisation of trend research locked to 2026 signals (on-device LLM, agent-as-product, vibe-coding, privacy-first, sustainability), with hard freshness cutoff (no sources older than 18 months).

**One-paragraph:** Year-locked trend snapshot built on product-development-trends, scoped to the 2026 signal set: on-device LLM inference, agent-as-product paradigm, AI-native CRMs, privacy-first shifts post-DSA, vibe-coding, sustainability badges. Enforces an 18-month source-age cap and a 2025-Q4-to-2026-Q4 retrieval window.

**Ефективно для:**

- 2026 річний планувальний цикл - треба зафіксувати поточні trends.
- Перевірка чи 2024-2025 bets ще релевантні у 2026.
- Investor narrative '2026 trend posture'.
- Pricing / packaging оновлення в світлі 2026 signals.
- Hiring 2026 - під які trends ми скейлимо.

## Applies If (ALL must hold)

- 2026 annual planning cycle; lock current trend posture.
- Re-validation of 2024-2025 bets against 2026 signals.
- Investor narrative '2026 trend posture' section.
- Pricing / packaging refresh in light of 2026 signals.
- Hiring 2026 - under which trends do we scale headcount?

## Skip If (ANY kills it)

- Non-2026 cycles (use product-development-trends instead).
- Trends with no 2026-specific divergence (use the parent methodology).
- Pre-PMF startups with no users; trend bets are noise.
- Hardware companies where 2026 signals lag.
- Internal tools.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 2026 candidate trend list | markdown | PM + research team |
| Q4 2025 retrospective | markdown | previous trend cycle |
| Source-freshness check | automated | CI / WebFetch |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[product-development-trends]] | supplies the 4-axis scoring rubric this snapshot specialises |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `freshness-gate` | haiku | Reject sources older than 18 months. |
| `score-2026-signals` | sonnet | Apply 4-axis scoring to the 2026 candidate set. |
| `verdict-2026` | opus | Bet/monitor/ignore with 2026-specific kill criteria. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trend-brief-2026.md` | 2026 trend brief skeleton with the 6 canonical 2026 trend buckets |
| `templates/collect-trends.py` | Pull 2026 source signals with freshness gate |
| `templates/score-signals.py` | Apply 4-axis scoring to 2026 candidates |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-development-trends-2026.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[product-development-trends]]
- [[trend-analysis]]
- [[competitive-intelligence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
