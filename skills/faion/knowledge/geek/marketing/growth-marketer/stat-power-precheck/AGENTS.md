---
slug: stat-power-precheck
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "fcf6e7965651b195"
summary: A short pre-test power calculation that tells solopreneurs and small-team marketers whether their primary landing page has enough traffic to detect a stated lift at a stated confidence within a stated window — before they launch an A/B test.
tags: [cro, ab-testing, power-analysis, experiment-design, geek, marketing]
---
# Stat Power Pre-Check

## Summary

**One-sentence:** A required pre-flight check on every CRO experiment that converts traffic, baseline conversion, and target lift into a "can we even detect this?" verdict before the test launches.

**One-paragraph:** Solopreneurs and small-team marketers run statistically underpowered tests constantly — too-little traffic, premature stops, "winners" that are noise. This methodology blocks that. Before launching any experiment on a primary landing page, the marketer fills a five-input form (weekly visitors, baseline conversion, target relative lift, desired alpha, desired power) and reads a verdict: GO (enough traffic for stated window), STRETCH (need to extend window or accept lower power), or KILL (the effect size is uneconomic — pivot to a structural change instead). The check is qualitative-numerate: no full Bayesian rigor, just enough math to refuse to run tests that cannot conclude. Pairs with `experiment-ledger-discipline` (pro/marketing) which logs the verdict and outcome.

## Applies If (ALL must hold)

- Planning a CRO experiment on a page with conversion event tracking already wired (no test runs blind).
- Weekly traffic to the test surface is measurable and stable (±20% week over week).
- Baseline conversion rate is known for the last 4 weeks at minimum.
- Decision authority rests with the marketer (no committee approval lag eating test window).

## Skip If (ANY kills it)

- Traffic is too sparse for any reasonable test (< ~200 conversions / week at baseline) — switch to qualitative methods: 5-second tests, user interviews, scroll-depth heatmaps.
- The change is a bug fix or compliance fix that MUST ship — do not gate shipping on power.
- The change is a brand / trust signal that cannot be measured by a single conversion event — different evaluation method applies.
- The test is structurally underpowered AND cannot be redesigned (e.g. one-shot launch announcement) — accept it as a non-experiment and label accordingly in the ledger.

## Prerequisites

- Last 4 weeks of weekly visitor + conversion counts on the test surface.
- A target lift expressed as a relative percentage (e.g. "10% lift on signup rate", not "0.5 percentage points").
- An agreed maximum test window (e.g. 4 weeks); shorter than the calculated minimum → STRETCH or KILL verdict.
- Optionally: a power calculator (Evan Miller, optimizely-sample-size, or a 10-line Python script invoking `statsmodels.stats.power`).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/experiment-hypothesis-scoring` | Upstream scoring decides which hypotheses are worth power-checking at all. |
| `pro/marketing/experiment-ledger-discipline` | The ledger is where the GO / STRETCH / KILL verdict is recorded. |
| `geek/marketing/seo-manager/google-ai-overviews-optimization` | Some CRO targets are AIO-eligibility changes; the power math is the same. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: required-inputs, no-launch-without-verdict, minimum-conversions, sequential-stop guard, lift-as-relative | ~1200 |

## Related

- parent skill: `geek/marketing/growth-marketer/`
- peer methodologies: `experiment-hypothesis-scoring` (pro/marketing), `experiment-ledger-discipline` (pro/marketing), `pricing-experiment-design` (pro/product)
- external: [Evan Miller — Sample Size Calculator](https://www.evanmiller.org/ab-testing/sample-size.html) · [statsmodels power module](https://www.statsmodels.org/) · [Optimizely Stats Engine paper](https://www.optimizely.com/)
