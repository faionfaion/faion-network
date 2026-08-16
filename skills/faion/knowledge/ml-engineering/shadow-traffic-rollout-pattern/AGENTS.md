# Shadow Traffic Rollout Pattern

## Summary

**One-sentence:** Mirrors production traffic to a candidate model/prompt in parallel (no user-facing impact), captures per-request diff vs baseline, blocks promotion until joint quality + latency + cost gates stay within named thresholds across a representative window.

**One-paragraph:** Mirrors production traffic to a candidate model/prompt in parallel (no user-facing impact), captures per-request diff vs baseline, blocks promotion until joint quality + latency + cost gates stay within named thresholds across a representative window. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Model swap (e.g. Sonnet → Opus) — потрібно перевірити divergence перед промо.
- Prompt-template зміна на критичному шляху (refunds, KYC, support).
- Latency-sensitive flows: candidate може повільніший — shadow вимірює перед rollout.
- Cost-sensitive flows: candidate може дорожчий — shadow рахує реальний bill.

## Applies If (ALL must hold)

- Production-mirror infra exists (request fan-out, no user impact).
- Judge model calibrated against ≥50 expert-labelled samples within 30 days.
- Baseline + candidate are independently identified (model id, prompt version).
- Traffic volume supports ≥500 scored requests in 48h.

## Skip If (ANY kills it)

- No production-mirror infra available — methodology can't execute.
- Candidate is config-only (region, retry policy) with no behavior delta.
- No judge calibration exists and cannot be produced.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Baseline model id + prompt version | string / semver | Repo / config |
| Candidate model id + prompt version | string / semver | Repo / config |
| Judge config (model + prompt + calibration date) | YAML | ML eng team |
| Mirror infra config | Kubernetes manifest / fan-out config | Infra team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-shadow-traffic-rollout-pattern` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shadow-traffic-rollout-pattern.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ai/ml-engineer/AGENTS.md`
- [[model-upgrade-migration-playbook]]
- [[golden-set-curation-and-maintenance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config-instance.json`

```json
{
  "candidate_id": "sonnet-4.7@2026-05-15",
  "baseline_id": "sonnet-4.6@2026-04-01",
  "window": {
    "start": "2026-05-20T00:00:00Z",
    "end": "2026-05-22T00:00:00Z",
    "n_requests": 2100,
    "coverage": [
      "weekday",
      "weekend"
    ]
  },
  "judge": {
    "model": "opus-4.6",
    "prompt_version": "judge-v3.1",
    "calibration_date": "2026-05-10"
  },
  "metrics": {
    "quality_delta": 0.04,
    "latency_delta_pct": 8.0,
    "cost_delta_pct": -3.0
  },
  "gate_result": "pass",
  "promotion_decision": "promote"
}
```
