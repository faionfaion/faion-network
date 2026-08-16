# Eval Set Stratified Sampling Recipe

## Summary

**One-sentence:** Produces a stratified sampling recipe (per-cohort × per-tool × per-intent quotas) for daily LLM eval-set drift checks so the slice is representative without paying full-eval cost.

**One-paragraph:** Daily drift checks cannot run the full eval set — too slow, too expensive. A naive random subsample misses tails (low-volume intents, new cohorts, rare tools). This methodology produces a written sampling recipe: declared strata (cohort × tool × intent × difficulty), per-stratum quota (proportional-with-floor, never raw-proportional), seed-locked sampler, fixed daily N, and a drift comparator that triggers re-sample only when the prod traffic distribution shifts >10%. Output is a `sampling-recipe.json` that the eval harness reads each morning.

**Ефективно для:** daily eval-suite triage, p7-llm-agent-developer drift monitoring, ML-ops on-call who needs a fixed-cost slice that still covers the long tail, teams whose eval bill 10x'd after they added cohorts.

## Applies If (ALL must hold)

- Production LLM workload has ≥3 named cohorts, tools, or intents.
- A full eval set ≥500 cases exists and is too expensive to run daily.
- Traffic distribution per stratum is known (analytics or trace logs).
- A daily slice budget (cases-per-day or $/day) is fixed.

## Skip If (ANY kills it)

- Full eval set ≤500 cases — run it whole, sampling adds noise without saving money.
- No traffic distribution data — fix observability before designing strata.
- Single cohort/intent — random subsample is equivalent, no stratification needed.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval set manifest | JSONL with `cohort`, `tool`, `intent`, `difficulty` fields | eval repo |
| Production traffic distribution | CSV `stratum,count_30d,share_pct` | analytics warehouse |
| Daily slice budget | int (cases/day) or float ($/day with $/case rate) | finops / on-call lead |
| Prior recipe (if exists) | `sampling-recipe.json` | eval repo `eval/` dir |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[llm-drift-daily-triage]]` | Consumer of the daily slice; recipe must match its cadence. |
| `geek/ai/llm-integration/AGENTS.md` | Parent group vocabulary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: proportional-with-floor, seed lock, drift trigger, stratum max-share cap, tail-floor 5 cases, recipe versioning | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for `sampling-recipe.json` + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: head-only sample, no floor, unchanged recipe under drift, no seed | ~600 |
| `content/04-procedure.xml` | recommended | 6 steps: enumerate strata → fetch traffic → set N → apply proportional+floor → seed → diff vs prior | ~700 |
| `content/05-examples.xml` | recommended | One full worked recipe for a 4-cohort × 3-tool agent | ~600 |
| `content/06-decision-tree.xml` | essential | Apply-or-skip + recipe-shape branches | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Enumerate strata from manifest | haiku | Mechanical group-by. |
| Compute per-stratum quotas | sonnet | Arithmetic + floor/cap judgment. |
| Diff vs prior recipe + decide refresh | sonnet | Bounded comparison. |
| Recipe rationale write-up | opus | Synthesis for human reviewer. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sampling-recipe.schema.json` | JSON Schema for the recipe artefact. |
| `templates/sampling-recipe.example.json` | Reference filled recipe for a 4×3×2 grid. |
| `templates/strata-quota.py` | Proportional-with-floor quota calculator. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-eval-set-stratified-sampling-recipe.py` | Validate a recipe JSON against the schema + rule checks. | After recipe write, before eval harness consumes. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[llm-drift-daily-triage]]` — downstream consumer
- `[[judge-calibration-protocol]]` — orthogonal eval-quality lever

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: eval-set size ≥500, multi-stratum, traffic data available, then chooses between fresh-recipe or carry-forward branches based on traffic drift vs prior recipe.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/sampling-recipe.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/eval-sampling-recipe",
  "title": "Stratified eval sampling recipe",
  "type": "object",
  "required": [
    "version",
    "parent_version",
    "created_at",
    "N_daily",
    "seed",
    "tail_floor",
    "head_cap_share",
    "strata",
    "drift_policy"
  ],
  "additionalProperties": false,
  "properties": {
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "parent_version": {
      "type": [
        "string",
        "null"
      ]
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "N_daily": {
      "type": "integer",
      "minimum": 10,
      "maximum": 5000
    },
    "seed": {
      "type": "integer"
    },
    "tail_floor": {
      "type": "integer",
      "minimum": 1,
      "maximum": 50,
      "default": 5
    },
    "head_cap_share": {
      "type": "number",
      "minimum": 0.1,
      "maximum": 0.6,
      "default": 0.4
    },
    "drift_policy": {
      "type": "object",
      "required": [
        "abs_share_threshold",
        "max_age_days"
      ],
      "additionalProperties": false,
      "properties": {
        "abs_share_threshold": {
          "type": "number",
          "minimum": 0.01,
          "maximum": 0.5
        },
        "max_age_days": {
          "type": "integer",
          "minimum": 1,
          "maximum": 90
        }
      }
    },
    "strata": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": [
          "key",
          "traffic_share",
          "quota"
        ],
        "additionalProperties": false,
        "properties": {
          "key": {
            "type": "string",
            "pattern": "^[a-z0-9._=-]+$"
          },
          "traffic_share": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "quota": {
            "type": "integer",
            "minimum": 1
          }
        }
      }
    }
  }
}
```

### `templates/sampling-recipe.example.json`

```json
{
  "version": "1.2.0",
  "parent_version": "1.1.0",
  "created_at": "2026-05-22T07:00:00Z",
  "N_daily": 200,
  "seed": 42,
  "tail_floor": 5,
  "head_cap_share": 0.4,
  "drift_policy": {
    "abs_share_threshold": 0.1,
    "max_age_days": 30
  },
  "strata": [
    {
      "key": "cohort=ent.tool=search.intent=lookup",
      "traffic_share": 0.55,
      "quota": 80
    },
    {
      "key": "cohort=ent.tool=summarise.intent=long-form",
      "traffic_share": 0.2,
      "quota": 50
    },
    {
      "key": "cohort=smb.tool=search.intent=lookup",
      "traffic_share": 0.15,
      "quota": 40
    },
    {
      "key": "cohort=trial.tool=search.intent=lookup",
      "traffic_share": 0.1,
      "quota": 30
    }
  ]
}
```

### `templates/strata-quota.py`

```python
"""Proportional-with-floor quota calculator for stratified eval sampling."""
from __future__ import annotations


def compute_quotas(
    strata: list[tuple[str, float]],
    n_daily: int,
    tail_floor: int = 5,
    head_cap_share: float = 0.4,
) -> list[tuple[str, int]]:
    if not strata or n_daily < 1:
        return []
    head_cap = int(n_daily * head_cap_share)
    raw = [(k, max(tail_floor, min(head_cap, round(n_daily * s)))) for k, s in strata]
    total = sum(q for _, q in raw)
    delta = n_daily - total
    if delta == 0:
        return raw
    # Redistribute to tail strata (sorted by share asc) one case at a time.
    order = sorted(range(len(raw)), key=lambda i: strata[i][1])
    out = [list(t) for t in raw]
    i = 0
    step = 1 if delta > 0 else -1
    while delta != 0 and order:
        idx = order[i % len(order)]
        new_q = out[idx][1] + step
        # Respect bounds.
        if new_q >= tail_floor and new_q <= head_cap:
            out[idx][1] = new_q
            delta -= step
        i += 1
        if i > len(order) * (abs(delta) + 10):
            break
    return [(k, q) for k, q in out]


if __name__ == "__main__":
    demo = [("head", 0.55), ("mid", 0.20), ("smb", 0.15), ("trial", 0.10)]
    for k, q in compute_quotas(demo, n_daily=200):
        # Documented stdout for demo only.
        import sys
        sys.stdout.write(f"{k}\t{q}\n")
```
