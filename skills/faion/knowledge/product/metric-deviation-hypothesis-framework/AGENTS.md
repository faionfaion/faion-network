# Metric Deviation Hypothesis Framework

## Summary

**One-sentence:** Produces a hypothesis report (named metric + named deviation + ≥3 ranked causes + ranked next-checks) so a metric anomaly stops being folklore and becomes a falsifiable next step.

**Ефективно для:** Solopreneurs reacting to dashboard wobble with vibes instead of a ranked-hypothesis pass that names what to check next and in what order.

**One-paragraph:** Dashboard metrics wobble; the indie reaction is 'must be the algo update' or 'maybe Tuesday is just low'. This methodology forces a structured pass: name the metric + the deviation magnitude + the time window, generate ≥3 ranked causal hypotheses (each with detector + estimated probability), and emit a ranked next-checks list. The output is consumed by the operator's followup queue.

## Applies If (ALL must hold)

- Operator notices a metric deviation ≥1.5σ from rolling baseline (or ≥20% WoW).
- Metric is instrumented with ≥4 weeks of history (baseline exists).
- Operator has read access to upstream funnel sources (events, server logs).
- A named owner exists to act on next-checks.

## Skip If (ANY kills it)

- Metric has <4 weeks of history — baseline is noise, defer until baseline exists.
- Deviation is within 1σ — not a deviation, just normal jitter.
- Operator cannot access upstream sources — hypotheses cannot be falsified.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| metric snapshot + baseline | time-series | analytics |
| deviation magnitude | % or σ | calculated |
| time window | datetime range | operator |
| upstream source list | array of URLs | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/mvp-instrumentation-checklist` | Upstream — instrumentation must be live for hypotheses to be checkable. |
| `solo/product/vanity-metrics-audit` | Sibling — flags whether the deviating metric is even worth chasing. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `compute_deviation` | haiku | Bounded math: σ / WoW computation. |
| `generate_hypotheses` | sonnet | Bounded judgement: enumerate ≥3 causal hypotheses. |
| `rank_next_checks` | opus | Cross-source synthesis: rank checks by P(falsify) × cost. |

## Templates

| File | Purpose |
|---|---|
| `templates/metric-deviation-hypothesis-framework.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/metric-deviation-hypothesis-framework.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-metric-deviation-hypothesis-framework.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[mvp-instrumentation-checklist]] — related methodology.
- [[vanity-metrics-audit]] — related methodology.
- [[solo-kpi-dashboard-template]] — related methodology.
- [[metric-deviation-hypothesis-framework]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
