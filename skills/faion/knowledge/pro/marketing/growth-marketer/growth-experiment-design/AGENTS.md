---
slug: growth-experiment-design
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: An end-to-end pipeline for designing growth experiments — hypothesis → ICE score → control → instrumentation → write-up — distinct from the statistical mechanics of A/B testing.
content_id: "193022fddfe97f68"
tags: [growth, experiments, ice, hypothesis, ab-test, instrumentation, controls]
---
# Growth Experiment Design

## Summary

**One-sentence:** An end-to-end pipeline for designing growth experiments — hypothesis → ICE score → control → instrumentation → write-up — distinct from the statistical mechanics of A/B testing.

**One-paragraph:** Growth teams ship "experiments without controls" — feature drops described as tests, retro-fitted with metrics, and declared wins post-hoc. This methodology forces a pre-mortem-grade design pass before the experiment runs: a hypothesis written in "If we do X for Y users, metric Z will change by W percent" form, an ICE (Impact / Confidence / Ease) score with documented assumptions, a control group defined BEFORE rollout, instrumentation verified with a synthetic event playback, a sample-size calculation tied to MDE (minimum detectable effect), and a write-up template the team commits to before the experiment ships. Primary output: a one-page experiment doc that survives a pre-flight review with the analytics owner.

## Applies If (ALL must hold)

- team runs ≥ 2 growth experiments per quarter
- product has ≥ 5,000 monthly active users (sample-size threshold)
- analytics infrastructure can split traffic and tag events
- experiment surface is not regulated (no FDA / medical / financial-disclosure constraints)
- team has named an experiment owner with veto authority over ship-without-control rollouts

## Skip If (ANY kills it)

- &lt; 1,000 weekly active users — qualitative tests beat statistical ones
- experiment is a one-way change (e.g., breaking schema, regulatory update) — no A/B possible
- "experiment" is actually a feature launch with retro-fit metrics — clarify intent first
- pure UI polish with no measurable outcome metric — use design review, not an experiment

## Prerequisites (must be true before starting)

- product has tracked north-star metric AND ≥ 1 actionable funnel metric
- experiment platform (Optimizely, GrowthBook, Statsig, in-house) configured and tested
- baseline metric stats (mean, variance, sample-per-day) from last 30 days
- experiment owner identified
- analytics owner available for pre-flight review

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/ab-testing-basics` | Statistical mechanics — sample size, p-values, sequential testing |
| `pro/marketing/growth-marketer/north-star-metric` | Defines the outcome metric the experiment targets |
| `pro/product/product-manager/experimentation-at-scale` | Process at organization level |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: hypothesis format, ICE before build, pre-defined control, instrumentation playback, MDE-tied sample | ~1000 |
| `content/02-output-contract.xml` | essential | One-page experiment doc schema, required fields, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (retrofit metrics, novelty effect, segment cherry-pick, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `hypothesis_format_validator` | haiku | Pattern check on "If we do X for Y users…" format |
| `ice_scoring_assistant` | sonnet | Score impact/confidence/ease with documented assumptions |
| `mde_sample_size_compute` | haiku | Pure arithmetic |
| `instrumentation_playback_synth` | sonnet | Generate synthetic events to verify pipeline |
| `experiment_writeup_draft` | sonnet | Convert results into committed template format |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment-one-pager.md` | One-page doc template (hypothesis through write-up) |
| `templates/ice-scoring-rubric.md` | Defined scale for Impact / Confidence / Ease |
| `templates/instrumentation-playback.json` | Synthetic event payloads for pipeline verification |
| `templates/experiment-writeup.md` | Post-experiment template committed before launch |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/mde-calculator.py` | Compute MDE / sample size from baseline stats | Design phase |
| `scripts/srm-check.py` | Sample-ratio-mismatch sanity check | Day 1 of experiment |
| `scripts/instrumentation-validator.py` | Replay synth events, verify funnel tags | Pre-launch |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodologies: `ab-testing-basics`, `north-star-metric`, `growth-loops`
- external: [GrowthBook docs](https://docs.growthbook.io/) · [Trustworthy Online Controlled Experiments (Kohavi)](https://experimentguide.com/)
