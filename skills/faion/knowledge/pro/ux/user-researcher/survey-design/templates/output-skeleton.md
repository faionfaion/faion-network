<!-- purpose: minimal Survey Design artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-survey-design.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# Survey Design — Artefact

| Field | Value |
|-------|-------|
| artefact_id | survey-design-YYYY-MM-DD |
| owner | named human (no group terms) |
| last_touched | ISO-8601 timestamp |
| template_version | 1.1.0 |
| status | draft \| ready_for_review \| approved \| archived |

## Inputs

- Triggering activity: [from AGENTS.md Applies If list]
- Source-of-truth refs: [list URLs / transcript ids / dashboard snapshots]

## Fields

[Fill per content/02-output-contract.xml schema. Every non-trivial field MUST carry a citation.]

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned
- [ ] owner is single named human
- [ ] every non-trivial field has >=1 evidence row
- [ ] status is not approved unless a named reviewer signed off
