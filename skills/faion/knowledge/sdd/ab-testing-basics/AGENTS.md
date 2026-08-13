# A/B Testing Basics

## Summary

**One-sentence:** Defines an A/B experiment up-front: hypothesis, variants, primary metric, target sample size; deterministic hash-bucketing on (experiment_id+user_id) for stable assignment.

**One-paragraph:** Defines an A/B experiment up-front: hypothesis, variants, primary metric, target sample size; deterministic hash-bucketing on (experiment_id+user_id) for stable assignment. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Testing a UI/UX change (button text, layout, checkout flow) before full rollout.
- Evaluating an algorithm improvement (ranking, recommendation) with a quantitative success metric.
- Stakeholders accept a 1–4 week test horizon before shipping the winning variant.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Testing a UI/UX change (button text, layout, checkout flow) before full rollout.
- Evaluating an algorithm improvement (ranking, recommendation) with a quantitative success metric.
- Stakeholders accept a 1–4 week test horizon before shipping the winning variant.

## Skip If (ANY kills it)

- No clear primary metric or no instrumentation to measure it — instrument first.
- Sample size too small to reach 95% power on the expected effect — pick a higher-traffic surface.
- Change is a bug fix or accessibility fix that must ship regardless of metric movement.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experiment hypothesis | 1-sentence write-up | PM |
| Primary metric definition | metric name + numerator/denominator | analytics |
| Baseline rate + MDE | historical baseline + smallest effect worth detecting | analytics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ab-testing-implementation]] | plumbing for typed events, exposure dedup, and analyzer |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-experiment` | sonnet | Define hypothesis + metric + MDE + sample size. |
| `draft-bucketing-code` | haiku | Mechanical hash-based assignment. |
| `pre-register-doc` | sonnet | One-page pre-registration document. |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment_definition.json` | Pre-registration template: hypothesis + variants + metric + MDE + target sample size |
| `templates/bucketing.py` | Deterministic hash-based bucketing for stable variant assignment |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing-basics.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[ab-testing-implementation]]
- [[feature-flags-rollout-targeting]]
- [[feature-flags-types-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is there a clear primary metric AND enough traffic to reach 80% power on the expected effect?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/experiment_definition.json`

```json
{
  "experiment_id": "checkout-button-color-2026q2",
  "hypothesis": "Green CTA increases checkout conversion vs blue.",
  "variants": [
    {
      "id": "control",
      "weight": 0.5
    },
    {
      "id": "treatment",
      "weight": 0.5
    }
  ],
  "primary_metric": {
    "name": "checkout_conversion",
    "numerator": "checkouts_completed",
    "denominator": "checkouts_started"
  },
  "baseline_rate": 0.082,
  "minimum_detectable_effect": 0.005,
  "power": 0.8,
  "alpha": 0.05,
  "target_sample_size": 21000
}
```

### `templates/bucketing.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Deterministic hash-based bucketing for stable variant assignment","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#preregister-before-data","token_budget_impact":"~150 tokens when loaded"}}
import hashlib


def assign(experiment_id: str, user_id: str, variants: list[tuple[str, float]]) -> str:
    raw = f"{experiment_id}:{user_id}".encode()
    bucket = int(hashlib.sha256(raw).hexdigest(), 16) % 10000
    cum = 0
    for variant_id, weight in variants:
        cum += int(weight * 10000)
        if bucket < cum:
            return variant_id
    return variants[-1][0]
```
