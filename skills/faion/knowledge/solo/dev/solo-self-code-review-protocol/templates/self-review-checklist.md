<!-- purpose: Self-review checklist (>=10 items) + risk-flag list. -->
<!-- consumes: see content/02-output-contract.xml inputs for solo-self-code-review-protocol -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# Solo Self-Review Checklist (v1)

## Required items (tick or waive)

- [ ] tests cover new branches
- [ ] no print/console.log left in
- [ ] error handling on external calls (try/except, .map_err)
- [ ] no hard-coded secrets / credentials
- [ ] migration is reversible (down() implemented + tested) if applicable
- [ ] feature flag exists for user-visible changes
- [ ] types are explicit (no `any`, no `_=...`)
- [ ] logging is structured (key=value)
- [ ] new dependencies pass supply-chain checklist
- [ ] CHANGELOG.md entry under [Unreleased]

## Risk flags (mark RISKY if any apply)

- DB migrations
- Billing / payments
- Auth / session handling
- Hard delete operations
- Infrastructure config (k8s, terraform, nginx)
