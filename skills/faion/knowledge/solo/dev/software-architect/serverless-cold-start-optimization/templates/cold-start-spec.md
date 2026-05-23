<!-- __faion_header_v1__ -->
<!-- purpose: Spec capturing baseline + chosen mitigation + post-fix numbers. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec; depends-on: content/01-core-rules.xml#r1-measure-before-mitigating -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Spec capturing baseline + chosen mitigation + post-fix numbers.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#r1-measure-before-mitigating","token_budget_impact":"~150 tokens when loaded"}} -->
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
