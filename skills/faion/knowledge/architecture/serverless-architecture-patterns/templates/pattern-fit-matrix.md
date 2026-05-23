<!-- __faion_header_v1__ -->
<!-- purpose: Matrix mapping workload signals to pattern fit. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: decision-record; depends-on: content/01-core-rules.xml#r1-pick-by-invocation-pattern -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Matrix mapping workload signals to pattern fit.","consumes":"see content/02-output-contract.xml","produces":"decision-record","depends_on":"content/01-core-rules.xml#r1-pick-by-invocation-pattern","token_budget_impact":"~150 tokens when loaded"}} -->
# Serverless Pattern Fit Matrix

| Workload signal             | API GW+Lambda | EventBridge+Lambda | Step Functions | SQS fan-out | Containers (Fargate/Cloud Run) |
|-----------------------------|---------------|--------------------|----------------|-------------|-------------------------------|
| Sync HTTP, low burst        | ✓             |                    |                |             | ✓ (lower cold-start)          |
| Async event integration     |               | ✓                  | ✓              | ✓           |                               |
| Long-running workflow > 15m |               |                    | ✓              |             | ✓                             |
| Fan-out batch               |               |                    |                | ✓           | ✓                             |
| Sub-50ms p99                |               |                    |                |             | ✓                             |
