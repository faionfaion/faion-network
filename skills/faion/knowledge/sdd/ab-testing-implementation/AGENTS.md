# A/B Testing Implementation

## Summary

**One-sentence:** Implements typed ExperimentEvent, ExperimentTracker with in-request exposure dedup, ExperimentAnalyzer using z-test + Wilson CIs, and ExperimentReporter for dashboards.

**One-paragraph:** Implements typed ExperimentEvent, ExperimentTracker with in-request exposure dedup, ExperimentAnalyzer using z-test + Wilson CIs, and ExperimentReporter for dashboards. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Building plumbing for experiments: deterministic assignment, exposure tracking, conversion events.
- Need a typed event layer landing cleanly in Mixpanel/Amplitude/PostHog/warehouse.
- Stakeholders demand confidence intervals and per-variant breakdowns, not just point estimates.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Building plumbing for experiments: deterministic assignment, exposure tracking, conversion events.
- Need a typed event layer landing cleanly in Mixpanel/Amplitude/PostHog/warehouse.
- Stakeholders demand confidence intervals and per-variant breakdowns, not just point estimates.

## Skip If (ANY kills it)

- Using a managed platform (Optimizely, GrowthBook) that already provides analyzer + dashboards.
- Only a single experiment per quarter — manual SQL is cheaper than building plumbing.
- No exposure model yet — design the experiment first (see ab-testing-basics).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experiment definition | experiment_definition.json | ab-testing-basics output |
| Event schema | TypedDict / Pydantic model | team |
| Analytics sink | Mixpanel/Amplitude/PostHog/Postgres | infra |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ab-testing-basics]] | experiment design and sample-size calculation upstream of this code |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-event-types` | haiku | Mechanical typed dataclass + Pydantic model generation. |
| `implement-analyzer` | sonnet | Z-test + Wilson interval requires careful numeric code. |
| `dashboard-reporter` | sonnet | Layout + per-variant breakdown. |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment_event.py` | Typed ExperimentEvent (exposure + conversion) with stable schema |
| `templates/analyzer.py` | Two-proportion z-test with Wilson 95% CI |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing-implementation.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ab-testing-basics]]
- [[feature-flags-types-lifecycle]]
- [[feature-flags-services-testing]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is there a managed platform with an analyzer, or do we own plumbing?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/experiment_event.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Typed ExperimentEvent (exposure + conversion) with stable schema","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#typed-event-schema","token_budget_impact":"~150 tokens when loaded"}}
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


@dataclass
class ExperimentEvent:
    experiment_id: str
    user_id: str
    variant_id: str
    kind: Literal["exposure", "conversion"]
    ts: datetime
    properties: dict = field(default_factory=dict)
```

### `templates/analyzer.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Two-proportion z-test with Wilson 95% CI","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#typed-event-schema","token_budget_impact":"~150 tokens when loaded"}}
import math


def two_proportion_z(c1: int, n1: int, c2: int, n2: int) -> dict:
    if n1 == 0 or n2 == 0:
        return {"p_value": None, "reason": "empty arm"}
    p1, p2 = c1 / n1, c2 / n2
    p_pool = (c1 + c2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    if se == 0:
        return {"p_value": 1.0, "lift": 0.0}
    z = (p2 - p1) / se
    # two-sided p via normal CDF approximation
    p_value = math.erfc(abs(z) / math.sqrt(2))
    return {"p1": p1, "p2": p2, "z": z, "p_value": p_value, "lift": p2 - p1}


def wilson_ci(c: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    phat = c / n
    denom = 1 + z * z / n
    centre = (phat + z * z / (2 * n)) / denom
    half = (z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))
```
