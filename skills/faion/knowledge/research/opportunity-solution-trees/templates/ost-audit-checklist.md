<!-- purpose: OST hygiene audit (8 binary checks) -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->
# OST Audit

- [ ] Exactly 1 outcome at root
- [ ] Outcome is metric-based (name + value + target)
- [ ] Every opportunity scored (freq x sev x addr)
- [ ] Every solution has >=1 falsifiable assumption test
- [ ] No orphan solutions (must hang off an opportunity)
- [ ] No nodes deeper than 4 levels
- [ ] Kill list emitted in last monthly review
- [ ] Week-over-week opportunity score deltas tracked
