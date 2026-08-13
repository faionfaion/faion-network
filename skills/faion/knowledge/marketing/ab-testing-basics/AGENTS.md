# A/B Testing Basics

## Summary

**One-sentence:** Controlled experiment fundamentals — 50/50 split, pre-registered primary metric, MDE-driven sample size, no peeking, verdict-card close — produces a defensible result card.

**One-paragraph:** A/B testing is a controlled experiment that compares two versions by splitting traffic 50/50, measuring which variant performs better on a pre-registered primary metric, and deciding based on statistical significance. This methodology pins the discipline: pre-registration (hypothesis + primary + secondary + MDE + sample-size + stop date written before test starts); no-peeking (no decision before pre-registered close); SRM check (sample-ratio mismatch &gt;5% invalidates the test); secondary-metrics declared up front (post-hoc additions forbidden); close-with-verdict (5-verdict vocabulary).

**Ефективно для:**

- First A/B test — establishes discipline.
- Solo growth marketer — pre-reg + close discipline.
- Agency client — shared method language.
- Post-mortem of failed tests — locate the rule violated.

## Applies If (ALL must hold)

- Product or page with ≥1k weekly events on the target metric.
- Experimentation platform (PostHog, Statsig, Optimizely, GrowthBook, GA).
- Authority to define + ship variants.
- Owner who will write the pre-registration.

## Skip If (ANY kills it)

- Traffic too low for MDE (test will be inconclusive).
- Multi-arm sequence (use multi-armed-bandit instead).
- Pure brand campaign with no quantifiable metric.
- One-shot transaction with no follow-on data.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Baseline metric value (30d) | dashboard | analytics |
| Minimum detectable effect (MDE) target | spec | growth team |
| Sample-size calculator | tool | stats library |
| Variant designs | files / Figma | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[experiment-hypothesis-scoring]] | Upstream — produces the queued hypothesis. |
| [[experiment-verdict-template]] | Downstream — closes the test. |
| [[experiment-ledger-discipline]] | Persistent storage of the test. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pre-registration-required, fifty-fifty-split-or-justify, no-peeking, srm-check-on-close, secondary-metrics-pre-registered | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-sample-size` | haiku | Formula application. |
| `draft-pre-reg` | sonnet | Bounded judgment on hypothesis + secondary choice. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pre-registration.json` | JSON example of a pre-registration |
| `templates/pre-registration.md` | Pre-registration markdown template |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing-basics.py` | Validate one spec JSON against the schema | After draft, before publish |

## Related

- [[experiment-hypothesis-scoring]]
- [[experiment-verdict-template]]
- [[experiment-ledger-discipline]]
- [[aarrr-pirate-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pre-registration.json`

```json
{
  "test_id": "EXP-2026-031",
  "hypothesis": "Shortening the hero copy increases primary CTA CTR for cold pricing traffic.",
  "primary_metric": {
    "name": "cta_ctr",
    "baseline": 0.062
  },
  "secondary_metrics": [
    {
      "name": "signup_cr"
    },
    {
      "name": "d7_retention"
    }
  ],
  "mde": 0.05,
  "sample_size": 12400,
  "split": {
    "control": 0.5,
    "treatment": 0.5
  },
  "starts_at": "2026-05-06",
  "closes_at": "2026-05-20",
  "owner": "@ruslan"
}
```
