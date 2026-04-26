# Value Stream Management

## Summary

Value Stream Management (VSM) maps the end-to-end path from customer request to delivered value and measures flow using Lead Time, Cycle Time, Process Time, %Complete/Accurate, and Throughput. Paired with DORA metrics for the DevOps stages, VSM reveals where AI productivity gains evaporate into cross-functional bottlenecks invisible to per-team metrics. The rule: always report Flow Metrics and DORA together; never present one alone to executives.

## Why

Teams optimize locally while constraints shift upstream or downstream. A team can double deployment frequency (DORA elite) while lead time stays flat because the bottleneck moved to discovery, legal review, or onboarding. VSM is the only frame that makes this visible. Mik Kersten's Flow Framework and the Theory of Constraints provide the empirical anchors — focus on the one biggest constraint per quarter.

## When To Use

- Programs where local team optimization no longer produces business throughput gains.
- Boards report "green" velocity but customer time-to-value is stuck.
- AI productivity rollout raised dev velocity but lead time did not decrease (productivity paradox).
- DevOps maturity reviews requiring a complete picture beyond DORA.
- Multi-team programs (SAFe Value Streams, ARTs) where VSM is foundational.

## When NOT To Use

- Single team, single product, short cycle times — VSM overhead exceeds insight value.
- Data quality too poor to trust (status-field abuse, transitions not captured) — fix discipline first.
- Culture where metrics will be weaponized for individual performance management — VSM dies on first quarterly review.
- Pure research / discovery work where "value" is exploratory; VSM optimizes known-work flow.
- Bottleneck is known and political (approval committee) and leadership won't intervene — measuring changes nothing.

## Content

| File | What's inside |
|------|---------------|
| `content/01-metrics.xml` | Flow metrics definitions (Lead Time, Cycle Time, %C/A, Throughput, WIP), DORA metrics, how to pair them. |
| `content/02-vsm-process.xml` | VSM mapping steps, Theory-of-Constraints application, productivity-paradox detection, anti-patterns. |
| `content/03-agent-usage.xml` | Agentic workflows: value-stream-mapper, metrics-pipeline, bottleneck-detector, paradox-watcher. Gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flow-metrics.py` | Compute Lead Time, Cycle Time, and Throughput from a transitions CSV. |
