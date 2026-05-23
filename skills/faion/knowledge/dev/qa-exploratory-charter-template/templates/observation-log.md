<!--
purpose: Time-stamped observation log written DURING the session.
consumes: see content/02-output-contract.xml inputs for qa-exploratory-charter-template
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml + content/04-procedure.xml
token-budget-impact: ~150-400 tokens when loaded as context
-->

# Observation log — ES-REPLACE

| Time | Kind (idea/observation/question/bug) | Note |
|------|--------------------------------------|------|
| 14:23 | idea | try unicode emoji in name field |
| 14:24 | observation | ZWJ emoji rendered as raw bytes in welcome email |
| 14:26 | bug | filed BUG-2118: ZWJ emoji not rendered |
| 14:27 | question | does this affect support tickets too? |
| 14:30 | idea | API path bypasses UI sanitiser |
