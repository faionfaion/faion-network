<!-- __faion_header_v1__ -->
<!-- purpose: Spec capturing baseline + chosen mitigation + post-fix numbers. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec -->
<!-- depends-on: content/02-output-contract.xml + content/01-core-rules.xml#r5-measure-after-fix -->
<!-- token-budget-impact: ~250 tokens when loaded as context -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Spec capturing baseline + chosen mitigation + post-fix numbers.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/02-output-contract.xml + content/01-core-rules.xml#r5-measure-after-fix","token_budget_impact":"~250 tokens when loaded as context"}} -->
# Cold Start Spec

## Baseline (measured)
- Cold start p99: <ms>
- Warm p99: <ms>
- Cold/warm ratio: <%>

## Latency budget
- p99: <ms>

## Chosen mitigation
- <runtime swap | provisioned concurrency | SnapStart | container migration | bundle trim>

## Post-fix (measured)
- Cold start p99: <ms>
- Warm p99: <ms>
- SLO met: yes/no

## Cost delta
- Provisioned concurrency cost: $<value>/month
- Net trade-off: <fill>
