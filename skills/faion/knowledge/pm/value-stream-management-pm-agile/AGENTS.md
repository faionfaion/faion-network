# Value Stream Management

## Summary

**One-sentence:** Maps the end-to-end path from customer request to delivered value and measures flow using Lead Time, Cycle Time, Process Time, %Complete/Accurate, and Throughput.

**One-paragraph:** Maps the end-to-end path from customer request to delivered value and measures flow using Lead Time, Cycle Time, Process Time, %Complete/Accurate, and Throughput. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-value-stream-management.py` enforces the output contract.

**Ефективно для:**

- Diagnosing where a delivery pipeline stalls (commit → deploy gaps).
- Selecting the single bottleneck step to invest in next quarter.
- Comparing flow efficiency (Process Time / Lead Time) across teams.
- Producing a flow-metrics report for portfolio review.

## Applies If (ALL must hold)

- Team can timestamp each value-stream step (request → analysis → dev → test → deploy → live).
- ≥30 completed items in the last 90 days (statistical floor).
- A single bottleneck can be acted on without org restructure.

## Skip If (ANY kills it)

- <30 completed items in 90 days — sample too small.
- Steps are not timestamped — instrument first.
- Bottleneck requires org-wide restructuring — escalate, do not VSM.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Value-stream step list | ordered list | team |
| Per-item timestamps | CSV/JSON | tool API |
| Throughput target | items/week | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scrum-ceremonies]] | cadence + ceremony data feeds flow signal |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-flow` | haiku | Mechanical percentile computation. |
| `identify-bottleneck` | sonnet | Judgement: which step holds the longest wait. |
| `draft-report` | sonnet | Narrative around flow metrics. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flow-metrics.py` | Flow-metrics computation from timestamp CSV → JSON report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-value-stream-management.py` | Validate the report artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[scrum-ceremonies]]
- [[tool-migration-basics]]
- [[earned-value-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

