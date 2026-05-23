# AI Feature Observability — Four Pillars

## Summary

**One-sentence:** Spec for the four observability pillars per AI feature — quality, latency, cost, drift — with dashboard panels, alert thresholds, and refresh cadences.

**One-paragraph:** Spec for the four observability pillars per AI feature — quality, latency, cost, drift — with dashboard panels, alert thresholds, and refresh cadences. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a spec produced by an agent applying ai feature observability — four pillars. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible spec for ai feature observability — four pillars across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- AI feature is in production or about to launch
- team owns the operational health of the feature end-to-end
- platform supports time-series + log aggregation at sufficient cardinality

## Skip If (ANY kills it)

- feature is internal-only prototype with no SLA — basic logging is enough
- feature is a thin proxy to a vendor with the vendor providing dashboards — link to those instead
- team uses an APM that already auto-instruments LLM calls — extend, don't re-do

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Time-series + log platform | Datadog / Prometheus / equivalent | platform |
| Trace propagation through LLM calls | OpenTelemetry / vendor SDK | platform |
| Eval suite (for quality pillar) | ml-engineering | ml-engineering |
| Cost attribution per call | logging | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[eval-driven-development-tdd-for-ai]] | Eval feeds quality pillar |
| [[inference-cost-unit-economics]] | Cost pillar feeds unit economics |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pillar_spec` | sonnet | Per pillar: metrics + dashboards + alerts. |
| `threshold_calibration` | sonnet | Calibrate alert thresholds from historical data. |
| `drift_design` | opus | Drift metric selection + sampling design. |

## Templates

| File | Purpose |
|------|---------|
| `templates/observability-spec.md` | Spec skeleton with the four pillars |
| `templates/dashboard-config.json` | Dashboard config JSON schema |
| `templates/_smoke-test.md` | Minimum viable filled-in observability spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-observability-four-pillars.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[eval-driven-development-tdd-for-ai]]
- [[inference-cost-unit-economics]]
- [[ai-feature-incident-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
