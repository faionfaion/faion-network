# Prompt A/B Power Calculator

## Summary

**One-sentence:** Computes per-arm sample sizes and significance thresholds for weekly prompt-version A/B reviews so solo agent builders stop running under-powered tests.

**One-paragraph:** Solo prompt iterators chronically under-power their A/Bs — they ship a variant after 12 traffic samples and call the regression a "model drift". This methodology produces a `power-calc-spec.json` artefact pinning baseline rate, MDE (minimum detectable effect), alpha, target power, and computed per-arm n. Downstream A/B harness consumes the spec; the calculator refuses to run under-powered configurations.

**Ефективно для:**

- Weekly prompt-version A/B review (recurring cadence).
- Solo agent builders, що pushуть variants without power calculation.
- Малий або середній traffic — точно знати, скільки треба зібрати.
- Bridge between prompt-engineering and rag-eval-ab-testing.
- Audit trail: spec versioned + owned + reviewed.

## Applies If (ALL must hold)

- Recurring A/B review on the operating cadence.
- Baseline metric defined and measurable.
- Named accountable owner.
- Repository / wiki hosts the versioned spec.

## Skip If (ANY kills it)

- One-shot prompt change without recurrence.
- No baseline metric defined yet — block on baseline definition first.
- Fewer than 3 instances per year.
- No named owner.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Baseline rate (current variant) | float ∈ [0,1] | eval harness |
| Minimum detectable effect (MDE) | float | product target |
| Alpha (significance) | float ∈ (0,0.5) | stats policy |
| Target power | float ∈ (0.5,0.99) | stats policy |
| Traffic per day | int | analytics |
| Named accountable owner | string | ownership log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer` | parent role skill |
| `[[prompt-pr-review-checklist]]` | downstream gate |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for power-calc-spec + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 5-step: collect inputs → compute n → write spec → audit → commit | ~700 |
| `content/05-examples.xml` | essential | Worked example: baseline 0.62, MDE 0.04 → n per arm | ~600 |
| `content/06-decision-tree.xml` | essential | Routes traffic volume + MDE to feasibility | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-inputs` | haiku | Form fill. |
| `compute-n` | sonnet | Closed-form formula + sanity checks. |
| `feasibility-review` | opus | Traffic vs sample size trade-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/power-calc-spec.json` | JSON skeleton matching 02-output-contract. |
| `templates/power-calc-spec.md` | Narrative review draft. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-ab-power-calculator.py` | Validate power-calc-spec; also computes per-arm n via two-proportion z-test | Pre-commit + before A/B start |

## Related

- [[prompt-pr-review-checklist]]
- [[prompt-portability-audit]]
- [[production-trace-mining-for-training-data]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes to the calculator if baseline rate and MDE are pinned; refuses if traffic-per-day cannot reach the computed n within the review cadence. Walk it before scheduling the A/B; running an under-powered test wastes the cadence slot.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/power-calc-spec.json`

```json
{
  "artefact_id": "ab-<feature>-<period>",
  "owner": "<handle>@faion.net",
  "trigger": {
    "kind": "schedule",
    "value": "weekly: thursday"
  },
  "baseline_rate": 0.62,
  "mde": 0.04,
  "alpha": 0.05,
  "power": 0.8,
  "traffic_per_day": 1200,
  "per_arm_n": 2350,
  "inputs_used": [
    {
      "name": "baseline_eval",
      "source": "git://<repo>/eval/<file>.json"
    },
    {
      "name": "mde_target",
      "source": "git://<repo>/product/<file>.md"
    },
    {
      "name": "traffic_analytics",
      "source": "warehouse://<table>"
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
