<!-- __faion_header_v1__ -->
<!-- purpose: Single ATAM-style scenario skeleton. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec -->
<!-- depends-on: content/02-output-contract.xml + content/01-core-rules.xml#r1-scenario-shape -->
<!-- token-budget-impact: ~350 tokens when loaded as context -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Single ATAM-style scenario skeleton.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/02-output-contract.xml + content/01-core-rules.xml#r1-scenario-shape","token_budget_impact":"~350 tokens when loaded as context"}} -->
# QA Scenario

| Field         | Value                                                       |
|---------------|-------------------------------------------------------------|
| ID            | qa-<short-slug>                                             |
| Source        | <who/what initiates>                                        |
| Stimulus      | <event>                                                     |
| Environment   | <normal | degraded | failure>                               |
| Artefact      | <system / module>                                           |
| Response      | <what the system does>                                      |
| Measure       | <numeric target>                                            |
| Priority      | high / medium / low                                          |
| Difficulty    | high / medium / low                                          |
