# Predictive Analytics for PM

## Summary

**One-sentence:** Forecast report applying ML-based prediction to schedule delay, budget overrun, resource utilisation, and risk pattern mining from issue tracker data, with calibration metrics.

**One-paragraph:** Predictive Analytics for PM defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Programs with >=12 weeks of issue-tracker history (statistical signal exists).
- PMs who want a defensible early-warning signal beyond gut feel.
- Portfolio leads benchmarking multiple programs on uniform metrics.
- Risk owners wanting pattern-mining over historical issues.

## Applies If (ALL must hold)

- >=12 weeks of clean issue tracker data with timestamps + state changes.
- A data engineer or analyst can implement the forecasting pipeline.
- Calibration history available (prior forecasts + actual outcomes).
- Decision owner accepts probabilistic forecasts (not point estimates).

## Skip If (ANY kills it)

- Issue tracker data is dirty (state transitions missing, no timestamps) — fix data first.
- Project lifetime <12 weeks — too little data to forecast.
- Decision owner insists on deterministic estimates — predictive analytics will be rejected on delivery.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `predictive-analytics-pm_template_fill` | haiku | Bounded template fill, no judgement. |
| `predictive-analytics-pm_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `predictive-analytics-pm_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the predictive analytics forecast artefact. |
| `templates/calibration.py` | Reference script computing calibration score against prior forecasts. |
| `templates/forecast-report.md.j2` | Markdown skeleton for the forecast report with predictions table + calibration block. |
| `templates/forecast-report.md` | Markdown skeleton for the forecast report with predictions table + calibration block. Generated from `templates/forecast-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/predictive-analytics-pm.json",
  "type": "object",
  "required": [
    "forecast_id",
    "program_id",
    "dataset_window",
    "model_version",
    "predictions",
    "calibration",
    "decision_owner"
  ],
  "properties": {
    "forecast_id": {
      "type": "string"
    },
    "program_id": {
      "type": "string"
    },
    "dataset_window": {
      "type": "object",
      "required": [
        "from",
        "to"
      ]
    },
    "model_version": {
      "type": "string"
    },
    "predictions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "target",
          "p50",
          "p85",
          "p95"
        ]
      }
    },
    "calibration": {
      "type": "object",
      "required": [
        "score",
        "prior_forecasts_compared"
      ]
    },
    "decision_owner": {
      "type": "string"
    },
    "bias_audit_due": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### `templates/calibration.py`

```python
"""


"""calibration.py — check predicted-probability calibration on a holdout set.

Usage: python calibration.py holdout.parquet
Input parquet columns: y_true (0/1 int), y_prob (float 0..1)
Output: Brier score, calibration table, pass/fail (threshold: Brier < 0.20).
Exit 0 = calibration OK, exit 1 = fails threshold.
"""
from __future__ import annotations
import json
import sys

import pandas as pd
from sklearn.calibration import calibration_curve


def main(path: str) -> int:
    df = pd.read_parquet(path)  # cols: y_true (0/1), y_prob (0..1)
    prob_true, prob_pred = calibration_curve(
        df["y_true"], df["y_prob"], n_bins=10
    )
    brier = float(((df["y_prob"] - df["y_true"]) ** 2).mean())
    out = {
        "brier": brier,
        "calibration_table": list(
            zip(map(float, prob_pred), map(float, prob_true))
        ),
        "ok": brier < 0.20,  # threshold; tune per project
    }
    print(json.dumps(out, indent=2))
    if not out["ok"]:
        print(f"FAIL: Brier score {brier:.3f} exceeds threshold 0.20", file=sys.stderr)
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
```
