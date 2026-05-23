<!-- __faion_header_v1__ -->
<!-- purpose: Single ATAM-style scenario skeleton. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec; depends-on: content/01-core-rules.xml#r1-scenario-shape -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Single ATAM-style scenario skeleton.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#r1-scenario-shape","token_budget_impact":"~150 tokens when loaded"}} -->
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
