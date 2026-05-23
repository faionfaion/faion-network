<!-- purpose: Audit checklist (12 binary checks) used by the audit pass -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->
# Methodology Detail Audit

- [ ] Frontmatter: 14 required keys present + non-empty
- [ ] Summary section present (1-sentence + 1-paragraph)
- [ ] When-to-use >= 3 bullets
- [ ] When-not-to-use >= 2 bullets
- [ ] Core rules table has >= 5 testable rules
- [ ] Output contract references schema file
- [ ] Failure modes >= 3 antipatterns with symptom/root-cause/fix
- [ ] Procedure section present if complexity >= medium
- [ ] Examples section present if produces in spec|report
- [ ] Decision tree section references content/06-decision-tree.xml
- [ ] Templates table has >= 1 entry
- [ ] Validator script referenced; file exists
