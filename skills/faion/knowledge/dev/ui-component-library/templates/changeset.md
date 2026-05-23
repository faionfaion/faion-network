<!-- purpose: Changeset entry template for a UI library release. -->
<!-- consumes: see content/02-output-contract.xml inputs for ui-component-library -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

---
'@acme/ui': minor
---

Add `Banner` primitive with `info | warn | error | success` variants. Deprecates `Alert` (warning for 2 minors).

- BREAKING (next major): remove `Alert` after v3.0.0.
- a11y: passes axe-core role + contrast.
- visual: 7 new Chromatic snapshots.
