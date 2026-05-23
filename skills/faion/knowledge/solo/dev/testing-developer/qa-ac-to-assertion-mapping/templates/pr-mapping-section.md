<!--
purpose: PR-description snippet reviewers expect to find for AC-to-assertion mapping.
consumes: see content/02-output-contract.xml inputs for qa-ac-to-assertion-mapping
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml + content/04-procedure.xml
token-budget-impact: ~150-400 tokens when loaded as context
-->

## AC-to-test mapping

| AC | Test path | Test name | Asserted behaviour | Class |
|----|-----------|-----------|--------------------|-------|
| AC-1 | tests/feature.spec.ts | submits valid form and persists | response 201 AND db.users row exists with expected email | state |
| AC-2 | tests/feature.spec.ts | rejects bad email | response 400 AND error.code = INVALID_EMAIL | negative |
| AC-3 | tests/feature.rate.spec.ts | rate-limits after 5 attempts | 6th call returns 429 AND retry-after header set | output |

Orphan ACs: none
Orphan tests in diff: none
Reviewer-walked: yes
