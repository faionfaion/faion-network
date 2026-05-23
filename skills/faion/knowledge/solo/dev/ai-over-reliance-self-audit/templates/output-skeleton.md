<!-- purpose: minimal AI Over-Reliance Self-Audit artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: checklist artefact validated by scripts/validate-ai-over-reliance-self-audit.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# AI Over-Reliance Self-Audit — Artefact

| Field | Value |
|-------|-------|
| artefact_id | ai-over-reliance-self-audit-YYYY-MM-DD |
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
| audit_period | ISO date range the audit covers |
| checklist_items | list of {id, prompt, passed, evidence} entries |
| score | passed/total ratio in [0,1] |
| threshold | minimum acceptable score, conventionally 0.7 |
| remediation | list of drills/actions if score<threshold |
| next_audit_date | ISO date for the next cycle |

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned to 1.1.0
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-ai-over-reliance-self-audit.py --file artefact.json` exits 0
