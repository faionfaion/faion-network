<!-- __faion_header_v1__ -->
<!-- purpose: Lookup table mapping symptom → candidate patterns. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: decision-record; depends-on: content/01-core-rules.xml#r1-symptom-before-pattern -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Lookup table mapping symptom \u2192 candidate patterns.","consumes":"see content/02-output-contract.xml","produces":"decision-record","depends_on":"content/01-core-rules.xml#r1-symptom-before-pattern","token_budget_impact":"~150 tokens when loaded"}} -->
# Pattern Signal Table

| Symptom                                   | Candidate patterns                        |
|-------------------------------------------|-------------------------------------------|
| Multiple algorithms behind one interface  | Strategy, Template Method, Chain of Resp. |
| Object creation depends on context        | Factory Method, Abstract Factory, Builder |
| Wrap one interface as another             | Adapter, Facade                           |
| Add behaviour without subclassing         | Decorator                                 |
| Track many subscribers                    | Observer, Mediator                        |
| Object behaves differently by state       | State                                     |
| Cross-service write with rollback         | Saga (orchestration / choreography)       |
| External call fails intermittently        | Circuit Breaker, Retry-with-Backoff       |
| Read model differs from write model       | CQRS                                      |
| Event-sourced rebuildable state           | Event Sourcing                            |
