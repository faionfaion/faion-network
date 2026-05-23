<!-- purpose: minimal AI Prompt Patterns for Test Ideation artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: checklist artefact validated by scripts/validate-ai-prompt-patterns-test-ideation.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# AI Prompt Patterns for Test Ideation — Artefact

| Field | Value |
|-------|-------|
| artefact_id | ai-prompt-patterns-test-ideation-YYYY-MM-DD |
| owner | named human (no group terms) |
| last_touched | ISO-8601 timestamp |
| template_version | 1.1.0 |
| status | draft \| ready_for_review \| approved \| archived |

## Inputs

- Triggering activity: [from AGENTS.md Applies If list]
- Source-of-truth refs: [list URLs / design-file ids / dashboard snapshots]

## Methodology fields

| Field | Purpose |
|-------|---------|
| function_id | module.function the tests target |
| patterns_used | subset of [boundary, oracle, mutation] |
| boundary_cases | list of edge inputs and expected behaviour |
| oracles | list of {property, violating_test} |
| mutations_caught | list of {mutation_description, test_id_that_catches} |
| coverage_target | branch coverage threshold, conventionally 0.8 |
| evidence | list of {source, citation} pairs anchoring each oracle and mutation |

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned to 1.1.0
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-ai-prompt-patterns-test-ideation.py --file artefact.json` exits 0
