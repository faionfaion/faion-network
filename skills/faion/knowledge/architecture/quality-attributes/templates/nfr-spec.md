<!-- __faion_header_v1__ -->
<!-- purpose: NFR spec template aggregating scenarios into ISO-25010 categories. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec; depends-on: content/01-core-rules.xml#r1-scenario-shape -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"NFR spec template aggregating scenarios into ISO-25010 categories.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#r1-scenario-shape","token_budget_impact":"~150 tokens when loaded"}} -->
# Non-Functional Requirements Spec

## Performance
- Scenarios: <links>
- SLOs: p95 / p99 / availability targets

## Reliability
- Scenarios: <links>
- SLO: 99.9% per 30d

## Security
- Scenarios: <links>
- Standards: OWASP ASVS L2

## Maintainability
- Scenarios: <links>
- Targets: MTTR < 30 min for known issues

## Scalability
- Scenarios: <links>
- Headroom: 5x current load

## Usability / Accessibility
- Scenarios: <links>
- WCAG 2.2 AA

## Compliance
- Scenarios: <links>
- Standards: <list>

## Trade-off Matrix
| Conflict pair        | Resolution rule                              |
|----------------------|----------------------------------------------|
| perf vs cost         | <rule>                                       |
| security vs usability| <rule>                                       |
