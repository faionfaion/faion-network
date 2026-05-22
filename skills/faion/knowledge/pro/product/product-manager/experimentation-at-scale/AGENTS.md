---
slug: experimentation-at-scale
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Run 100+ experiments/year with statistical rigor.
content_id: "4e204465f81afa3d"
tags: [experimentation, a-b-testing, hypothesis-driven, data-driven-decisions, product-metrics]
---
# Experimentation at Scale

## Summary

**One-sentence:** Run 100+ experiments/year with statistical rigor.

**One-paragraph:** Run 100+ experiments/year with statistical rigor. Pre-register hypotheses, behavioral predictions, guardrail metrics, and decision rules to prevent HiPPO override and build org learning.

## Applies If (ALL must hold)

- A roadmap bet is reversible, has a clear behavioral prediction, and can be measured within 4 weeks at current traffic.
- Quarterly planning when roadmap candidates outnumber conviction — turn opinions into a ranked experiment slate.
- After discovery rounds where 2–4 candidate solutions exist for one opportunity — experiment to pick, not to launch.
- A guardrail-only "do-no-harm" rollout: PM wants to ship a refactor or migration and needs proof it didn't regress conversion/retention.
- A pricing or packaging change where finance wants quantified lift before commit (with legal sign-off on bait-pricing rules).
- Stakeholder disputes (design vs. eng vs. growth) where pre-registering a metric and accepting the verdict is faster than politics.
- Planning org experimentation infrastructure: choosing tooling (GrowthBook vs. Statsig vs. Eppo), governance, and statistical standards.
- Onboarding a new PM into an experiment-mature org — agentized hypothesis review tightens the loop fast.

## Skip If (ANY kills it)

- Strategic, irreversible bets (rebrand, repositioning, contract terms) — A/B will under-power on the metrics that matter and over-emphasize short-term proxies. Use evidence triangulation instead.
- Pre-PMF (less than 1k WAU): the PM should be doing problem interviews, not optimizing CTAs. A null result here means "no signal," not "no effect."
- Innovation-tier features where the audience needs greater than 30 days to learn the new behavior — novelty/primacy will dominate the readout.
- Internal tooling, B2B with fewer than 50 accounts, or one-off launches (regulatory, marketing event). Use cohort/case-study analysis.
- When the PM cannot articulate a falsifiable behavioral prediction with a numeric MDE — that is a discovery gap, not an experiment gap. Run a fake-door, prototype test, or interview round first.
- Surfaces under compliance review (HIPAA, PCI, KYC) where any variant requires legal sign-off — gating loop is slower than the agentic experiment author; default to risk-controlled rollout, not A/B.
- When success can only be measured greater than 1 quarter out (LTV, retention beyond available holdout) — switch to switchback or holdout-cohort analysis with explicit stakeholder agreement.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/product/product-manager/`
