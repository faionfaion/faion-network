<!-- purpose: agency-pricing-tiers playbook-step template -->
<!-- consumes: inputs named in AGENTS.md Prerequisites -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/06-decision-tree.xml -->
<!-- token-budget-impact: ~600 tokens when loaded -->
# Agency Pricing Tiers — Playbook step

## Owner
[name]

## Steps
1. id=s1 input=brief owner=lead exit_criterion="..." output_location=docs/...
2. id=s2 input=data owner=analyst exit_criterion="..." output_location=warehouse:tbl
3. id=s3 input=draft owner=writer exit_criterion="..." output_location=docs/drafts/
4. id=s4 input=draft owner=lead exit_criterion="signoff" output_location=docs/published/

## Decision branches
- when: signal_X < threshold then: loop back to s2

## Deviation log reference
[path / link]
