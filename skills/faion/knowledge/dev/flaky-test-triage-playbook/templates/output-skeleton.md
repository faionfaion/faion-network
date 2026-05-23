<!-- purpose: minimal Flaky Test Triage Playbook artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: report artefact validated by scripts/validate-flaky-test-triage-playbook.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# Flaky Test Triage Playbook — Artefact

| Field | Value |
|-------|-------|
| artefact_id | flaky-test-triage-playbook-YYYY-MM-DD |
| owner | named human (no group terms) |
| last_touched | ISO-8601 timestamp |
| template_version | 1.1.0 |
| status | draft \| ready_for_review \| approved \| archived |

## Inputs

- Triggering activity: [from AGENTS.md Applies If list]
- Source-of-truth refs: [list URLs / ids / dashboard snapshots]

## Fields

[Fill per content/02-output-contract.xml schema. Every non-trivial field MUST carry a citation.]

## Self-check

- [ ] template_version pinned
- [ ] owner is single named human
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
