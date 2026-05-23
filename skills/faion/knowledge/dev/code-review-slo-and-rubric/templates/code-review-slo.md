<!-- purpose: Markdown skeleton naming SLO + rubric + AI-pre-review pattern. | consumes: see content/02-output-contract.xml inputs | produces: artefact conforming to content/02-output-contract.xml (code-review-slo-and-rubric) | depends-on: content/01-core-rules.xml | token-budget-impact: small (template is loaded only when an artefact is being authored) -->
# Code Review SLO + Rubric — <team>

**Owner:** <@handle>
**Version:** 1.0.0
**Last reviewed:** 2026-05-23

## SLO

- First reviewer response: <= 24 business hours
- Merge after approval: <= 48 business hours
- Reviewer open-PR cap: 5

## Reviewer rotation

- Algorithm: round-robin within team excluding PR author
- On-call reviewer override: yes (for hotfixes)

## Rubric

### Blockers (must fix before merge)

- Correctness regression on a test case
- Security defect (injection, auth, secret leak)
- Public API contract change without a versioned migration
- Missing test for a new behaviour

### Nit-picks (suggestion, not blocking)

- Naming preference
- Formatting style
- Unrelated refactor request

## AI pre-review

- Tool: <Claude / CodeRabbit / GH Copilot>
- Scope: mechanical pass (style, obvious bugs, contract mismatch)
- Human reviewer: judgment pass (design, invariants, security, business correctness)

## Exceptions

Labeled `review-exception` + audit log entry.
