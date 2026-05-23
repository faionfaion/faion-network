<!--
purpose: Done-definition snippet for the PR template.
consumes: nothing — copy into .github/PULL_REQUEST_TEMPLATE.md.
produces: a checklist the reviewer reads (and the CI gate enforces).
depends-on: CI gate that fails on TODOs + missing CHANGELOG entry.
token-budget-impact: ~100 tokens when copied.
-->

## Done checklist (XP r6)

- [ ] All tests pass on this branch
- [ ] No TODO / FIXME / XXX comments introduced in changed files
- [ ] CHANGELOG.md updated under `## [Unreleased]`
- [ ] Lint + typecheck clean
- [ ] No new compiler warnings introduced
- [ ] Pair / AI-pair reviewer named (XP r4)

Bot enforces these mechanically; the box-tick is for human attention, not a substitute for the gate.
