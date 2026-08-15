<!-- __faion_header_v1__ -->
<!-- purpose: ADR skeleton for serverless pattern selection. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: decision-record -->
<!-- depends-on: content/02-output-contract.xml + content/01-core-rules.xml#r1-pick-by-invocation-pattern -->
<!-- token-budget-impact: ~280 tokens once filled -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"ADR skeleton for serverless pattern selection.","consumes":"see content/02-output-contract.xml","produces":"decision-record","depends_on":"content/02-output-contract.xml + content/01-core-rules.xml#r1-pick-by-invocation-pattern","token_budget_impact":"~280 tokens once filled"}} -->
# ADR: Serverless Pattern Selection

## Status
Proposed

## Context
Workload: <fill>. Invocation pattern: <event-driven | sync request/response | scheduled | streaming>.

## Decision Drivers
- Latency budget
- Cost at expected RPS
- Cold-start tolerance
- Operational maturity

## Considered Patterns
1. API Gateway + Lambda (sync)
2. EventBridge + Lambda (event-driven)
3. Step Functions orchestration
4. SQS + Lambda fan-out
5. Containers (Fargate / Cloud Run)

## Decision
Chosen: <fill>. Rejected: <fill>.

## Consequences
Good: <fill>. Bad: <fill>. Review trigger: <fill>.
