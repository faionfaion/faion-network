<!--
purpose: per-intent rubric card co-authored by PM + SME for inclusion in acceptance-contract.yaml
consumes: query sample + SME interview output
produces: spec (rubric block per intent)
depends-on: rag-feature-acceptance-contract methodology
token-budget-impact: ~150t per intent when bundled into 05-examples context
-->

# Intent Rubric Card: <intent-name>

## PM outcome
<one sentence: what user outcome does success mean here?>

## Acceptable failure
<what failure mode is tolerable, what is NOT?>

## SME pass / borderline / fail (with verbatim examples)

### Pass example
- Query: "<real query from logs>"
- Expected answer pattern: <pattern + criterion>
- Why pass: <SME reason>

### Borderline example
- Query: "<real query>"
- Borderline answer: <what makes it borderline, not fail>
- Why not fail: <SME reason>

### Fail example
- Query: "<real query>"
- Failing answer: <what makes it fail>
- Why fail: <SME reason>

## Offline metrics (with baselines)

| Metric | Threshold | Baseline | Source |
|--------|-----------|----------|--------|
| faithfulness | >= X | Y (system Z) | run-id |
| context-precision | >= X | Y | run-id |

## Online metrics (paired)

| Metric | Threshold | Baseline | Telemetry source |
|--------|-----------|----------|------------------|
| thumbs-down-rate | <= X% | Y% (last 30d) | analytics |
| escalation-rate | <= X% | Y% | helpdesk |
