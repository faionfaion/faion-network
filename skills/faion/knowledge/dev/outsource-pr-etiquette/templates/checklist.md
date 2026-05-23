<!-- __faion_header_v1__ -->
<!-- purpose: Markdown checklist scaffolding the artefact items. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: checklist; depends-on: content/01-core-rules.xml#single-intent -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Markdown checklist scaffolding the artefact items.","consumes":"see content/02-output-contract.xml","produces":"checklist","depends_on":"content/01-core-rules.xml#single-intent","token_budget_impact":"~150 tokens when loaded"}} -->
# Outsource PR Etiquette — Checklist

- [ ] A PR carries exactly one intent (one feature, one fix, or one refactor). Mixed-intent PRs are split before opening.
- [ ] Diff size is ≤400 changed lines excluding lockfile updates and generated code. PRs over the cap are split or flagged with an explicit waiver.
- [ ] Every PR names a single primary reviewer (handle, not team). Teams may be added as secondary.
- [ ] Body contains a Repro section with the exact commands (clone, checkout branch, run) and the expected output that proves the change works.
- [ ] Behaviour changes ship with before/after screenshots, log snippets, or response payloads attached in the PR body.
- [ ] Each PR states the rollback in one sentence (revert SHA, feature-flag toggle, db rollback steps).

## Evidence links

- [ ] Link to artefact
- [ ] Link to validator self-test output
